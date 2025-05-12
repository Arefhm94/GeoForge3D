from shapely.geometry import box
import geopandas as gpd

class BuildingExtractionService:
    def __init__(self, map_data_source):
        self.map_data_source = map_data_source

    def extract_buildings(self, rectangle):
        min_x, min_y, max_x, max_y = rectangle.bounds
        query_box = box(min_x, min_y, max_x, max_y)

        # Load the map data (assuming it's in GeoDataFrame format)
        gdf = gpd.read_file(self.map_data_source)

        # Filter buildings within the rectangle
        buildings_within_rectangle = gdf[gdf.geometry.intersects(query_box)]

        return buildings_within_rectangle

    def export_to_geojson(self, buildings):
        return buildings.to_json()