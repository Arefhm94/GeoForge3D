import json
import math
from pyproj import Transformer

def extract_center_and_distance(geojson_path):
    """
    Reads a GeoJSON file, extracts the center of the polygon,
    and calculates the distance from center to one edge.
    
    Args:
        geojson_path: Path to the GeoJSON file
        
    Returns:
        tuple: ((formatted_lat, formatted_lon), distance_in_meters)
    """
    # Read the GeoJSON file
    with open(geojson_path, 'r') as file:
        data = json.load(file)
    
    # Extract the polygon coordinates
    features = data['features']
    if not features:
        return None, None
    
    geometry = features[0]['geometry']
    if geometry['type'] != 'Polygon':
        return None, None
    
    coordinates = geometry['coordinates'][0]  # Get the exterior ring
    
    # Calculate the center by averaging coordinates
    sum_lon = sum(coord[0] for coord in coordinates[:-1])  # Exclude the closing point
    sum_lat = sum(coord[1] for coord in coordinates[:-1])
    num_points = len(coordinates) - 1  # Exclude the closing point
    
    center_lon = sum_lon / num_points
    center_lat = sum_lat / num_points
    
    # Calculate distance from center to one edge (using the first edge)
    edge_midpoint_lon = (coordinates[0][0] + coordinates[1][0]) / 2
    edge_midpoint_lat = (coordinates[0][1] + coordinates[1][1]) / 2
    
    # Calculate distance using the Haversine formula
    R = 6371000  # Earth radius in meters
    
    # Convert to radians
    lat1 = math.radians(center_lat)
    lon1 = math.radians(center_lon)
    lat2 = math.radians(edge_midpoint_lat)
    lon2 = math.radians(edge_midpoint_lon)
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c  # Distance in meters
    
    # Format the center coordinates
    formatted_lat = format_coordinate(center_lat, 'NS')
    formatted_lon = format_coordinate(center_lon, 'EW')
    
    return (formatted_lat, formatted_lon), distance

def format_coordinate(coord, direction):
    """
    Format coordinate in the specified format: "30°5'29.12"N"
    
    Args:
        coord: Decimal degrees coordinate
        direction: 'NS' for latitude, 'EW' for longitude
    
    Returns:
        str: Formatted coordinate string
    """
    is_positive = coord >= 0
    coord = abs(coord)
    
    degrees = int(coord)
    minutes_float = (coord - degrees) * 60
    minutes = int(minutes_float)
    seconds = (minutes_float - minutes) * 60
    
    if direction == 'NS':
        hemisphere = 'N' if is_positive else 'S'
    else:  # 'EW'
        hemisphere = 'E' if is_positive else 'W'
    
    return f"{degrees}°{minutes}'{seconds:.2f}\"{hemisphere}"

def get_center_utm(geojson_path, transformer=None):
    """
    Gets the center of a polygon in UTM coordinates.
    
    Args:
        geojson_path: Path to the GeoJSON file
        transformer: Transformer object. If None, creates a new one.
        
    Returns:
        tuple: (x, y) coordinates in UTM projection (EPSG:32614)
    """
    # Read the GeoJSON file
    with open(geojson_path, 'r') as file:
        data = json.load(file)
    
    # Extract the polygon coordinates
    features = data['features']
    if not features:
        return None
    
    geometry = features[0]['geometry']
    if geometry['type'] != 'Polygon':
        return None
    
    coordinates = geometry['coordinates'][0]  # Get the exterior ring
    
    # Calculate the center by averaging coordinates
    sum_lon = sum(coord[0] for coord in coordinates[:-1])
    sum_lat = sum(coord[1] for coord in coordinates[:-1])
    num_points = len(coordinates) - 1
    
    center_lon = sum_lon / num_points
    center_lat = sum_lat / num_points
    
    # Determine UTM zone number based on longitude
    zone_number = int((center_lon + 180) / 6) + 1
    
    # Determine if northern or southern hemisphere
    north_south = 6 if center_lat >= 0 else 7
    
    # Create the EPSG code for this UTM zone
    # Format: 32[6/7]xx where xx is the zone number and 6=north, 7=south
    epsg_code = f"32{north_south}{zone_number:02d}"
    
    # Create transformer from WGS84 to UTM
    if transformer is None:
        transformer = Transformer.from_crs("EPSG:4326", f"EPSG:{epsg_code}", always_xy=True)
    else:
        # Use the provided transformer
        epsg_code = transformer.target_crs.to_proj4().split(':')[1]
    
    # Transform the coordinates
    x, y = transformer.transform(center_lon, center_lat)
    
    return x, y