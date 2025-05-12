import os
from DownloadLidarData import DownloadLidarData
from TerrainToMesh import TifToMesh
import functions as fc
import sys

def main():
    # Download LiDAR data
    output_dir = "lidar_data"
    if len(sys.argv) > 1:
        geojson_path = sys.argv[1]
    else:
        # Fallback to default path if no argument is provided
        geojson_path = "test.geojson"
        print("No GeoJSON path provided as argument, using default:", geojson_path)

    case = DownloadLidarData(geojson_path=geojson_path, output_dir=output_dir)
    case.bbox()

    # Download DEM using GPXZ, 100 requests per day limit
    case.gpxz()
    # case.show_raster()
    
    # Create mesh from TIF
    tif_path = os.path.join(output_dir, geojson_path.split('/')[-1].split('.')[0] + '_DEM.tif')
    output_dir = r'lidar_data'
    
    # Create TifToMesh instance
    mesh = TifToMesh(tif_path, output_dir, fc.get_center_utm(geojson_path))
    
    # Load TIF
    mesh.load_tif()
    
    # Create adaptive TIN
    mesh.create_adaptive_tin(sample_ratio=0.5)
    
    # Visualize sampling
    mesh.visualize(show=False)
    
    # # Export mesh
    mesh.export_tin(format='stl')
    
    # Get mesh information
    mesh.generate_mesh_info()

    # Create TRN with PyVista
    mesh.create_trn(pixel_to_triangle_ratio=0.5)

if __name__ == "__main__":
    main()
