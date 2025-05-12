def calculate_area(rectangle):
    """Calculate the area of a rectangle given its coordinates."""
    x1, y1, x2, y2 = rectangle
    return abs((x2 - x1) * (y2 - y1))

def is_point_in_rectangle(point, rectangle):
    """Check if a point is inside a given rectangle."""
    x, y = point
    x1, y1, x2, y2 = rectangle
    return x1 <= x <= x2 and y1 <= y <= y2

def rectangle_to_geojson(rectangle):
    """Convert a rectangle defined by its coordinates to GeoJSON format."""
    x1, y1, x2, y2 = rectangle
    coordinates = [
        [x1, y1],
        [x2, y1],
        [x2, y2],
        [x1, y2],
        [x1, y1]  # Closing the polygon
    ]
    return {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [coordinates]
        },
        "properties": {}
    }