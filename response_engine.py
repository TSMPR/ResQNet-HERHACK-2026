"""Baseline incident classification and human-review guidance."""
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Small, intentionally illustrative training set. Not representative of real emergencies.
TRAINING = [
    ("vehicle collision on road, crash, injured person", "Road accident"),
    ("car hit motorcycle, traffic collision, injured", "Road accident"),
    ("two vehicles crashed and road is blocked", "Road accident"),
    ("building fire, smoke, flames, people evacuating", "Fire"),
    ("kitchen fire with heavy smoke in apartment", "Fire"),
    ("electrical short circuit caused flames", "Fire"),
    ("person collapsed, unconscious, not responding", "Medical"),
    ("someone has severe bleeding and needs medical help", "Medical"),
    ("person having difficulty breathing and chest pain", "Medical"),
    ("flood water rising, street submerged, people stranded", "Flood"),
    ("heavy rain flooding houses and roads", "Flood"),
    ("water entered homes and residents need evacuation", "Flood"),
    ("street light broken, pothole, damaged road", "Infrastructure"),
    ("tree fallen and blocking road, no injuries reported", "Infrastructure"),
    ("power line down near sidewalk", "Infrastructure"),
    ("lost bag, minor inconvenience, asking for information", "Other"),
    ("asking for directions and general assistance", "Other"),
    ("noise complaint with no immediate danger", "Other"),
]

PRIORITY_RULES = {
    "Medical": ("Urgent review", ["medical", "unconscious", "bleeding", "breathing"]),
    "Fire": ("Urgent review", ["fire", "smoke", "flames", "burning"]),
    "Flood": ("High review", ["flood", "water rising", "stranded", "submerged"]),
    "Road accident": ("High review", ["collision", "crash", "injured", "accident"]),
    "Infrastructure": ("Routine review", ["pothole", "street light", "tree fallen", "power line"]),
    "Other": ("Unclassified review", []),
}

def build_model():
    texts, labels = zip(*TRAINING)
    model = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), lowercase=True)),
        ("classifier", LogisticRegression(max_iter=1000, random_state=42))
    ])
    model.fit(texts, labels)
    return model

_MODEL = build_model()

def classify_report(text: str) -> dict:
    clean = re.sub(r"\s+", " ", (text or "")).strip()
    if not clean:
        raise ValueError("Report text cannot be empty.")
    category = _MODEL.predict([clean])[0]
    priority, terms = PRIORITY_RULES[category]
    lowered = clean.lower()
    matched = [term for term in terms if term in lowered]
    if matched:
        explanation = f"The model matched the report to '{category}'. The following configured terms were also found: {', '.join(matched)}."
    else:
        explanation = f"The model matched the report to '{category}' based on learned word patterns. No configured explanation terms were found."
    return {"category": category, "priority": priority, "explanation": explanation}

def get_response_guidance(result: dict) -> list[str]:
    category = result["category"]
    common = [
        "A trained human operator should verify the report, location and current status.",
        "Record the source and timestamp if this is part of an authorised response workflow.",
        "Do not share identifying or sensitive information in public channels."
    ]
    specific = {
        "Medical": ["If there is immediate danger, contact emergency medical services directly."],
        "Fire": ["Keep a safe distance and contact the fire service directly if there is an active fire."],
        "Flood": ["Avoid entering moving or rising water; follow official evacuation instructions."],
        "Road accident": ["Keep clear of traffic and contact emergency services if anyone may be injured."],
        "Infrastructure": ["Route the issue to the relevant municipal or utility authority."],
        "Other": ["Request clarification from the reporter before assigning an operational priority."]
    }
    return specific[category] + common

def summarize_incidents(df: pd.DataFrame) -> pd.DataFrame:
    return (df.groupby(["area", "category"], as_index=False)
              .size().rename(columns={"size": "sample_reports"})
              .sort_values(["area", "sample_reports"], ascending=[True, False]))
