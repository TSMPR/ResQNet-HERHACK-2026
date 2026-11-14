"""ResQNet baseline classifier. Bundled data is synthetic demo data only."""
from pathlib import Path
import re
import joblib
import pandas as pd
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'train_reports.csv'
MODEL = ROOT / 'models' / 'baseline.joblib'

def train_baseline(data_path=DATA, model_path=MODEL):
    df = pd.read_csv(data_path).dropna(subset=['text', 'category'])
    features = FeatureUnion([
        ('word', TfidfVectorizer(ngram_range=(1, 2), analyzer='word', min_df=1, sublinear_tf=True)),
        ('char', TfidfVectorizer(ngram_range=(2, 5), analyzer='char', min_df=1, sublinear_tf=True)),
    ])
    model = Pipeline([('features', features), ('clf', LogisticRegression(max_iter=1200, class_weight='balanced'))])
    model.fit(df['text'].astype(str), df['category'].astype(str))
    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)
    return model

def load_model():
    return joblib.load(MODEL) if MODEL.exists() else train_baseline()

_MODEL = None
def classify_report(text, language='auto'):
    clean = re.sub(r'\s+', ' ', str(text or '')).strip()
    if not clean:
        raise ValueError('Report text cannot be empty.')
    global _MODEL
    if _MODEL is None:
        _MODEL = load_model()
    probs = _MODEL.predict_proba([clean])[0]
    classes = list(_MODEL.classes_)
    order = probs.argsort()[::-1]
    category = classes[int(order[0])]
    terms = re.findall(r'[A-Za-z]+|[\u0C00-\u0C7F]+|[\u0900-\u097F]+', clean)
    return {
        'category': category,
        'score': round(float(probs[order[0]]), 4),
        'score_label': 'uncalibrated model score',
        'review_status': 'human_review_required',
        'language': language,
        'evidence_terms': list(dict.fromkeys(terms))[:8],
        'alternatives': [{'category': classes[int(i)], 'score': round(float(probs[i]), 4)} for i in order[1:3]],
        'explanation': f"The baseline classifier ranked '{category}' highest. This is not a verified incident or calibrated probability. Review the original report and location."
    }

def find_duplicates(text, rows, threshold=0.48):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    candidates = [r for r in rows if r.get('text')]
    if not candidates or not text.strip():
        return []
    matrix = TfidfVectorizer(analyzer='char', ngram_range=(2, 5)).fit_transform([text] + [r['text'] for r in candidates])
    scores = cosine_similarity(matrix[0:1], matrix[1:]).ravel()
    result = []
    for idx in scores.argsort()[::-1]:
        if scores[idx] >= threshold:
            result.append({'report_id': candidates[int(idx)].get('report_id'), 'text': candidates[int(idx)]['text'], 'similarity': round(float(scores[idx]), 3)})
    return result[:5]
