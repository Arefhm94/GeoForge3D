def calculate_area(rectangle):
    """Calculate the area of a rectangle given its coordinates."""
    x1, y1, x2, y2 = rectangle
    return abs((x2 - x1) * (y2 - y1))

def validate_rectangle(rectangle):
    """Validate that the rectangle coordinates are in the correct order."""
    x1, y1, x2, y2 = rectangle
    if x1 >= x2 or y1 >= y2:
        raise ValueError("Invalid rectangle coordinates: ensure x1 < x2 and y1 < y2.")

def export_geojson(rectangle):
    """Export the rectangle as a GeoJSON feature."""
    x1, y1, x2, y2 = rectangle
    geojson = {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [x1, y1],
                [x2, y1],
                [x2, y2],
                [x1, y2],
                [x1, y1]
            ]]
        },
        "properties": {}
    }
    return geojson