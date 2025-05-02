"""
MIT License
"""
import os
import json
import re
import math
import tempfile
from pathlib import Path
from typing import List, Tuple
import shutil

import geopandas as gpd
import folium
import pandas as pd
import numpy as np
from shapely.geometry import Polygon, Point, shape
from shapely.geometry.polygon import orient
import mercantile
import cadquery as cq
from tqdm import tqdm
from OSMPythonTools.overpass import Overpass
from pyproj import Transformer
import pyvista as pv


class OSMDataFetcherCircle:
    """"Fetches OSM data for buildings, amenities, and natural features within a specified radius."""
    
    def __init__(self, dms_lat, dms_lon, radius_meters=1500, cache_dir="cache"):
        """Initializes the OSMDataFetcher with provided latitude, longitude, and radius."""
        self.overpass = Overpass()
        # Parse DMS coordinates to decimal degrees
        self.latitude = self.parse_dms(dms_lat)
        self.longitude = self.parse_dms(dms_lon)
        self.center = Point(self.longitude, self.latitude)
        self.radius_meters = radius_meters
        self.cache_dir = Path(cache_dir).absolute()

        # Create AOI (Area of Interest) Polygon
        self.aoi_polygon = self.create_circle(self.center, self.radius_meters)

        # Create a rectangle around the center point

        # Feature types to fetch (building, amenity, natural)
        self.feature_types = ["building", "amenity", "natural"]

        # Clear the cache directory if it exists
        if self.cache_dir.exists():
            try:
                # Delete only contents, keep the directory
                for item in self.cache_dir.iterdir():
                    if item.is_file():
                        item.unlink()  # Remove files
                    elif item.is_dir():
                        shutil.rmtree(item)  # Remove subdirectories
                print("Cleared existing cache directory")
            except (PermissionError, OSError) as e:
                print(f"Warning: Could not clear cache directory: {e}")
        else:
            # Create cache directory if it doesn't exist
            self.cache_dir.mkdir(parents=True, exist_ok=True)

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

    def create_circle(self, center, radius, num_points=64):
        """Create a circular polygon from a center point and radius."""
        earth_radius = 6378137  # Earth's radius in meters
        lat, lon = center.y, center.x
        angles = [2 * math.pi * i / num_points for i in range(num_points)]
        circle_points = [
            (
                lon + (radius * math.cos(angle) / (earth_radius * math.cos(math.radians(lat)))) * (180 / math.pi),
                lat + (radius * math.sin(angle) / earth_radius) * (180 / math.pi)
            )
            for angle in angles
        ]
        circle_points.append(circle_points[0])
        return Polygon(circle_points)

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


class OSMDataFetcherGeoJSON:
    """Fetches OSM data for buildings, amenities, and natural features within a specified area."""
    def __init__(self, geojson_path, cache_dir="cache"):
        """Initializes the OSMDataFetcher with provided latitude, longitude, and radius."""
        self.overpass = Overpass()
        with open(geojson_path, 'r') as file:
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
        self.cache_dir = Path(cache_dir).absolute()

        # Feature types to fetch (building, amenity, natural)
        self.feature_types = ["building", "amenity", "natural"]

        # Clear the cache directory if it exists
        if self.cache_dir.exists():
            try:
                # Delete only contents, keep the directory
                for item in self.cache_dir.iterdir():
                    if item.is_file():
                        item.unlink()  # Remove files
                    elif item.is_dir():
                        shutil.rmtree(item)  # Remove subdirectories
                print("Cleared existing cache directory")
            except (PermissionError, OSError) as e:
                print(f"Warning: Could not clear cache directory: {e}")
        
        # Create cache directory if it doesn't exist
        self.cache_dir.mkdir(parents=True, exist_ok=True)

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


class MicrosoftBuildingFootprints:
    """Fetches Microsoft Building Footprints within a specified area of interest (AOI)."""
    def __init__(self, aoi_polygon, cache_dir="cache"):
        """Initializes the MicrosoftBuildingFootprints class."""
        self.aoi_polygon = aoi_polygon
        self.cache_dir = Path(cache_dir)

    def download_microsoft_building_footprints(self):
        """Download and filter Microsoft Building Footprints within AOI, or load from cache."""
        msft_output_path = self.cache_dir / "microsoft_footprints.geojson"

        # Check if cached data exists, if so, return it directly
        if msft_output_path.exists():
            print("Loading Microsoft Building Footprints from cache...")
            combined_gdf = gpd.read_file(msft_output_path)
            return combined_gdf, msft_output_path

        # Otherwise, download the data
        print("Downloading Microsoft Building Footprints...")
        aoi_bounds = self.aoi_polygon.bounds
        quad_keys = {mercantile.quadkey(tile) for tile in mercantile.tiles(*aoi_bounds, zooms=9)}

        csv_url = "https://minedbuildings.z5.web.core.windows.net/global-buildings/dataset-links.csv"
        csv_path = self.cache_dir / "dataset-links.csv"

        if not csv_path.exists():
            print("Downloading dataset index...")
            df = pd.read_csv(csv_url, dtype=str)
            df.to_csv(csv_path, index=False)
        else:
            df = pd.read_csv(csv_path, dtype=str)

        quad_urls = df[df["QuadKey"].isin(quad_keys)]["Url"].tolist()
        print(f"The input area spans {len(quad_urls)} tiles.")

        # Merge Microsoft data
        combined_gdf = gpd.GeoDataFrame()
        with tempfile.TemporaryDirectory() as tmpdir:
            for url in tqdm(quad_urls, desc="Downloading Microsoft Footprints"):
                df_msft = pd.read_json(url, lines=True)
                df_msft["geometry"] = df_msft["geometry"].apply(shape)
                gdf_msft = gpd.GeoDataFrame(df_msft, crs="EPSG:4326")
                combined_gdf = pd.concat([combined_gdf, gdf_msft], ignore_index=True)

        # Filter geometries within AOI and save
        combined_gdf = combined_gdf[combined_gdf.geometry.within(self.aoi_polygon)]
        combined_gdf.to_file(msft_output_path, driver="GeoJSON")
        print("Saved Microsoft footprints.")

        return combined_gdf, msft_output_path


class DataMerger:
    """Merges OSM and Microsoft Building Footprints data, removing duplicates."""
    def __init__(self, cache_dir="cache"):
        """Initializes the DataMerger class."""
        self.cache_dir = Path(cache_dir)

    def merge_and_deduplicate_data(self, osm_output_path, msft_output_path):
        """Merge OSM and Microsoft Building Footprints data, removing duplicates."""
        osm_gdf = gpd.read_file(osm_output_path)
        msft_gdf = gpd.read_file(msft_output_path[0])

        # Remove overlapping Microsoft polygons using spatial join
        msft_gdf_cleaned = msft_gdf[~msft_gdf.geometry.intersects(osm_gdf.unary_union)]

        # Check if any Microsoft data was removed (i.e., if there was an intersection)
        if msft_gdf_cleaned.empty:
            print("No Microsoft polygons were removed. Using all Microsoft data.")
            # If no intersection occurred, just use all the Microsoft Footprints data
            merged_gdf = pd.concat([osm_gdf, msft_gdf], ignore_index=True)
        else:
            # Otherwise, proceed with the cleaned data
            print(f"Removed {len(msft_gdf) - len(msft_gdf_cleaned)} Microsoft polygons due to overlap.")
            merged_gdf = pd.concat([osm_gdf, msft_gdf_cleaned], ignore_index=True)

        # Save the merged GeoDataFrame to file (GeoJSON format)
        merged_output_path = self.cache_dir / "merged_polygons.geojson"
        merged_gdf.to_file(merged_output_path, driver="GeoJSON")
        print("Merged dataset saved.")

        return merged_gdf, merged_output_path
    
    def remove_intersecting_msft_data(self, osm_output_path, msft_output_path):
        """Keep only Microsoft Building Footprints that do not intersect with OSM buildings."""
        osm_gdf = gpd.read_file(osm_output_path)
        msft_gdf = gpd.read_file(msft_output_path)

        # Remove overlapping Microsoft polygons
        msft_gdf_filtered = msft_gdf[~msft_gdf.geometry.intersects(osm_gdf.unary_union)]

        print(f"Removed {len(msft_gdf) - len(msft_gdf_filtered)} Microsoft polygons due to intersection.")

        # Save the remaining Microsoft footprints
        msft_filtered_output_path = self.cache_dir / "msft_filtered.geojson"
        msft_gdf_filtered.to_file(msft_filtered_output_path, driver="GeoJSON")
        print(f"Filtered Microsoft dataset saved to {msft_filtered_output_path}")

        return msft_gdf_filtered, msft_filtered_output_path    


class Visualizer:
    """Visualizes OSM and Microsoft Building Footprints data on a Folium map."""
    def __init__(self, latitude, longitude):
        """Initializes the Visualizer class."""
        self.latitude = latitude
        self.longitude = longitude

    def visualize_data(self, data=None, additional_datasets=None, name="merged_and_additional_data_map"):
        """Visualize fetched OSM data and optionally merged data on a Folium map."""
        m = folium.Map(location=[self.latitude, self.longitude], zoom_start=14, tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}", attr="Google Maps")

        # Define a color mapping for natural feature tags
        natural_tag_colors = {
            "wood": "green",
            "water": "blue",
            "sand": "yellow",
            "grass": "lightgreen",
            "scrub": "darkgreen",
            "rock": "gray",
            "mixed": "green",
            "yes": "red",
            # Add more tags as needed
        }
        
        # Visualize merged data (if provided)
        if data is not None:
            # Check if data is a GeoDataFrame
            if hasattr(data, 'iterrows'):
                # Process as a GeoDataFrame
                for _, row in data.iterrows():
                    folium.GeoJson(
                        row["geometry"].__geo_interface__,
                        name="Merged Data",
                        style_function=lambda feature, color="purple": {
                            "fillColor": "purple", "color": "purple", "weight": 1, "fillOpacity": 0.5
                        }
                    ).add_to(m)
            # Check if data is a dictionary
            elif isinstance(data, dict):
                # Process the dictionary data
                for feature_type, gdf in data.items():
                    if hasattr(gdf, 'to_json'):
                        folium.GeoJson(
                            gdf.to_json(),
                            name=f"{feature_type.capitalize()} Data",
                            style_function=lambda feature: {
                                "fillColor": "purple", "color": "purple", "weight": 1, "fillOpacity": 0.5
                            }
                        ).add_to(m)

        # Add additional datasets (if any, e.g., natural and amenity data)
        if additional_datasets:
            for name, dataset in additional_datasets.items():
                if name == 'Natural Features':
                    # For natural features, apply tag-based color mapping with default gray
                    folium.GeoJson(
                        dataset.to_json(),
                        name=name,
                        style_function=lambda feature: {
                            "fillColor": natural_tag_colors.get(
                                list(feature["properties"].get("tags", {}).values())[0], 
                                "gray"  # Default color if the tag is not found
                            ),
                            "color": "black",
                            "weight": 1,
                            "fillOpacity": 0.5
                        }
                    ).add_to(m)
                else:
                    # Default color for non-natural datasets (like amenities)
                    folium.GeoJson(
                        dataset.to_json(),
                        name=name,
                        style_function=lambda feature: {
                            "fillColor": "orange", "color": "orange", "weight": 1, "fillOpacity": 0.5
                        }
                    ).add_to(m)

        folium.LayerControl().add_to(m)
        m.save(f"{name}.html")
        print(f"Map saved as {name}.html")
    
    def visualize_osm_and_msft_data(self, osm_data, msft_data):
        """Visualizes OSM and Microsoft Building Footprints data on the map before merging."""
        m = folium.Map(location=[self.latitude, self.longitude], zoom_start=14, tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}", attr="Google Maps")

        # Check if osm_data and msft_data are GeoDataFrames, not dicts
        if isinstance(osm_data, dict):
            # Access the 'building' data (you can select another type like 'amenity', etc.)
            osm_data = osm_data.get("building")

        if isinstance(msft_data, dict):
            # You should pass the entire GeoDataFrame, not just the URL or file path
            msft_data = gpd.read_file(msft_data)  # If msft_data is a file path or URL

        # Add OSM data to map (example: OSM data color could be blue)
        folium.GeoJson(
            osm_data.to_json(),
            name="OSM Data",
            style_function=lambda feature: {
                "fillColor": "blue", "color": "blue", "weight": 1, "fillOpacity": 0.5
            }
        ).add_to(m)

        # Add Microsoft Building Footprints data to map (example: MSFT data color could be green)
        folium.GeoJson(
            msft_data.to_json(),
            name="Microsoft Footprints",
            style_function=lambda feature: {
                "fillColor": "green", "color": "green", "weight": 1, "fillOpacity": 0.5
            }
        ).add_to(m)

        folium.LayerControl().add_to(m)
        m.save("osm_and_msft_map.html")
        print("Map with OSM and Microsoft data saved as osm_and_msft_map.html")


class GeoJSONToCADConverter:
    """Converts GeoJSON building footprints to CAD format (STEP or STL) using CadQuery."""
    def __init__(self, geojson_path: str, buildings_geojson_path: str, default_height: float = 5.0, extrude_height: float = 0.0):
        """
        Initialize the converter with a GeoJSON file path and default height.
        
        :param geojson_path:: Path to the input GeoJSON file
        :param buildings_geojson_path: Path to the buildings GeoJSON file
        :param default_height: Height to use when no height is specified (default 5.0)
        """
        self.default_height = default_height
        self.extrude_height = extrude_height
        self.geojson_path = geojson_path
        self.buildings_geojson_path = buildings_geojson_path
        
        # Read the GeoJSON file
        with open(buildings_geojson_path, 'r', encoding='utf-8') as f:
            self.geojson_data = json.load(f)
        
        # Create output directory if it doesn't exist
        self.output_dir = Path('building_models')

        # # Clear the output directory if it exists
        # if self.output_dir.exists():
        #     try:
        #         # Remove directory and all its contents
        #         shutil.rmtree(self.output_dir)
        #         print(f"Removed existing {self.output_dir} directory")
        #     except (PermissionError, OSError) as e:
        #         print(f"Warning: Could not remove output directory: {e}")

        # Create fresh output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # # Create coordinate transformer (assuming UTM zone 14N for Austin, Texas)
        # self.transformer = Transformer.from_crs("EPSG:4326", "EPSG:32614", always_xy=True)
    
    # def _convert_coordinates(self, lon: float, lat: float) -> Tuple[float, float]:
    #     """ Convert longitude and latitude to meters using UTM projection. """
    #     return self.transformer.transform(lon, lat)

    def _convert_coordinates(self, lon: float, lat: float) -> Tuple[float, float]:
        """Convert longitude and latitude to meters using UTM projection."""
        # Determine UTM zone number based on longitude
        zone_number = int((lon + 180) / 6) + 1
        
        # Determine if northern or southern hemisphere
        north_south = 6 if lat >= 0 else 7
        
        # Create the EPSG code for this UTM zone
        # Format: 32[6/7]xx where xx is the zone number and 6=north, 7=south
        epsg_code = f"32{north_south}{zone_number:02d}"
        
        # Create transformer from WGS84 to UTM
        transformer = Transformer.from_crs("EPSG:4326", f"EPSG:{epsg_code}", always_xy=True)
        
        # Transform the coordinates
        x, y = transformer.transform(lon, lat)
        return x, y
        
    def _extract_coordinates(self, feature: dict) -> List[Tuple[float, float]]:
        """ Extract and convert 2D coordinates from a GeoJSON feature. """
        orig_coords = feature['geometry']['coordinates'][0]
        return [self._convert_coordinates(lon, lat) for lon, lat in orig_coords]
    
    def _get_height(self, feature: dict) -> float:
        """ Get height for a feature, using default if not specified. """
        tags = feature['properties'].get('tags', {})
        return float(tags.get('height', self.default_height)) + self.extrude_height

    def convert_to_step(self):
        """ Convert GeoJSON features to STEP files using CadQuery. """
        for idx, feature in enumerate(self.geojson_data.get('features', []), 1):
            if feature['properties'].get('tags', {}).get('building') is None:
                continue
            
            coords = self._extract_coordinates(feature)
            height = self._get_height(feature)
            
            poly = Polygon(coords)
            step_filename = os.path.join(self.output_dir, f'building_{idx}.step')
            self._create_3d_model(poly, height, step_filename, file_format='STEP')
            print(f"Generated STEP file for building {idx}: {step_filename}")
    
    def convert_to_stl(self):
        """ Convert GeoJSON features to STL files using CadQuery. """
        for idx, feature in enumerate(self.geojson_data.get('features', []), 1):
            if feature['properties'].get('tags', {}).get('building') is None:
                continue
            
            coords = self._extract_coordinates(feature)
            height = self._get_height(feature)
            
            poly = Polygon(coords)
            stl_filename = os.path.join(self.output_dir, f'building_{idx}.stl')
            self._create_3d_model(poly, height, stl_filename, file_format='STL')
            print(f"Generated STL file for building {idx}: {stl_filename}")
    
    def _create_3d_model(self, polygon: Polygon, height: float, output_path: str, file_format: str):
        """ Generate a 3D model file (STEP or STL) from a polygon and height using CadQuery. """
        polygon = orient(polygon, sign=1.0)
        base_points = np.array(polygon.exterior.coords)
        
        # Create a 3D extrusion using CadQuery
        workplane = cq.Workplane("XY").polyline(base_points.tolist()).close().extrude(height)
        
        # Export to specified file format
        if file_format == 'STEP':
            cq.exporters.export(workplane, output_path)
        elif file_format == 'STL':
            cq.exporters.export(workplane, output_path, exportType='STL')


class MoveCADToTerrain(GeoJSONToCADConverter):
    """Moves CAD models to terrain using PyVista for STL files."""
    
    def __init__(self, geojson_path: str, buildings_geojson_path: str, default_height: float = 5.0, extrude_height: float = 0.0):
        """Initializes the MoveCADToTerrain class as a child of GeoJSONToCADConverter."""
        super().__init__(geojson_path, buildings_geojson_path, default_height, extrude_height)
        
        self.geojson_path = geojson_path
        self.buildings_geojson_path = buildings_geojson_path
        
        building_models = [
            os.path.join(self.output_dir, f) for f in os.listdir(self.output_dir) if f.endswith('.stl')
        ]
        self.stl_paths = building_models
        
        
        # get the terrain path from the lidar_data folder
        lidar_data_dir = Path("lidar_data")
        if not lidar_data_dir.exists():
            self.terrain_path=None
        else:
            self.terrain_path = f"{self.geojson_path.split('.')[0]}_DEM_trn.stl"
            if not Path(self.terrain_path).exists():
                print(f"Terrain file not found at {self.terrain_path}.")
                self.terrain_path = None
                # stop the program if terrain file is not found
                return False
            
            self.output_dir = Path('placed_buildings')

            # Create output directory if it doesn't exist
            if not self.output_dir.exists():
                self.output_dir.mkdir(parents=True, exist_ok=True)

            self.extrude_height = extrude_height

    def import_stl_and_find_base_center(self, stl_path):
        """
        Import an STL file using PyVista and find the center of its base.
        
        Returns:
            tuple: (mesh, base_center) where base_center is (x, y, z) coordinates
        """
        # Import STL file
        mesh = pv.read(stl_path)
        
        # Get bounds of the mesh (min and max along each axis)
        bounds = mesh.bounds
        x_min, y_min, z_min = bounds[0], bounds[2], bounds[4]
        x_max, y_max, z_max = bounds[1], bounds[3], bounds[5]
        
        # The base center is at the middle of the X-Y plane at minimum Z
        base_center = [(x_min + x_max) / 2, (y_min + y_max) / 2, z_min]
        
        return mesh, base_center
    
    def find_terrain_height_at_point(self, terrain_mesh, x, y):
        """
        Find the height of the terrain at a given X,Y point using ray tracing.
        
        Args:
            terrain_mesh: PyVista mesh of the terrain
            x, y: Coordinates in the X-Y plane
            
        Returns:
            float: Z coordinate where a vertical line through (x,y) intersects terrain
        """
        # Define a ray starting high above the point and projecting downward
        start_point = [x, y, 1000.0]  # Start from high above
        end_point = [x, y, -1000.0]   # End below the terrain
        
        # Perform ray-tracing to find intersection with terrain
        intersections = terrain_mesh.ray_trace(start_point, end_point)
        
        if intersections[0].size > 0:
            # Return Z coordinate of the first intersection
            return intersections[0][0][2]
        else:
            print(f"Warning: No terrain intersection found at ({x}, {y})")
            return 0.0  # Default height if no intersection found
    
    def move_cad_to_terrain(self):
        """Place each building model on the terrain at the appropriate position."""
        # Import terrain mesh
        if self.terrain_path is None:
            print("No terrain file found.")
            return False
        else:
            print(f"Using terrain file: {self.terrain_path}")
            terrain_mesh = pv.read(self.terrain_path)
            
            for stl_path in self.stl_paths:
                # Import building and find its base center
                building_mesh, base_center = self.import_stl_and_find_base_center(stl_path)
                x, y, base_z = base_center
                
                # Find terrain height at building position
                terrain_z = self.find_terrain_height_at_point(terrain_mesh, x, y)
                
                # Calculate required Z translation to place building on terrain
                z_translation = terrain_z - base_z - self.extrude_height
                
                # Translate building mesh
                translated_mesh = building_mesh.translate([0, 0, z_translation])
                
                # Save the placed building
                output_path = self.output_dir / f"{Path(stl_path).stem}_placed.stl"
                translated_mesh.save(str(output_path))
                print(f"Placed building saved as {output_path}")
            
            return print("All buildings placed on terrain successfully.")