import geopy.distance
import geojson
from shapely.geometry import Point

# Center point (longitude, latitude)
center_lon = 12.394610000000966
center_lat = 55.681900829282256

# Radius in meters
radius = 500

# Calculate the north and south latitudes
north = geopy.distance.distance(meters=radius).destination((center_lat, center_lon), bearing=0)
north_lat = north.latitude

south = geopy.distance.distance(meters=radius).destination((center_lat, center_lon), bearing=180)
south_lat = south.latitude

# Calculate the east and west longitudes
east = geopy.distance.distance(meters=radius).destination((center_lat, center_lon), bearing=90)
east_lon = east.longitude

west = geopy.distance.distance(meters=radius).destination((center_lat, center_lon), bearing=270)
west_lon = west.longitude

# Create rectangle vertices (going clockwise: NE, SE, SW, NW, NE to close the polygon)
rectangle_coords = [
    [east_lon, north_lat],   # Northeast
    [east_lon, south_lat],   # Southeast
    [west_lon, south_lat],   # Southwest
    [west_lon, north_lat],   # Northwest
    [east_lon, north_lat]    # Back to Northeast to close the polygon
]

# Create GeoJSON polygon for rectangle
rectangle_polygon = geojson.Polygon([rectangle_coords])
rectangle_feature = geojson.Feature(geometry=rectangle_polygon, properties={
    "type": "rectangle",
    "center": [center_lon, center_lat],
    "radius_meters": radius
})

# Write rectangle to file
rectangle_output_file = f"rectangle_{radius}m.geojson"
with open(rectangle_output_file, 'w') as f:
    geojson.dump(geojson.FeatureCollection([rectangle_feature]), f, indent=2)

print(f"GeoJSON rectangle created and saved to {rectangle_output_file}")

# Create a circular polygon using shapely
center_point = Point(center_lon, center_lat)
circle_polygon = center_point.buffer(radius / 111320)  # Approximation: 1 degree ≈ 111.32 km
circle_coords = [[x, y] for x, y in circle_polygon.exterior.coords]

# Create GeoJSON polygon for circle
circle_geojson_polygon = geojson.Polygon([circle_coords])
circle_feature = geojson.Feature(geometry=circle_geojson_polygon, properties={
    "type": "circle",
    "center": [center_lon, center_lat],
    "radius_meters": radius
})

# Write circle to file
circle_output_file = f"circle_{radius}m.geojson"
with open(circle_output_file, 'w') as f:
    geojson.dump(geojson.FeatureCollection([circle_feature]), f, indent=2)

print(f"GeoJSON circle created and saved to {circle_output_file}")