"""Backward-compatible imports for tests and scripts from the original ResQNet prototype.

The current implementation lives in backend.engine. This module keeps the
original top-level API available while using the expanded ResQNet dataset.
"""
import pandas as pd

from backend.engine import classify_report as _classify_report


_PRIORITY = {
    "Medical": "Urgent review",
    "Fire": "Urgent review",
    "Flood": "High review",
    "Road accident": "High review",
    "Cyclone / storm": "High review",
    "Earthquake": "High review",
    "Landslide": "High review",
    "Infrastructure": "Routine review",
    "Other": "Unclassified review",
}


def classify_report(text: str) -> dict:
    """Classify an incident using the current backend model.

    Retains the original function name so older tests can import it.
    """
    result = _classify_report(text)
    result["priority"] = _PRIORITY.get(result["category"], "Human review")
    return result


def get_response_guidance(result: dict) -> list[str]:
    """Return non-operational, human-review guidance for a predicted category."""
    category = result.get("category", "Other")
    common = [
        "A trained human operator must verify the report, location and current status.",
        "Preserve the original source and timestamp where available.",
        "Do not publish personal or sensitive information.",
        "Do not treat an AI prediction as confirmation that an incident occurred.",
    ]
    specific = {
        "Medical": [
            "For an immediate medical emergency in India, contact 112 or local emergency medical services.",
            "Do not attempt medical treatment based only on this system's output.",
        ],
        "Fire": [
            "Keep people away from smoke, flames and hazardous structures.",
            "Do not enter a burning or smoke-filled building.",
            "For an active fire in India, contact 112 or the local fire service.",
        ],
        "Flood": [
            "Avoid entering moving or rising water.",
            "Follow verified local evacuation instructions and official alerts.",
        ],
        "Road accident": [
            "Keep clear of moving traffic and report possible injuries to emergency services.",
        ],
        "Infrastructure": [
            "Refer the issue to the relevant municipal, electricity or utility authority.",
        ],
        "Cyclone / storm": [
            "Follow official weather warnings and avoid exposed outdoor areas during severe conditions.",
        ],
        "Earthquake": [
            "Follow official earthquake safety guidance and avoid visibly damaged structures.",
        ],
        "Landslide": [
            "Keep away from unstable slopes and blocked areas; follow local authority instructions.",
        ],
        "Other": [
            "Request additional information and human verification before assigning an operational priority.",
        ],
    }
    return specific.get(category, specific["Other"]) + common


def summarize_incidents(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize incident counts by area and category.

    Supports the original schema (area, category). If area is absent, it uses
    location when available; otherwise it groups all reports under 'Unknown'.
    """
    if "category" not in df.columns:
        raise ValueError("DataFrame must contain a 'category' column.")

    work = df.copy()
    if "area" not in work.columns:
        if "location" in work.columns:
            work["area"] = work["location"].fillna("Unknown")
        else:
            work["area"] = "Unknown"

    return (
        work.groupby(["area", "category"], as_index=False)
        .size()
        .rename(columns={"size": "sample_reports"})
        .sort_values(["area", "sample_reports"], ascending=[True, False])
        .reset_index(drop=True)
    )
