import pytest
from response_engine import classify_report, get_response_guidance, summarize_incidents
import pandas as pd

def test_medical_report_classified():
    result = classify_report("A person is unconscious and not responding")
    assert result["category"] == "Medical"
    assert result["priority"] == "Urgent review"

def test_fire_report_has_safety_guidance():
    result = classify_report("There are flames and heavy smoke in the building")
    assert result["category"] == "Fire"
    assert any("safe distance" in x for x in get_response_guidance(result))

def test_empty_report_rejected():
    with pytest.raises(ValueError):
        classify_report("   ")

def test_summary_counts_rows():
    data = pd.DataFrame([
        {"area": "A", "category": "Fire"},
        {"area": "A", "category": "Fire"},
        {"area": "B", "category": "Medical"},
    ])
    summary = summarize_incidents(data)
    assert int(summary["sample_reports"].sum()) == 3
