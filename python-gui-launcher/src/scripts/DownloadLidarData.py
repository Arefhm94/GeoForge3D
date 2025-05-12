import os
import json
import requests
import numpy as np
import geopandas as gpd
from tqdm import tqdm
import rioxarray as rxr
import earthpy.plot as ep
import matplotlib.pyplot as plt
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class DownloadLidarData():
    
    def __init__(self, geojson_path, output_dir):
        self.geojson_path = geojson_path
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        self.output_dir = os.path.abspath(output_dir)
        self.tnm_api_url = "https://tnmaccess.nationalmap.gov/api/v1/products"
    
    
    def load_geojson(self):
        """Load GeoJSON data from file and parse it"""
        gdf = gpd.read_file(self.geojson_path)
        return gdf
    
    
    def bbox(self):
        """Get the bounding box of the GeoJSON data"""
        gdf = self.load_geojson()
        
        # Get the bounding box of the GeoJSON data
        bbox = gdf.total_bounds
        print(f"Bounding box: \n{bbox}")
        
        # Get the boundary coordinates of the GeoJSON data
        geometry = gdf.geometry.iloc[0]
        # Check if it's a Polygon or MultiPolygon
        if geometry.geom_type == 'Polygon':
            boundary_coords = np.array(geometry.exterior.coords)

        elif geometry.geom_type == 'MultiPolygon':
            # Extract boundaries from all polygons in the MultiPolygon
            boundary_coords = [np.array(polygon.exterior.coords) for polygon in geometry.geoms]
        
        print(f"Boundary coordinates: \n{boundary_coords}")
        
        return bbox, boundary_coords
    
    
    def show_data_as_html(self, data):
        """Save JSON response data as an HTML file and open it in a browser."""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Lidar Query Data Results</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                pre {{ background: #f4f4f4; padding: 10px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <h1>LiDAR Data Query Results</h1>
            <pre>{json.dumps(data, indent=2)}</pre>
        </body>
        </html>
        """

        html_path = os.path.join(self.output_dir, "lidar_data_query.html")
        with open(html_path, "w", encoding="utf-8") as file:
            file.write(html_content)

        print(f"HTML file saved at: {html_path}")
        
        # Automatically open in a web browser (optional)
        # import webbrowser
        # webbrowser.open("file://" + os.path.abspath(html_path))
    
    
    def download_request_tqdm(self, mode="lidar"):
        
        _bbox, _ = self.bbox()
        minx, miny, maxx, maxy = _bbox
        
        params = {
            "bbox": f"{minx},{miny},{maxx},{maxy}",  # Correct format
            "prodFormats": "LAS,LAZ",  # Ensure correct filtering
            "outputFormat": "JSON"
        }
        
        print(f"Downloading lidar data for bounding box: {params['bbox']} from {self.tnm_api_url}")
        response = requests.get(self.tnm_api_url, params=params)

        if response.status_code != 200:
            print(f"Error: API returned status code {response.status_code}")
            print(response.text)
            return []
    
        data = response.json()
        self.show_data_as_html(data)

        if 'items' not in data or len(data['items']) == 0:
            print("No data found for the specified area. The area might not have any datasets available.")
            print("Try using a slightly larger bounding box.")
            return []
        
        print(f"Found {len(data['items'])} total datasets.")
        
        downloaded_files = []
        for i, item in enumerate(data['items']):
            try:
                download_url = item["downloadLazURL"] if mode in ["lidar", "l"] else item["previewGraphicURL"]
                title = item.get('title', f"lidar_data_{i+1}")
                
                if not download_url:
                    print(f"No download URL found for {title}. Skipping.")
                    continue

                # Assuming download_url is already defined
                filename = download_url.split("/")[-1].strip()

                # Ensure there are no unwanted characters, like spaces or special symbols
                filename = filename.replace(" ", "_")

                # Combine the output directory and filename
                output_file = os.path.join(self.output_dir, f"{filename}")
                
                session = requests.Session()
                adapter = requests.adapters.HTTPAdapter(max_retries=5)
                session.mount("https://", adapter)

                with session.get(download_url, stream=True, timeout=60) as r:
                    r.raise_for_status()
                    total_size = int(r.headers.get('content-length', 0))
                    
                    with open(output_file, 'wb') as f, tqdm(
                        total=total_size, unit_scale=True, 
                        desc=f"Dataset {i+1}/{len(data['items'])}"
                    ) as pbar:
                        for chunk in r.iter_content(chunk_size=4096):
                            if chunk:  # Filter out keep-alive new chunks
                                f.write(chunk)
                                pbar.update(len(chunk))

                downloaded_files.append(output_file)
                print(f"Successfully downloaded to {output_file}")
            except Exception as e:
                print(f"Error downloading {item.get('title', 'dataset')}: {str(e)}")
        
        return downloaded_files


    def download_request(self, mode="lidar"):
        
        _bbox, _ = self.bbox()
        minx, miny, maxx, maxy = _bbox
        
        params = {
            "bbox": f"{minx},{miny},{maxx},{maxy}",  # Correct format
            "prodFormats": "LAS,LAZ",  # Ensure correct filtering
            "outputFormat": "JSON"
        }
        
        print(f"Downloading lidar data for bounding box: {params['bbox']} from {self.tnm_api_url}")
        response = requests.get(self.tnm_api_url, params=params)

        if response.status_code != 200:
            print(f"Error: API returned status code {response.status_code}")
            print(response.text)
            return []
    
        data = response.json()
        self.show_data_as_html(data)

        if 'items' not in data or len(data['items']) == 0:
            print("No data found for the specified area. The area might not have any datasets available.")
            print("Try using a slightly larger bounding box.")
            return []
        
        print(f"Found {len(data['items'])} total datasets.")
        
        downloaded_files = []
        for i, item in enumerate(data['items']):
            try:
                download_url = item["downloadLazURL"] if mode in ["lidar", "l"] else item["previewGraphicURL"]
                title = item.get('title', f"lidar_data_{i+1}")
                
                if not download_url:
                    print(f"No download URL found for {title}. Skipping.")
                    continue

                # Assuming download_url is already defined
                filename = download_url.split("/")[-1].strip()

                # Ensure there are no unwanted characters, like spaces or special symbols
                filename = filename.replace(" ", "_")

                # Combine the output directory and filename
                output_file = os.path.join(self.output_dir, f"{filename}")
                
                # Setup retry strategy
                session = requests.Session()
                retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
                adapter = HTTPAdapter(max_retries=retries)
                session.mount("https://", adapter)

                with session.get(download_url, stream=True, timeout=120) as r:
                    r.raise_for_status()

                    # Save the entire file without using chunks
                    with open(output_file, 'wb') as f:
                        f.write(r.content)

                downloaded_files.append(output_file)
                print(f"Successfully downloaded to {output_file}")
            except Exception as e:
                print(f"Error downloading {item.get('title', 'dataset')}: {str(e)}")
        
        return downloaded_files


    def gpxz(self, plot=True):
        # Prepare output file path
        output_filename = os.path.splitext(os.path.basename(self.geojson_path))[0]
        output_path = os.path.join(self.output_dir, f"{output_filename}_DEM.tif")
        
        # if os.path.exists(output_path):
        #     return print(f"LiDAR data already downloaded as '{output_filename}_DEM.tif'")
        
        # Define the API URL
        url = "https://api.gpxz.io/v1/elevation/hires-raster"

        _bbox, _ = self.bbox()
        # Define bounding box and resolution
        params = {
            "res_m": 1,  # Resolution in meters
            "bbox_left": _bbox[0],
            "bbox_right": _bbox[2],
            "bbox_bottom": _bbox[1],
            "bbox_top": _bbox[3],
            "api-key": "ak_n6mAFtFp_1FRttWTDravQciiP"
        }

        # Make the request
        response = requests.get(url, params=params)
        
        # Check response status
        if response.status_code == 200:
            # Save the data as a GeoTIFF file
            with open(output_path, "wb") as file:
                file.write(response.content)
            print(f"LiDAR data downloaded successfully as '{output_filename}_DEM.tif'")
        else:
            print("Error:", response.status_code, response.text)
        
        if plot:
            self.show_raster()


    def show_raster(self):
        # Prepare output file path
        output_filename = os.path.splitext(os.path.basename(self.geojson_path))[0]
        output_path = os.path.join(self.output_dir, f"{output_filename}_DEM.tif")

        raster = rxr.open_rasterio(output_path, masked=True)

        ep.plot_bands(
        arr=raster,
        cmap="RdYlGn",
        figsize=(8, 8),
        title="Lidar DEM using IDW"
        )

        plt.show()