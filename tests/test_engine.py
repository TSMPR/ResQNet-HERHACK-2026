from backend.engine import classify_report, find_duplicates

def test_empty_report_rejected():
    try: classify_report('   ')
    except ValueError: return
    assert False, 'Expected ValueError'

def test_classifier_returns_expected_schema():
    out = classify_report('Heavy rain has flooded houses and roads')
    assert out['category'] in ['Flood','Fire','Road accident','Medical','Infrastructure','Cyclone / storm','Earthquake','Landslide','Other']
    assert 0 <= out['score'] <= 1
    assert out['review_status'] == 'human_review_required'

def test_duplicate_match():
    rows = [{'report_id':'A1','text':'Heavy rain has flooded houses and roads'}]
    matches = find_duplicates('Heavy rain has flooded houses and roads', rows, threshold=0.4)
    assert matches and matches[0]['report_id'] == 'A1'
