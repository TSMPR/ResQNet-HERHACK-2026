from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
from typing import Optional
from pathlib import Path
from datetime import datetime, timezone
import sqlite3, uuid, shutil
from .engine import classify_report, find_duplicates
from .geo import haversine_km

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / 'data' / 'resqnet.db'
UPLOADS = ROOT / 'uploads'
UPLOADS.mkdir(exist_ok=True)
app = FastAPI(title='ResQNet API', version='0.1.0', description='Research/demo decision-support API. Not an emergency service.')

def conn():
    c = sqlite3.connect(DB); c.row_factory = sqlite3.Row; return c

def init_db():
    with conn() as c:
        c.execute('CREATE TABLE IF NOT EXISTS reports(report_id TEXT PRIMARY KEY,text TEXT NOT NULL,language TEXT,category TEXT,score REAL,latitude REAL,longitude REAL,source TEXT,created_at TEXT,review_status TEXT,cluster_id TEXT)')
        c.execute('CREATE TABLE IF NOT EXISTS review_log(id INTEGER PRIMARY KEY AUTOINCREMENT,report_id TEXT,decision TEXT,note TEXT,created_at TEXT)')
        c.execute('CREATE TABLE IF NOT EXISTS resources(resource_id TEXT PRIMARY KEY,resource_type TEXT,area TEXT,latitude REAL,longitude REAL,availability TEXT,last_updated TEXT)')
        if c.execute('SELECT COUNT(*) FROM resources').fetchone()[0] == 0:
            demo = [('R-001','medical_team','Demo area',17.385,78.4867,'demo_only'),('R-002','fire_unit','Demo area',17.40,78.48,'demo_only'),('R-003','rescue_boat','Demo area',17.42,78.50,'demo_only')]
            c.executemany('INSERT INTO resources VALUES(?,?,?,?,?,?,?)', [(a,b,d,e,f,g,datetime.now(timezone.utc).isoformat()) for a,b,d,e,f,g in demo])
init_db()

class ReportIn(BaseModel):
    text: str = Field(min_length=3, max_length=5000)
    language: str = 'auto'
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    source: str = 'user_submitted_demo'
class ReviewIn(BaseModel):
    decision: str = Field(pattern='^(verified|rejected|needs_more_information)$')
    note: str = ''

@app.get('/health')
def health(): return {'status':'ok','service':'ResQNet','mode':'demo'}

@app.post('/api/v1/reports')
def create_report(item: ReportIn):
    try: pred = classify_report(item.text, item.language)
    except Exception as e: raise HTTPException(400, str(e))
    rid = 'RPT-' + uuid.uuid4().hex[:10]
    with conn() as c:
        existing = [dict(r) for r in c.execute('SELECT report_id,text FROM reports ORDER BY created_at DESC LIMIT 300').fetchall()]
        duplicates = find_duplicates(item.text, existing)
        c.execute('INSERT INTO reports VALUES(?,?,?,?,?,?,?,?,?,?,?)', (rid,item.text,item.language,pred['category'],pred['score'],item.latitude,item.longitude,item.source,datetime.now(timezone.utc).isoformat(),'human_review_required',None))
    return {'report_id':rid,'prediction':pred,'candidate_duplicates':duplicates,'note':'Prediction and duplicate matches require human verification.'}

@app.get('/api/v1/reports')
def list_reports(limit: int = 100):
    with conn() as c: rows = c.execute('SELECT * FROM reports ORDER BY created_at DESC LIMIT ?', (min(max(limit,1),500),)).fetchall()
    return [dict(r) for r in rows]

@app.get('/api/v1/reports/{report_id}')
def get_report(report_id: str):
    with conn() as c: r = c.execute('SELECT * FROM reports WHERE report_id=?',(report_id,)).fetchone()
    if not r: raise HTTPException(404,'Report not found')
    return dict(r)

@app.post('/api/v1/reports/{report_id}/review')
def review_report(report_id: str, item: ReviewIn):
    now = datetime.now(timezone.utc).isoformat()
    with conn() as c:
        if not c.execute('SELECT 1 FROM reports WHERE report_id=?',(report_id,)).fetchone(): raise HTTPException(404,'Report not found')
        c.execute('UPDATE reports SET review_status=? WHERE report_id=?',(item.decision,report_id))
        c.execute('INSERT INTO review_log(report_id,decision,note,created_at) VALUES(?,?,?,?)',(report_id,item.decision,item.note,now))
    return {'report_id':report_id,'review_status':item.decision,'recorded_at':now}

@app.get('/api/v1/resources')
def resources():
    with conn() as c: rows = c.execute('SELECT * FROM resources').fetchall()
    return [dict(r) for r in rows]

@app.get('/api/v1/resources/nearby')
def nearby_resources(latitude: float, longitude: float, radius_km: float = 20.0, resource_type: Optional[str] = None):
    if not (-90 <= latitude <= 90 and -180 <= longitude <= 180) or not (0 < radius_km <= 500):
        raise HTTPException(400, 'Invalid coordinates or radius')
    with conn() as c:
        rows = c.execute('SELECT * FROM resources').fetchall()
    found = []
    for row in rows:
        item = dict(row)
        if resource_type and item['resource_type'] != resource_type:
            continue
        item['distance_km'] = round(haversine_km(latitude, longitude, item['latitude'], item['longitude']), 2)
        if item['distance_km'] <= radius_km:
            found.append(item)
    return {'results': sorted(found, key=lambda x: x['distance_km']), 'warning': 'Inventory is fictional demo data; availability and response capability are not verified.'}

@app.post('/api/v1/reports/voice')
async def voice_upload(file: UploadFile = File(...)):
    ext = Path(file.filename or 'audio.wav').suffix.lower()
    if ext not in ['.wav','.mp3','.m4a','.ogg','.webm']: raise HTTPException(400,'Unsupported audio format')
    path = UPLOADS / (uuid.uuid4().hex + ext)
    with path.open('wb') as out: shutil.copyfileobj(file.file,out)
    return {'status':'uploaded_not_transcribed','file_id':path.name,'message':'Upload storage only. Speech-to-text inference is not enabled in this MVP.'}

@app.post('/api/v1/reports/image')
async def image_upload(file: UploadFile = File(...)):
    ext = Path(file.filename or 'image.jpg').suffix.lower()
    if ext not in ['.jpg','.jpeg','.png','.webp']: raise HTTPException(400,'Unsupported image format')
    path = UPLOADS / (uuid.uuid4().hex + ext)
    with path.open('wb') as out: shutil.copyfileobj(file.file,out)
    return {'status':'uploaded_not_analysed','file_id':path.name,'message':'Upload storage only. Visual model inference is not enabled in this MVP.'}

@app.get('/api/v1/metrics')
def metrics():
    with conn() as c:
        total = c.execute('SELECT COUNT(*) FROM reports').fetchone()[0]
        cats = [dict(r) for r in c.execute('SELECT category,COUNT(*) AS count FROM reports GROUP BY category').fetchall()]
        statuses = [dict(r) for r in c.execute('SELECT review_status,COUNT(*) AS count FROM reports GROUP BY review_status').fetchall()]
    return {'total_reports':total,'by_category':cats,'by_review_status':statuses}
