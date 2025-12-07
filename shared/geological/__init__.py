"""
Shared geological modeling functionality.

This package provides common NURBS-based geological modeling tools
used across different geological formations.
"""

from .nurbs import create_nurbs_curve, NURBSCurveGenerator, NURBS
from .formations import SaltFormation, GeologicalFormation, salt

__all__ = [
    'create_nurbs_curve', 'NURBSCurveGenerator', 'NURBS',
    'SaltFormation', 'GeologicalFormation', 'salt'
]