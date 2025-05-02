"""OSM Data Fetcher for Building, Amenity, and Natural Features
"""
import os
import json
import re

from pathlib import Path
import geopandas as gpd
from shapely.geometry import Polygon
from OSMPythonTools.overpass import Overpass


class OSMDataFetcher:
    """
    Fetch OpenStreetMap (OSM) data for building, amenity, and natural features.
    """
    
    def __init__(self, geojson_path):
        """Initializes the OSMDataFetcher with provided latitude, longitude, and radius."""
        self.overpass = Overpass()
        with open(geojson_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Create the AOI polygon from the GeoJSON file
        features = data['features']
        if not features:
            raise ValueError("No features found in the GeoJSON file.")
        geometry = features[0]['geometry']
        if geometry['type'] != 'Polygon':
            raise ValueError("Geometry type is not Polygon.")

        coordinates = geometry['coordinates'][0]  # Get the exterior ring
        self.aoi_polygon = Polygon(coordinates)
        self.latitude = self.aoi_polygon.centroid.y
        self.longitude = self.aoi_polygon.centroid.x

        # Feature types to fetch (building, amenity, natural)
        self.feature_types = ["building", "amenity", "natural"]

        # Check if in the data_storage directory, download folder exists
        os.path = Path(__file__).resolve().parent.parent.parent.parent
        self.data_storage = os.path / "data_storage"
        self.download_folder = self.data_storage / "download"

    def dms_to_decimal(self, degrees, minutes, seconds, direction):
        """Convert DMS (Degrees, Minutes, Seconds) to Decimal Degrees."""
        decimal = degrees + (minutes / 60) + (seconds / 3600)
        return -decimal if direction in ['S', 'W'] else decimal

    def parse_dms(self, dms_str):
        """Parse DMS string (e.g. 38°24'7.97"N) into decimal degrees."""
        match = re.match(r"(\d+)°(\d+)'(\d+(?:\.\d+)?)\"([NSEW])", dms_str)
        if not match:
            raise ValueError("Invalid DMS format")
        return self.dms_to_decimal(*map(float, match.groups()[:-1]), match.group(4))

    def get_osm_data(self, feature_type):
        """Fetch OSM data for a given feature type."""
        poly_coords = " ".join(f"{lat} {lon}" for lon, lat in self.aoi_polygon.exterior.coords)
        query = f'(way["{feature_type}"](poly:"{poly_coords}");); (._;>;); out body;'
        response = self.overpass.query(query, timeout=120)
        elements = response.toJSON().get("elements", [])
        
        if not elements:
            print(f"No {feature_type} data found in the area.")
            return None
        else:
            node_coords = {e["id"]: (e["lon"], e["lat"]) for e in elements if e["type"] in ["node"]}

            features = []
            for element in elements:
                if element.get("type") == "way" or "nodes" in element:
                    try:
                        coords = [node_coords[node_id] for node_id in element["nodes"]]
                        # Create a Polygon geometry for the building (or other feature)
                        features.append({"geometry": Polygon(coords), "tags": element.get("tags", {})})
                    except KeyError:
                        continue  # Skip incomplete data

            # Explicitly create a GeoDataFrame with the 'geometry' column
            gdf = gpd.GeoDataFrame(features, geometry="geometry", crs="EPSG:4326")
            return gdf

    def fetch_osm_data(self):
        """Fetch OSM data for all feature types (building, amenity, natural)."""
        datasets = {feature: self.get_osm_data(feature) for feature in self.feature_types}

        if datasets is None:
            print("No data found for the given feature types.")
            return None
        else:
            # Save Data as GeoJSON
            for feature, data in datasets.items():
                if feature in ["amenity", "natural"]:
                    return None
                else:
                    filename = self.cache_dir / f"osm_{feature}.geojson"
                    data.to_file(filename, driver="GeoJSON")
                    print(f"Saved: {filename}")

            return datasets
