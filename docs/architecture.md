# Architecture overview
- `dashboard.py`: Streamlit client.
- `backend/app.py`: FastAPI routes, SQLite persistence, upload endpoints and review logging.
- `backend/engine.py`: TF-IDF word/character baseline, prediction formatting and candidate duplicate matcher.
- `data/training_reports.csv`: synthetic multilingual demonstration corpus.
- `notebooks/ResQNet_Colab_Training.ipynb`: XLM-R training workflow.

Future stages: async workers, PostgreSQL/PostGIS, authenticated roles, real speech and vision inference, source adapters, event clustering, model monitoring and audit controls. These are not completed capabilities in this release.
