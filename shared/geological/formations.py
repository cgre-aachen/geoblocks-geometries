"""
Geological formation classes for 3D modeling.

This module provides classes for different geological formations
used in nuclear waste disposal site analysis.
"""

import numpy as np
import pandas as pd
import gempy as gp
import plotly.graph_objects as go
from typing import Tuple, Optional, List, Any
import warnings


class GeologicalFormation:
    """Base class for geological formations."""
    
    def __init__(self, formation_name: str = "formation"):
        """Initialize geological formation."""
        self.formation_name = formation_name
        self.geo_model: Optional[Any] = None
    
    def get_input_points(self):
        """Get input points for the formation. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement get_input_points")
    
    def set_input_data(self):
        """Set input data for GemPy model. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement set_input_data")


class SaltFormation(GeologicalFormation):
    """
    Salt formation class for geological modeling.
    
    This class handles salt dome and stratiform salt geometries using
    two perpendicular slices to define 3D salt body boundaries.
    """
    
    DEFAULT_EXTENT = [0, 20, 0, 20, 0, 20]
    DEFAULT_RESOLUTION = [50, 50, 50]
    
    def __init__(
        self,
        slice_nr: int = 2,
        slice_1_parameter: Optional[Tuple] = None,
        slice_2_parameter: Optional[Tuple] = None,
        slice_1_pos: float = 10,
        slice_2_pos: float = 10,
        formation_name: str = "salt",
        extent: Optional[List[float]] = None,
        resolution: Optional[List[int]] = None
    ):
        """
        Initialize salt formation.
        
        Args:
            slice_nr: Number of slices (typically 2)
            slice_1_parameter: Tuple of (curve_points, degree_angles) for first slice
            slice_2_parameter: Tuple of (curve_points, degree_angles) for second slice
            slice_1_pos: Position of first slice in 3D space
            slice_2_pos: Position of second slice in 3D space
            formation_name: Name of the geological formation
            extent: Model extent [x_min, x_max, y_min, y_max, z_min, z_max]
            resolution: Model resolution [nx, ny, nz]
        """
        super().__init__(formation_name)
        
        # Validate inputs
        if slice_1_parameter is None or slice_2_parameter is None:
            raise ValueError("Both slice_1_parameter and slice_2_parameter must be provided")
        
        self.slice_nr = slice_nr
        self.slice_1_data, self.degree_1 = slice_1_parameter
        self.slice_2_data, self.degree_2 = slice_2_parameter
        self.slice_pos_1 = slice_1_pos
        self.slice_pos_2 = slice_2_pos
        
        # Model configuration
        self.extent = extent or self.DEFAULT_EXTENT
        self.resolution = resolution or self.DEFAULT_RESOLUTION
        
        # Validate extent and resolution
        if len(self.extent) != 6:
            raise ValueError("Extent must have 6 values: [x_min, x_max, y_min, y_max, z_min, z_max]")
        if len(self.resolution) != 3:
            raise ValueError("Resolution must have 3 values: [nx, ny, nz]")
    
    def get_input_points(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get input points for both slices.
        
        Returns:
            Tuple of (x_slice_points, y_slice_points)
        """
        return self.slice_1_data, self.slice_2_data
    
    def set_input_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Process slice data into GemPy-compatible format.
        
        Returns:
            Tuple of (orientations_dataframe, surface_points_dataframe)
            
        Raises:
            ValueError: If slice data is invalid
        """
        try:
            x_slice_points = np.array(self.slice_1_data)
            y_slice_points = np.array(self.slice_2_data)
            
            # Validate slice data
            if x_slice_points.shape[1] != 2 or y_slice_points.shape[1] != 2:
                raise ValueError("Slice data must have shape (n_points, 2)")
            
            # Create X slice dataframe (fixed Y position)
            x_slice_coords = np.column_stack([
                x_slice_points[:, 0],  # x coordinates
                np.full(len(x_slice_points), self.slice_pos_1),  # fixed y position
                x_slice_points[:, 1]   # z coordinates
            ])
            x_slice_df = pd.DataFrame(x_slice_coords, columns=['x', 'y', 'z'])
            
            # Create Y slice dataframe (fixed X position)
            y_slice_coords = np.column_stack([
                np.full(len(y_slice_points), self.slice_pos_2),  # fixed x position
                y_slice_points[:, 0],  # y coordinates
                y_slice_points[:, 1]   # z coordinates
            ])
            y_slice_df = pd.DataFrame(y_slice_coords, columns=['x', 'y', 'z'])
            
            # Combine surface points
            surface_points = pd.concat([x_slice_df, y_slice_df], ignore_index=True)
            
            # Add formation names
            formation_column = pd.DataFrame({
                'formation': [self.formation_name] * len(surface_points)
            })
            surface_points = pd.concat([surface_points, formation_column], axis=1)
            
            # Create orientations
            orientation_1 = pd.DataFrame({
                'dip': self.degree_1 - 180,
                'azimuth': ['90'] * len(x_slice_df),
                'polarity': ['1'] * len(x_slice_df)
            })
            
            orientation_2 = pd.DataFrame({
                'dip': self.degree_2 - 180,
                'azimuth': ['0'] * len(y_slice_df),
                'polarity': ['1'] * len(y_slice_df)
            })
            
            # Combine orientations with surface points
            orientations = pd.concat([
                surface_points,
                pd.concat([orientation_1, orientation_2], ignore_index=True)
            ], axis=1)
            
            return orientations, surface_points
            
        except Exception as e:
            raise ValueError(f"Error processing slice data: {e}") from e
    
    def create_model(self) -> Any:
        """
        Create GemPy geological model.
        
        Returns:
            GemPy geological model object
            
        Raises:
            RuntimeError: If model creation fails
        """
        try:
            orientations, surface_points = self.set_input_data()
            
            # Create GemPy model
            geo_model = gp.create_model(self.formation_name)
            
            # Initialize model data
            gp.init_data(
                geo_model,
                extent=self.extent,
                resolution=self.resolution,
                orientations_df=orientations,
                surface_points_df=surface_points,
                default_values=True
            )
            
            # Add basement surface
            geo_model.add_surfaces('basement')
            
            self.geo_model = geo_model
            return geo_model
            
        except Exception as e:
            raise RuntimeError(f"Error creating geological model: {e}") from e
    
    def compute_model(
        self, 
        plot_3d: bool = True,
        plot_size: Tuple[int, int] = (900, 900),
        theano_optimizer: str = 'fast_compile'
    ) -> Any:
        """
        Compute the geological model interpolation.
        
        Args:
            plot_3d: Whether to create 3D visualization
            plot_size: Size of 3D plot (width, height)
            theano_optimizer: Theano optimization level
            
        Returns:
            Computed GemPy model
            
        Raises:
            RuntimeError: If model computation fails
        """
        try:
            # Create model if not already created
            if self.geo_model is None:
                self.create_model()
            
            # Set interpolator with error handling
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                gp.set_interpolator(
                    self.geo_model,
                    compile_theano=True,
                    theano_optimizer=theano_optimizer
                )
            
            # Compute model
            sol = gp.compute_model(self.geo_model)
            
            # Create 3D visualization if requested
            if plot_3d:
                self._create_3d_visualization(plot_size)
            
            return self.geo_model
            
        except Exception as e:
            raise RuntimeError(f"Error computing geological model: {e}") from e
    
    def _create_3d_visualization(self, plot_size: Tuple[int, int]) -> None:
        """Create 3D isosurface visualization."""
        try:
            if self.geo_model is None or self.geo_model.solutions is None:
                print("Warning: No model solution available for visualization")
                return
            
            # Create meshgrid for visualization
            x_range = np.arange(self.extent[0], self.extent[1], 0.4)
            y_range = np.arange(self.extent[2], self.extent[3], 0.4)
            z_range = np.arange(self.extent[4], self.extent[5], 0.4)
            xx, yy, zz = np.meshgrid(x_range, y_range, z_range)
            
            # Get scalar field values
            scalar_field = self.geo_model.solutions.scalar_field_matrix[0]
            surface_points_values = self.geo_model.solutions.scalar_field_at_surface_points[0]
            
            if len(surface_points_values) == 0:
                print("Warning: No surface points available for visualization")
                return
            
            # Create isosurface plot
            fig = go.Figure(data=[go.Isosurface(
                x=xx.flatten(),
                y=yy.flatten(),
                z=zz.flatten(),
                value=scalar_field,
                isomin=surface_points_values[0],
                isomax=surface_points_values[0],
                surface_count=1,
                opacity=0.6,
                caps=dict(x_show=False, y_show=False, z_show=False),
                colorscale='BlueRed'
            )])
            
            fig.update_layout(
                autosize=True,
                width=plot_size[0],
                height=plot_size[1],
                margin=dict(autoexpand=True),
                title=f"{self.formation_name.title()} Formation 3D Model"
            )
            
            fig.show()
            
        except Exception as e:
            print(f"Warning: Could not create 3D visualization: {e}")


# Backward compatibility alias
salt = SaltFormation