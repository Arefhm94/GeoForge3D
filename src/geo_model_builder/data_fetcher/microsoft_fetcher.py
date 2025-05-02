"""MST Data Fetcher for Building, Amenity, and Natural Features
"""
import mercantile
import tempfile
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import shape
from tqdm import tqdm


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
