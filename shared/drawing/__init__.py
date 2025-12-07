"""
Drawing interface module for interactive curve drawing.

Provides pygame-based interactive drawing tools for geological
boundary definition.
"""

from .draw_interface import DrawingInterface, main as run_drawing_interface

__all__ = ['DrawingInterface', 'run_drawing_interface']