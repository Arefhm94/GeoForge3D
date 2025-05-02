import os
import numpy as np
import rasterio
import matplotlib.pyplot as plt
import cv2
import trimesh
import pyvista as pv
from scipy.spatial import Delaunay
import matplotlib.gridspec as gridspec

class TifToMesh:
    def __init__(self, tif_path, output_dir, geocenter):
        """
        Initialize the TifToMesh class.
        Parameters:
        -----------
        tif_path : str
            Path to the input GeoTIFF file
        output_dir : str
            Directory to save output files
        """
        self.tif_path   = tif_path
        self.output_dir = output_dir
        self.geocenter  = geocenter

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Attributes to store processed data
        self.raster_data  = None
        self.data         = None
        self.mesh         = None
        self.geotransform = None
        self.crs          = None

    def load_tif(self, band_index=1):
        """
        Load GeoTIFF file and extract raster data.
        
        Parameters:
        -----------
        band_index : int, optional
            Index of the band to process (default is 1)
        """
        with rasterio.open(self.tif_path) as src:
            # Read specified band
            self.raster_data = src.read(band_index)
            
            # Squeeze to remove band dimension if present
            if self.raster_data.ndim > 2:
                self.raster_data = self.raster_data.squeeze()

            # Store geospatial metadata
            self.geotransform = src.transform
            self.crs = src.crs

    def check_raster_loaded(self):
        """Helper function to check if raster data is loaded."""
        if self.raster_data is None:
            raise ValueError("Raster data not loaded. Call load_tif() first.")

    def detect_terrain_complexity(self):
        """
        Detect areas of terrain complexity using edge detection and variance.
        
        Returns:
        --------
        numpy.ndarray
            Complexity map highlighting areas of significant elevation change
        """
        self.check_raster_loaded()
        
        # Compute gradient magnitude to detect terrain changes
        sobelx = cv2.Sobel(self.raster_data.astype(np.float32), cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(self.raster_data.astype(np.float32), cv2.CV_64F, 0, 1, ksize=3)
        
        # Compute gradient magnitude
        gradient_magnitude = np.sqrt(sobelx**2 + sobely**2)
        
        # Compute local variance as another complexity measure
        variance = self.local_variance(self.raster_data)
        
        # Combine gradient and variance for complexity detection
        complexity = (gradient_magnitude + variance) / 2
        
        # Normalize complexity
        complexity = (complexity - complexity.min()) / (complexity.max() - complexity.min())
        
        return complexity

    def local_variance(self, img, kernel_size=5):
        """
        Compute the local variance of the image using a moving kernel.
        
        Parameters:
        -----------
        img : numpy.ndarray
            The image data for which to compute the variance
        kernel_size : int, optional
            Size of the moving kernel (default is 5)
        
        Returns:
        --------
        numpy.ndarray
            Local variance of the image
        """
        kernel = np.ones((kernel_size, kernel_size)) / (kernel_size**2)
        mean = cv2.filter2D(img, -1, kernel)
        variance = cv2.filter2D((img - mean)**2, -1, kernel)
        return variance

    def adaptive_sampling(self, complexity_map, sample_ratio=0.2, min_samples=100, max_samples=int(1e6)):
        """0
        Perform adaptive sampling based on terrain complexity, 
        ensuring ALL edge points are always sampled.
        
        Parameters:
        -----------
        complexity_map : numpy.ndarray
            Complexity map from detect_terrain_complexity()
        sample_ratio : float, optional
            Proportion of pixels to sample (default: 0.2)
        min_samples : int, optional
            Minimum number of samples (default: 100)
        max_samples : int, optional
            Maximum number of samples (default: 10000)
        
        Returns:
        --------
        tuple
            Sampled points and their corresponding values
        """
        # Get raster dimensions
        rows, cols = complexity_map.shape
        
        # Verify raster_data shape matches complexity_map
        if self.raster_data.shape != complexity_map.shape:
            raise ValueError(f"Raster data shape {self.raster_data.shape} does not match complexity map shape {complexity_map.shape}")
        
        # Flatten complexity map
        flat_complexity = complexity_map.ravel()
        
        # Compute number of samples (subtract points we'll explicitly add)
        total_pixels = complexity_map.size
        num_samples = max(min_samples, 
                        min(max_samples, int(total_pixels * sample_ratio) - 12))
        
        # Normalize probabilities
        probabilities = flat_complexity / flat_complexity.sum()
        
        # Explicitly capture ALL edge points
        edge_points = np.array([
            # Top edge (including corners)
            [0, 0],           # Top-left
            [0, cols-1],      # Top-right
            
            # Bottom edge (including corners)
            [rows-1, 0],      # Bottom-left
            [rows-1, cols-1], # Bottom-right
            
            # Additional full edge points
            [0, cols//4],     # Top 1/4
            [0, cols//2],     # Top middle
            [0, 3*cols//4],   # Top 3/4
            
            [rows-1, cols//4],     # Bottom 1/4
            [rows-1, cols//2],     # Bottom middle
            [rows-1, 3*cols//4],   # Bottom 3/4
            
            [rows//4, 0],     # Left 1/4
            [rows//2, 0],     # Left middle
            [3*rows//4, 0]    # Left 3/4
        ])
        
        # Sample additional indices based on complexity
        sampled_indices = np.random.choice(
            total_pixels, 
            size=num_samples, 
            p=probabilities, 
            replace=False
        )
        
        # Convert flat indices to 2D coordinates
        sampled_points = np.column_stack([ 
            sampled_indices % cols,    # x coordinates
            sampled_indices // cols    # y coordinates
        ])
        
        # Combine edge points with additional sampled points
        final_sampled_points = np.vstack((edge_points, sampled_points))
        
        # Remove any potential duplicates
        final_sampled_points = np.unique(final_sampled_points, axis=0)
        
        # Clamp points to ensure they are within bounds
        final_sampled_points = np.clip(final_sampled_points, 
                                        [0, 0], 
                                        [cols-1, rows-1])
        
        # Get corresponding values
        sampled_values = self.raster_data[ 
            final_sampled_points[:, 1], 
            final_sampled_points[:, 0]
        ]
        
        return final_sampled_points, sampled_values

    def create_adaptive_tin(self, sample_ratio=0.2):
        """
        Create an adaptive Triangulated Irregular Network.
        
        Parameters:
        -----------
        sample_ratio : float, optional
            Proportion of pixels to sample (default: 0.2). 
            Note: Higher values will lead to longer processing times.
            But, it will provide a more detailed TIN.
        
        Returns:
        --------
        dict
            TIN data with adaptive sampling
        """
        
        self.check_raster_loaded()
        
        # Detect terrain complexity
        complexity_map = self.detect_terrain_complexity()
        
        # Perform adaptive sampling
        points, values = self.adaptive_sampling(complexity_map, sample_ratio)
        
        # Remove invalid points
        valid_mask = ~np.isnan(values) & (values >= 0)
        points = points[valid_mask]
        values = values[valid_mask]
        
        # Store TIN data
        self.data = {
            'points': points,
            'values': values
        }
        
        return self.data

    def export_tin(self, format='stl', normalized=False):
        """
        Export the Triangulated Irregular Network to a mesh file.
        
        Parameters:
        -----------
        format : str, optional
            Output file format (obj, stl, ply, etc.) (default is 'stl')
        normalized : bool, optional
            Normalize elevation values (default is False)
        
        Returns:
        --------
        trimesh.Trimesh
            Exported mesh object
        """
        self.check_tin_data()
        
        # Prepare vertices and faces
        points = self.data['points']
        values = self.data['values']
        
        # Create 3D vertices by adding z-coordinate (elevation)
        if normalized:
            # Normalize elevation to [0, 1] range
            values = (values - values.min()) / (values.max() - values.min())
        
        # Create 3D vertices (x, y, elevation)
        vertices = np.column_stack([ 
            points, 
            values
        ])
        
        # Flip Y-coordinates by subtracting from the max Y value
        max_y = self.raster_data.shape[0]  # Max row index
        vertices[:, 1] = max_y - vertices[:, 1]
        
        # Use Delaunay triangulation to create faces
        triangulation = Delaunay(points)
        faces = triangulation.simplices
        
        # Create mesh using trimesh
        self.mesh = trimesh.Trimesh(
            vertices=vertices,
            faces=faces
        )
        
        # Transfer mesh to geocenter if specified
        if self.geocenter is not None:
            # Calculate current centroid
            current_centroid = self.mesh.centroid
            
            # Create translation vector
            translation_vector = np.concatenate((np.array(self.geocenter), [current_centroid[2]])) - current_centroid
            
            # Translate vertices
            self.mesh.vertices += translation_vector

        # Prepare output file path
        output_filename = os.path.splitext(os.path.basename(self.tif_path))[0]
        output_path = os.path.join(self.output_dir, f"{output_filename}_tin.{format}")
        
        # Export mesh
        self.mesh.export(output_path)
        
        print(f"Mesh exported to {output_path}")
        
        return self.mesh

    def check_tin_data(self):
        """Helper function to check if TIN data is available."""
        if self.data is None:
            raise ValueError("TIN not created. Call create_adaptive_tin() first.")

    def create_trn(self, pixel_to_triangle_ratio=1):
        """Create a mesh from a DEM (TIFF) file using PyVista.
        pixel_to_triangle_ratio controls the mesh density (default is 1: 1 pixel -> 1 triagnle).
        Smaller values create a coarser mesh, maximum is 1.
        """
        
        if pixel_to_triangle_ratio > 1:
            raise ValueError("The Maximum for pixel_to_triangle_ratio is 1; one cell per pixel.")
        
        self.check_raster_loaded()
        
        with rasterio.open(self.tif_path) as src:
            elevation_data = src.read(1)

        # Create the grid of coordinates
        rows, cols = elevation_data.shape
        
        # Adjust sampling based on pixel_to_triangle_ratio
        step = max(1, int(1/pixel_to_triangle_ratio))  # Ensure step is at least 1
        x = np.arange(0, cols, step)
        y = np.arange(0, rows, step)
        
        # Subsample the elevation data
        elevation_data = elevation_data[::step, ::step]
        
        # Create the mesh grid
        x, y = np.meshgrid(x, y)

        # Flatten the coordinates and elevations
        points = np.vstack([x.ravel(), y.ravel(), elevation_data.ravel()]).T
        max_y = elevation_data.shape[0]  # Get max Y value
        y_flipped = max_y - y  # Flip Y-coordinates

        points = np.vstack([x.ravel(), y_flipped.ravel(), elevation_data.ravel()]).T
        
        valid_points = points[~np.isnan(points[:, 2])]  # Remove NaN points

        # Triangulate the points using Delaunay
        tri = Delaunay(valid_points[:, :2])

        # Create a PyVista mesh from the triangulated points
        mesh = pv.PolyData(valid_points)
        mesh.faces = np.hstack([np.full((tri.simplices.shape[0], 1), 3), tri.simplices])

        # Transfer mesh to geocenter if specified
        if self.geocenter is not None:
            # Create translation vector
            translation_vector = np.concatenate((np.array(self.geocenter), [mesh.center[2]])) - mesh.center
            
            # Translate vertices
            mesh.translate(translation_vector, inplace=True)

        # Prepare output file path
        output_filename = os.path.splitext(os.path.basename(self.tif_path))[0]
        output_path = os.path.join(self.output_dir, f"{output_filename}_trn.stl")

        # Export the mesh to STL
        mesh.save(output_path)
        print(f"Mesh successfully exported to {output_path}")

    def visualize(self, show=True):
        """
        Visualize the terrain and TIN sampling with the same aspect ratio for all subplots.
        """
        self.check_raster_loaded()
        self.check_tin_data()
        
        # Create the figure with specific size
        fig = plt.figure(figsize=(15, 5))
        
        # Use GridSpec to control the layout and size of subplots
        gs = gridspec.GridSpec(1, 3, width_ratios=[1, 1, 1])
        
        # Original raster subplot
        ax1 = plt.subplot(gs[0])
        ax1.imshow(self.raster_data, cmap='terrain')
        ax1.set_title('Original Raster')
        plt.colorbar(ax1.imshow(self.raster_data, cmap='terrain'), ax=ax1, label='Elevation')
        
        # Complexity map subplot
        complexity_map = self.detect_terrain_complexity()
        ax2 = plt.subplot(gs[1])
        ax2.imshow(complexity_map, cmap='viridis')
        ax2.set_title('Terrain Complexity')
        plt.colorbar(ax2.imshow(complexity_map, cmap='viridis'), ax=ax2, label='Complexity')
        
        # TIN Sampling subplot
        max_y = self.raster_data.shape[0]  # Get max row index
        flipped_y = max_y - self.data['points'][:, 1]  # Flip Y-axis
        
        # Define plot limits based on raster dimensions
        xlim = (0, self.raster_data.shape[1])  # Column range
        ylim = (0, self.raster_data.shape[0])  # Row range
        
        ax3 = plt.subplot(gs[2])
        scatter = ax3.scatter(self.data['points'][:, 0], 
                            flipped_y,  
                            c=self.data['values'], 
                            cmap='terrain', 
                            alpha=0.7, s=5)
        
        ax3.set_xlim(xlim)
        ax3.set_ylim(ylim)
        ax3.set_title('Adaptive TIN Sampling')
        ax3.set_xlabel('X')
        ax3.set_ylabel('Y')
        
        # Correct colorbar association
        plt.colorbar(scatter, ax=ax3, label='Elevation')
        
        # Adjust layout to make sure subplots are evenly distributed
        plt.tight_layout()
        
        # Show or save the plot
        plt.show() if show else plt.savefig(os.path.join(self.output_dir, "sampling_quality.png"))

    def generate_mesh_info(self):
        """
        Generate and return mesh information.
        
        Returns:
        --------
        dict
            Mesh statistics and information
        """
        self.check_tin_data()
        
        mesh_summary =  {
            'vertices_count': len(self.mesh.vertices),
            'faces_count': len(self.mesh.faces),
            'volume': self.mesh.volume,
            'surface_area': self.mesh.area,
            'is_watertight': self.mesh.is_watertight,
            'is_empty': self.mesh.is_empty,
            'bounds': {
                'min': self.mesh.bounds[0],
                'max': self.mesh.bounds[1]
            }
        }

        # write the mesh summary as a log file
        with open(os.path.join(self.output_dir, "mesh_summary.txt"), "w") as f:
            for key, value in mesh_summary.items():
                f.write(f"{key}: {value}\n")