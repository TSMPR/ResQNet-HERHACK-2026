import pytest
from backend.geo import haversine_km

def test_same_point_is_zero():
    assert haversine_km(17.385,78.4867,17.385,78.4867) == 0

def test_invalid_coordinates_rejected():
    with pytest.raises(ValueError):
        haversine_km(100,0,0,0)
