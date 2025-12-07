"""
NURBS-based geological curve generation.

This module provides optimized NURBS curve generation for geological
boundary modeling with improved performance and error handling.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional, Union
from geomdl import BSpline
from geomdl import utilities as utils


class NURBSCurveGenerator:
    """Optimized NURBS curve generator for geological boundaries."""
    
    DEFAULT_DEGREE = 3
    DEFAULT_NR_POINTS = 50
    
    def __init__(self, degree: int = DEFAULT_DEGREE):
        """Initialize the NURBS curve generator."""
        self.degree = degree
    
    def create_curve_from_control_points(
        self,
        left_x: float, right_x: float, mid_left_x: float, mid_right_x: float,
        top_left_x: float, top_right_x: float, top_x: float,
        left_y: float, right_y: float, mid_left_y: float, mid_right_y: float,
        top_left_y: float, top_right_y: float, top_y: float,
        nr_points: int = DEFAULT_NR_POINTS,
        plot: bool = True
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create NURBS curve from 7 control points.
        
        Args:
            left_x, left_y: Bottom left control point
            mid_left_x, mid_left_y: Left control point at 33% height
            top_left_x, top_left_y: Left control point at 66% height
            top_x, top_y: Top control point
            top_right_x, top_right_y: Right control point at 66% height
            mid_right_x, mid_right_y: Right control point at 33% height
            right_x, right_y: Bottom right control point
            nr_points: Number of points to sample from curve
            plot: Whether to create visualization plot
            
        Returns:
            Tuple of (curve_points, derivative_angles)
            
        Raises:
            ValueError: If control points are invalid
        """
        try:
            # Validate inputs
            if nr_points <= 0:
                raise ValueError("nr_points must be positive")
            
            # Create control points array
            control_points = [
                [left_x, left_y], 
                [mid_left_x, mid_left_y], 
                [top_left_x, top_left_y],
                [top_x, top_y], 
                [top_right_x, top_right_y], 
                [mid_right_x, mid_right_y],
                [right_x, right_y]
            ]
            
            # Validate control points
            if any(not isinstance(pt[0], (int, float)) or not isinstance(pt[1], (int, float)) 
                   for pt in control_points):
                raise ValueError("All control point coordinates must be numeric")
            
            return self._create_curve_from_points(control_points, nr_points, plot)
            
        except Exception as e:
            raise ValueError(f"Error creating NURBS curve: {e}") from e
    
    def _create_curve_from_points(
        self, 
        control_points: List[List[float]], 
        nr_points: int,
        plot: bool
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Create NURBS curve from control points array."""
        # Create B-spline curve
        curve = BSpline.Curve()
        curve.degree = self.degree
        curve.ctrlpts = control_points
        
        # Generate knot vector
        curve.knotvector = utils.generate_knot_vector(self.degree, len(curve.ctrlpts))
        
        # Set evaluation delta
        curve.delta = 1.0 / nr_points
        
        # Get curve points
        curve_points = np.array(curve.evalpts)
        
        # Calculate derivatives more efficiently
        derivative_angles = self._calculate_derivative_angles(curve, nr_points)
        
        # Create plot if requested
        if plot:
            self._plot_curve(curve_points, control_points)
        
        return curve_points, derivative_angles
    
    def _calculate_derivative_angles(self, curve: BSpline.Curve, nr_points: int) -> np.ndarray:
        """Calculate derivative angles efficiently using vectorized operations."""
        # Pre-allocate arrays for better performance
        u_values = np.linspace(0, 1, nr_points, endpoint=False)
        derivatives = np.zeros((nr_points, 2))
        
        # Calculate derivatives
        for i, u in enumerate(u_values):
            derivative = curve.derivatives(u=u, order=1)[1]
            derivatives[i] = [derivative[0], derivative[1]]
        
        # Calculate angles
        angles_rad = np.arctan2(derivatives[:, 1], derivatives[:, 0])
        angles_deg = np.degrees(angles_rad) % 360
        
        return angles_deg
    
    def _plot_curve(self, curve_points: np.ndarray, control_points: List[List[float]]) -> None:
        """Create visualization plot of the curve."""
        try:
            fig, ax = plt.subplots(figsize=(7, 7))
            
            # Plot curve
            ax.plot(curve_points[:, 0], curve_points[:, 1], "-", 
                   label="NURBS Curve", linewidth=2)
            
            # Plot control points
            ctrl_pts_array = np.array(control_points)
            ax.plot(ctrl_pts_array[:, 0], ctrl_pts_array[:, 1], "o-", 
                   label="Control Points", markersize=8, alpha=0.7)
            
            # Set axis properties
            ax.set_xlim(0, 20)
            ax.set_ylim(0, 20)
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.legend()
            ax.grid(True, alpha=0.3)
            ax.set_title("NURBS Geological Boundary Curve")
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            print(f"Warning: Could not create plot: {e}")


def create_nurbs_curve(
    left_x: float, right_x: float, mid_left_x: float, mid_right_x: float,
    top_left_x: float, top_right_x: float, top_x: float,
    left_y: float, right_y: float, mid_left_y: float, mid_right_y: float,
    top_left_y: float, top_right_y: float, top_y: float,
    nr_points: int = 50,
    fig: bool = True
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Create NURBS curve for geological boundary modeling.
    
    This function maintains compatibility with the original NURBS function
    while providing improved performance and error handling.
    
    Args:
        Control point coordinates (14 parameters for 7 points)
        nr_points: Number of points to sample from curve
        fig: Whether to create visualization plot
        
    Returns:
        Tuple of (curve_points, derivative_angles)
    """
    generator = NURBSCurveGenerator()
    return generator.create_curve_from_control_points(
        left_x, right_x, mid_left_x, mid_right_x,
        top_left_x, top_right_x, top_x,
        left_y, right_y, mid_left_y, mid_right_y,
        top_left_y, top_right_y, top_y,
        nr_points, fig
    )


# Backward compatibility alias
NURBS = create_nurbs_curve