from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

ROOT = Path(__file__).resolve().parents[1]
train = pd.read_csv(ROOT / "data" / "train_reports.csv")
test = pd.read_csv(ROOT / "data" / "test_reports.csv")
model = Pipeline([("features", FeatureUnion([
    ("word", TfidfVectorizer(ngram_range=(1, 2), analyzer="word", sublinear_tf=True)),
    ("char", TfidfVectorizer(ngram_range=(2, 5), analyzer="char", sublinear_tf=True)),
])), ("clf", LogisticRegression(max_iter=1500, class_weight="balanced"))])
model.fit(train.text.astype(str), train.category.astype(str))
pred = model.predict(test.text.astype(str))
print("Held-out test accuracy:", round(accuracy_score(test.category, pred), 4))
print(classification_report(test.category, pred, zero_division=0))
print("Confusion matrix labels:", list(model.classes_))
print(confusion_matrix(test.category, pred, labels=model.classes_))
print("CAUTION: all bundled rows are synthetic. These metrics test the pipeline only, not real-world performance.")
