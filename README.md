# GeoBlocks - Catalogue of Geometries

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GemPy](https://img.shields.io/badge/GemPy-2.3+-green.svg)](https://www.gempy.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

This is the catalogue of standard geometries created in the GeoBlocks project, as introduced in Carl et al., 2023a: "Host rock analysis for the German nuclear waste disposal site-selection: review of subsurface geometries and input data for geological modelling". According to the extended abstract and references therein, standard geometries were constructed for the 4 potential host rock types in the German site-selection for high-level radioactive waste disposal (StandAG, 2017):

1. **Claystone/shale**
2. **Crystalline rocks**
3. **Stratiform salt**
4. **Steep salt**

The structure of the catalogue is chosen according to the systematizations outlined in Carl et al., 2023a.

## 🏗️ **Project Structure**

```
geoblocks-geometries/
├── 📁 geometries/                    # Geological formation models
│   ├── 📁 claystone/                # Clay formation geometries
│   ├── 📁 crystalline_rocks/        # Crystalline rock formations
│   └── 📁 salt/                     # Salt formation geometries
├── 📁 block_model_generator/         # Interactive block model creation tools
├── 📁 model_generator/               # 2D to 3D geological model generators
├── 📁 shared/                       # 🆕 Shared modules (refactored code)
│   ├── 📁 drawing/                  # Interactive drawing interface
│   └── 📁 geological/               # NURBS curves & geological modeling
├── 📁 examples/                     # 🆕 Usage examples and tutorials
├── 📁 images/                       # Documentation images
├── 📄 requirements.txt              # 🆕 Python dependencies
├── 📄 environment.yml               # 🆕 Conda environment
├── 📄 MIGRATION_GUIDE.md           # 🆕 Refactoring guide
└── 📄 CLAUDE.md                     # 🆕 Development documentation
```

## 🚀 **Installation**

### Option 1: Using conda (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-org/geoblocks-geometries.git
cd geoblocks-geometries

# Create conda environment (this installs most dependencies)
conda env create -f environment.yml
conda activate geoblocks

# Verify installation
python -c "import shared.geological; print('✅ Installation successful!')"
```

### Option 2: Using pip

```bash
# Clone the repository
git clone https://github.com/your-org/geoblocks-geometries.git
cd geoblocks-geometries

# Create virtual environment (recommended)
python -m venv geoblocks-env
source geoblocks-env/bin/activate  # On Windows: geoblocks-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import shared.geological; print('✅ Installation successful!')"
```

### Option 3: Manual Installation

If you encounter issues with the environment files:

```bash
# Install core dependencies first
conda install -c conda-forge numpy scipy pandas matplotlib plotly jupyter

# Install specialized packages via pip
pip install gempy>=2.3.0 geomdl>=5.3.0 pykrige>=1.6.0 pyvista>=0.36.0

# Install GUI packages
conda install -c conda-forge pyqt pygame ipywidgets
```

### 🔧 **Troubleshooting Installation**

**Common Issues:**

1. **GemPy Installation Problems:**
   ```bash
   # Try installing with specific channels
   pip install gempy --no-deps
   pip install theano-pymc aesara
   ```

2. **geomdl Not Found:**
   ```bash
   # geomdl is only available via pip
   pip install geomdl>=5.3.0
   ```

3. **PyQt5 Issues on macOS:**
   ```bash
   # Use conda for PyQt5 on macOS
   conda install -c conda-forge pyqt
   ```

4. **VTK/PyVista Display Issues:**
   ```bash
   # For headless systems or display issues
   export PYVISTA_OFF_SCREEN=true
   ```

### System Dependencies

Some features may require additional system-level dependencies:
- **GDAL/OGR** for advanced geospatial data handling
- **VTK** for 3D visualization (usually installed with PyVista)
- **System display drivers** for interactive drawing interface

### 📋 **Verify Installation**

Test that everything works correctly:

```python
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
```

## 📖 **Quick Start**

### 1. Interactive Geological Drawing

Create geological boundaries using the interactive drawing interface:

```python
from shared.drawing import run_drawing_interface

# Launch interactive drawing tool
run_drawing_interface()

# Read the drawn curve points
import json
with open("curve_points.json", "r") as f:
    curve_points = json.load(f)
```

### 2. NURBS-Based Geological Modeling

Generate smooth geological curves using NURBS:

```python
from shared.geological import create_nurbs_curve

# Create a salt dome boundary curve
curve_points, derivative_angles = create_nurbs_curve(
    left_x=0, right_x=20, mid_left_x=3, mid_right_x=17,
    top_left_x=7, top_right_x=13, top_x=10,
    left_y=5, right_y=5, mid_left_y=8, mid_right_y=8,
    top_left_y=12, top_right_y=12, top_y=15,
    nr_points=50, fig=True
)
```

### 3. 3D Geological Model Creation

Build complete 3D geological models:

```python
from shared.geological import SaltFormation

# Create salt formation from two cross-sections
salt_formation = SaltFormation(
    slice_1_parameter=(curve_points_x, derivative_angles_x),
    slice_2_parameter=(curve_points_y, derivative_angles_y),
    slice_1_pos=10, slice_2_pos=10,
    formation_name="salt_dome"
)

# Compute 3D geological model
geological_model = salt_formation.compute_model(plot_3d=True)
```

## 🧪 **Available Geological Formations**

### Salt Formations
- **Flat Salt** (`geometries/salt/Flat_Salt.ipynb`)
- **Salt Roller** (`geometries/salt/Roller.ipynb`)
- **Salt Sheet** (`geometries/salt/Sheet.ipynb`)
- **Salt Stock** (`geometries/salt/Stock.ipynb`)
- **Salt Wall** (`geometries/salt/Wall.ipynb`)
- **Salt Anticline** (`geometries/salt/anticline.ipynb`)
- **Salt Pillow** (`geometries/salt/pillow.ipynb`)

### Claystone Formations
- **Flat Clay** (`geometries/claystone/Flat.ipynb`)
- **Folded Clay** (`geometries/claystone/folded_clay.ipynb`)

### Crystalline Rock Formations
- **Batholith Stock** (`geometries/crystalline_rocks/Batholith_stock.ipynb`)

## 🔧 **Development Tools**

### Interactive Model Generators
- **Block Model Generator** - GUI-based geological block model creation
- **2D to 3D Generator** - Convert 2D geological cross-sections to 3D models

### Shared Modules (NEW ✨)
- **`shared.drawing`** - Pygame-based interactive drawing interface
- **`shared.geological.nurbs`** - Optimized NURBS curve generation
- **`shared.geological.formations`** - Geological formation classes

## 📚 **Documentation & Examples**

### Getting Started
- **`examples/using_shared_modules.ipynb`** - Complete usage examples
- **`MIGRATION_GUIDE.md`** - Guide for updating legacy notebooks
- **`CLAUDE.md`** - Development documentation and architecture guide

### API Documentation
```python
# Interactive Drawing
from shared.drawing import DrawingInterface, run_drawing_interface

# NURBS Geometry
from shared.geological import (
    create_nurbs_curve, 
    NURBSCurveGenerator
)

# Geological Formations  
from shared.geological import (
    SaltFormation, 
    GeologicalFormation
)
```

## 🔬 **Scientific Workflow**

The typical workflow for geological modeling:

1. **📐 Design Geometry** - Use interactive drawing tools or define NURBS control points
2. **🎯 Create Curves** - Generate smooth geological boundaries using NURBS interpolation
3. **🏗️ Build 3D Model** - Combine multiple cross-sections into full 3D geological models
4. **📊 Visualize & Analyze** - Interactive 3D visualization and geological analysis
5. **💾 Export Results** - Save models and data for further analysis

## ⚠️ **Migration Notice**

**Legacy notebooks may contain security vulnerabilities.** Please see `MIGRATION_GUIDE.md` for instructions on:
- Replacing `%run` magic commands with secure imports
- Using shared modules instead of duplicated code
- Updating to the new project structure

## 🛠️ **Key Technologies**

- **[GemPy](https://www.gempy.org/)** - 3D geological modeling platform
- **[PyVista](https://pyvista.org/)** - 3D visualization and mesh analysis
- **[geomdl](https://github.com/orbingol/NURBS-Python)** - NURBS curve and surface library
- **[Matplotlib](https://matplotlib.org/)** - 2D plotting and visualization
- **[Plotly](https://plotly.com/python/)** - Interactive 3D plotting
- **[Pygame](https://www.pygame.org/)** - Interactive drawing interface
- **[NumPy](https://numpy.org/)**/**[SciPy](https://scipy.org/)**/**[Pandas](https://pandas.pydata.org/)** - Scientific computing core

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Citation**

If you use this software in your research, please cite:

```
Carl et al., 2023a: "Host rock analysis for the German nuclear waste disposal 
site-selection: review of subsurface geometries and input data for geological 
modelling"
```

## 🐛 **Issues & Contributing**

- **Report bugs** or request features via GitHub Issues
- **Contributing guidelines** - See development documentation in `CLAUDE.md`
- **Security issues** - Please report privately for responsible disclosure

## 🔗 **Related Projects**

- [GemPy](https://github.com/cgre-aachen/gempy) - Open-source 3D geological modeling
- [StandAG 2017](https://www.bge.de/en/disposal/site-selection/) - German site selection process