# ResQNet — Project Brief

## One-line pitch
ResQNet uses a lightweight NLP model to organise emergency-style text reports into explainable categories and human-review queues, supported by a dashboard of synthetic incident data.

## Target users
- Emergency coordination teams (conceptual target; not connected in this prototype)
- Campus and community administrators
- Disaster-preparedness organisations
- Civic response coordinators

## Core demonstration
1. Enter an example report.
2. Show predicted category and suggested review priority.
3. Explain which model/rule signals contributed.
4. Show safe, human-led next-step guidance.
5. Explore the synthetic incident dashboard.

## What makes it stronger than a generic chatbot
- A reproducible ML classification pipeline.
- A separate, transparent rule layer.
- Structured incident summaries.
- Clear human-in-the-loop boundary.
- Explicit limitations and data provenance.

## Suggested group name
**Team NovaSakhi**

Tagline: "Intelligence that coordinates. Innovation that cares."

Alternative names: ResponseX, CodeResQ, Team PulseAI, SignalForce.

## Suggested team roles
- AI/ML lead: dataset, text preprocessing, classifier evaluation.
- Backend/data lead: incident schema, validation, API and data pipeline.
- Frontend lead: Streamlit dashboard and demo experience.
- Research/pitch lead: problem validation, impact, safety and presentation.

## 90-second pitch
"During emergencies, reports often arrive as unstructured messages. Before useful coordination can happen, teams need to understand what kind of incident is being reported and what needs human review. ResQNet is an AI-assisted prototype that classifies text reports into broad categories such as medical, fire, flood and road accidents. It adds a transparent review-priority layer, explains its suggestions, and visualises incident patterns using synthetic demonstration data. We deliberately keep humans in control: the model does not verify incidents or dispatch responders. Our next step is to evaluate it on responsibly sourced, labelled data and work with domain experts to build a safe coordination workflow."
