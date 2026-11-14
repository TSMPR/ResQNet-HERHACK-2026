# ResQNet — AI Emergency Response Intelligence

**HERHACK 2026 | AI Track**

ResQNet is a hackathon prototype demonstrating AI-assisted classification of emergency-style text reports, a transparent human-review priority layer, and a dashboard over synthetic incident records.

> **Safety notice:** This is not an emergency service. It does not contact responders, dispatch help, verify incidents, or provide live resource availability. For immediate danger in India, contact 112 or the appropriate local emergency service directly.

## Problem

During emergencies, information can arrive as unstructured text from different sources. It may be difficult to quickly organise reports by type and route them for human review.

## Proposed solution

ResQNet demonstrates:
- NLP-based classification of text reports into broad incident categories.
- A transparent rule-based review-priority suggestion.
- A human-readable explanation for each result.
- A dashboard summarising synthetic sample incidents by area and category.
- Basic response checklists that reinforce human verification.

## Run locally

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Run tests

```bash
pytest -q
```

## Project structure

```text
ResQNet/
├── app.py
├── response_engine.py
├── data/
│   └── sample_incidents.csv
├── tests/
│   └── test_response_engine.py
├── requirements.txt
└── README.md
```

## Model details and limitations

The current baseline uses TF-IDF features and Logistic Regression trained on a small, hand-written illustrative set of text examples embedded in `response_engine.py`. It is not trained on a representative emergency dataset and has not been validated for operational use. Predictions may be incorrect, especially for multilingual, ambiguous, misspelled or out-of-distribution reports.

The priority layer is rule-based and is only a suggestion for human review. It is not a severity assessment or a substitute for emergency dispatch protocols.

The bundled CSV contains fictional demonstration records and approximate demo coordinates. It must not be interpreted as live incidents or actual resource locations.

## Responsible development roadmap

1. Obtain legally reusable, verified and appropriately labelled data.
2. Define a taxonomy with emergency-response domain experts.
3. Evaluate per-class precision, recall, F1, confusion matrix and calibration.
4. Test language, spelling, ambiguity and demographic/geographic bias.
5. Add human review, audit logs, access controls and privacy protections.
6. Integrate verified responder/resource directories only with formal permissions and live availability checks.
7. Conduct usability and safety testing with relevant stakeholders.

## Demo walkthrough

1. Start the Streamlit app.
2. Enter a sample incident description.
3. Review predicted category, suggested review priority and explanation.
4. Review the safety checklist.
5. Open the dashboard and explain that all displayed records are synthetic.
