# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GeoBlocks is a catalogue of standard geometries for nuclear waste disposal site analysis in Germany. The project contains geometries for 4 host rock types: claystone/shale, crystalline rocks, stratiform salt, and steep salt. This is a research project based on Carl et al., 2023a focusing on subsurface geological modeling.

## Architecture

The project is organized into distinct geology-focused modules:

- `geometries/`: Contains Jupyter notebooks for different geological formations
  - `salt/`: Salt geometry models (flat salt, roller, sheet, stock, wall, anticline, pillow)
  - `claystone/`: Clay formation models (flat, folded)
  - `crystalline rocks/`: Crystalline rock models (batholith stock)
- `block_model_generator/`: Interactive tools for creating block models with GUI components
- `mdoel_generator/`: 2D to 3D data generation tools for geological modeling

## Development Environment

This is a Python-based project using Jupyter notebooks as the primary development environment. The codebase heavily relies on:

- **GemPy**: Primary geological modeling library
- **PyVista**: 3D visualization
- **Matplotlib/Plotly**: 2D plotting and interactive visualization  
- **NumPy/Pandas**: Data manipulation
- **Pygame/PyQt5**: Interactive drawing interfaces
- **NURBS/B-spline libraries**: For geological curve generation
- **Kriging libraries**: For spatial interpolation

## Key Development Patterns

### Geological Modeling Workflow
1. Define control points using NURBS curves for geological boundaries
2. Create slice-based geometries (often using 2 perpendicular slices)
3. Generate surface points and orientations data
4. Use GemPy to create 3D geological models
5. Visualize results with PyVista/Plotly

### Interactive Development
- Notebooks use ipywidgets for interactive parameter control
- Sliders control NURBS control points for real-time geometry modification
- Standard model presets are available for common geological formations

### Data Structure
- Surface points stored as pandas DataFrames with x,y,z coordinates and formation names
- Orientation data includes dip, azimuth, and polarity for geological structures
- Models use 20x20x20 grid resolution by default for interpolation

## Working with Geometries

Each geometry notebook follows a similar pattern:
1. Import dependencies and define NURBS functions
2. Create interactive sliders for control points
3. Generate slice geometries using NURBS curves
4. Combine slices into 3D geological models
5. Compute and visualize the final model

When modifying geometries, work with the slider values to adjust control points rather than hardcoding coordinates.