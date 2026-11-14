from math import radians, sin, cos, asin, sqrt

def haversine_km(lat1, lon1, lat2, lon2):
    """Great-circle distance between two coordinates in kilometres."""
    vals = [lat1, lon1, lat2, lon2]
    if any(v is None for v in vals):
        raise ValueError('All coordinates are required')
    if not (-90 <= lat1 <= 90 and -90 <= lat2 <= 90 and -180 <= lon1 <= 180 and -180 <= lon2 <= 180):
        raise ValueError('Coordinates are outside valid latitude/longitude ranges')
    dlat, dlon = radians(lat2-lat1), radians(lon2-lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    return 6371.0088 * 2 * asin(sqrt(a))
