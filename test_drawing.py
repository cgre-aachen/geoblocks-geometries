from shared.drawing import run_drawing_interface

# Launch interactive drawing tool
run_drawing_interface()

# Read the drawn curve points
import json
with open("curve_points.json", "r") as f:
    curve_points = json.load(f)
