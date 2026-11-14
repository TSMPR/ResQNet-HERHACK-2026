# ResQNet: One-Night Build Plan

## Goal
Deliver a credible, demonstrable multilingual emergency-report intelligence prototype in one focused night. Prioritize a working end-to-end flow over a long list of unfinished integrations.

## Recommended model stack

### Primary semantic model: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
Use this pretrained multilingual sentence encoder for semantic similarity and candidate duplicate detection across English, Telugu and Hindi. It creates sentence embeddings; compare them with cosine similarity. It is a pretrained encoder, not a disaster classifier and not a model trained specifically on ResQNet data.

### Incident category model: TF-IDF + Logistic Regression baseline
Keep the bundled baseline as the reliable, fast, reproducible classifier. Train it on the labelled CSV, report held-out metrics, and show its limitations. Do not present its score as a calibrated probability.

### Optional next-stage classifier: `xlm-roberta-base`
The Colab notebook contains a fine-tuning path for multilingual classification. Treat this as a next-stage experiment, not a requirement for the overnight demo. Fine-tune only after obtaining a larger, reviewed, non-synthetic dataset and a leakage-safe split.

## Minimum demo acceptance criteria
1. Submit an incident report in English, Telugu or Hindi.
2. Display predicted category, model score, evidence terms and a human-review warning.
3. Show semantically similar earlier reports as duplicate candidates (never auto-delete or merge).
4. Persist the report in SQLite and display it in the incident monitor.
5. Display the demo resource-distance lookup with a clear fictional-data label.
6. Run automated tests and save a test/evaluation report.
7. Push the source code to GitHub without credentials, uploads, databases or model binaries.

## Suggested overnight schedule

| Time | Work | Deliverable |
|---|---|---|
| Hour 1 | Create venv, install requirements, run API and dashboard | App starts locally |
| Hour 2 | Inspect data, train baseline, run evaluation | Metrics and confusion matrix |
| Hours 3–4 | Exercise multilingual reports and duplicate candidates | Recorded demo cases |
| Hour 5 | Add/verify semantic encoder duplicate-search integration if environment permits | Similarity demo |
| Hour 6 | Run pytest, fix failures, test API through `/docs` | Passing tests |
| Hour 7 | Add screenshots, architecture notes and limitations | Demo-ready README |
| Hour 8 | Git commits, push, rehearse 3-minute demo | GitHub repository |

If the pretrained encoder download or installation takes too long, keep the existing character n-gram duplicate matcher and complete the end-to-end app. A working, tested baseline is better than a half-installed transformer.

## Training and evaluation rules
- Start with `python scripts/train_baseline.py`.
- Run `python scripts/evaluate_baseline.py` and `python -m pytest -q`.
- The included dataset is synthetic and small. Its metrics are pipeline checks only, not evidence of real-world accuracy.
- For meaningful evaluation, gather permissioned, representative reports; have native-language reviewers validate labels; split by event/source to avoid near-duplicate leakage; retain an untouched test set.
- Report accuracy, macro precision, macro recall, macro F1 and a confusion matrix. Inspect per-language results separately.
- Do not claim production readiness, live emergency detection or verified dispatch.

## Demo narrative
A user reports a flooded road in Telugu. ResQNet classifies the report, surfaces similar reports, stores it, and shows nearby fictional resource records. A reviewer checks the report and records a decision. Explain that the system assists triage; a human must verify all reports and resources.
