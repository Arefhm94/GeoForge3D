""" This script fetches OSM data, Microsoft building footprints, merges them, and converts them to CAD format."""
import sys

from MapDataFetcher import OSMDataFetcherGeoJSON, MicrosoftBuildingFootprints, DataMerger, Visualizer, GeoJSONToCADConverter, MoveCADToTerrain


# Get the GeoJSON path from command-line argument if provided
if len(sys.argv) > 1:
    GEOJSON_PATH = sys.argv[1]
else:
    # Fallback to default path if no argument is provided
    GEOJSON_PATH = r"xwxw.geojson"
    print("No GeoJSON path provided as argument, using default:", GEOJSON_PATH)

# Step 1: Initialize OSMDataFetcher with the coordinates and radius
osm_fetcher = OSMDataFetcherGeoJSON(geojson_path=GEOJSON_PATH)

# Step 2: Fetch the OSM data for building, amenity, and natural features
osm_data = osm_fetcher.fetch_osm_data()

# Step 3: Initialize MicrosoftBuildingFootprints with the AOI polygon
msft_fetcher = MicrosoftBuildingFootprints(osm_fetcher.aoi_polygon)

# Step 4: Download Microsoft building footprints within the AOI
msft_data, msft_output_path = msft_fetcher.download_microsoft_building_footprints()

# Step 5: Merge and deduplicate the OSM and Microsoft data
data_merger = DataMerger()
merged_data, merged_output_path = data_merger.merge_and_deduplicate_data(
    osm_output_path=osm_fetcher.cache_dir / r"osm_building.geojson",  # Assuming this file exists
    msft_output_path=[msft_output_path]
)

# Step 6: Initialize the Visualizer and visualize the data
visualizer = Visualizer(osm_fetcher.latitude, osm_fetcher.longitude)

# You can visualize the individual OSM features and the merged data
visualizer.visualize_data(
    data=osm_data,  # OSM data (building, amenity, and natural)
)

model = GeoJSONToCADConverter(geojson_path=GEOJSON_PATH, buildings_geojson_path=r"cache/osm_building.geojson", extrude_height=5.0)

# model.convert_to_step()
model.convert_to_stl()

# Move the CAD model to the terrain
move_cad = MoveCADToTerrain(geojson_path=GEOJSON_PATH, buildings_geojson_path=r"cache/osm_building.geojson")
move_cad.move_cad_to_terrain()
