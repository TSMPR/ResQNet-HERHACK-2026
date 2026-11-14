# Model card — ResQNet baseline
- Model: word + character TF-IDF with Logistic Regression.
- Training data: `data/training_reports.csv`.
- Data status: curated synthetic examples for software demonstration.
- Intended use: local prototype testing and educational experimentation only.
- Not intended for real emergency triage, severity determination, dispatch, diagnosis or safety decisions.
- Scores: raw classifier scores; not calibrated probabilities.
- Known limitations: small synthetic dataset, limited linguistic variation, domain shift, ambiguity and no real-world validation.
- Evaluation: run tests and Colab notebook; do not publish performance claims based on synthetic data.
