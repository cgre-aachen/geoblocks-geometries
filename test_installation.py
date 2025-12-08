# Test basic imports
from shared.geological import create_nurbs_curve, SaltFormation
from shared.drawing import DrawingInterface

# Test NURBS generation
curve_points, angles = create_nurbs_curve(
    0, 20, 3, 17, 7, 13, 10,  # x coordinates
    5, 5, 8, 8, 12, 12, 15,   # y coordinates
    nr_points=20, fig=False
)
print(f"✅ Generated {len(curve_points)} curve points")
