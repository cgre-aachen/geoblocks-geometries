# Migration Guide: Updating Notebooks to Use Shared Modules

This guide explains how to update existing notebooks to use the new shared module structure instead of duplicated code and `%run` magic commands.

## 🚨 Security Notice

The `%run` magic commands have been identified as a security vulnerability and should be replaced with proper Python imports.

## Changes Made

### 1. Removed Duplicate Files
- ✅ Removed `block_model_generator/draw.py`
- ✅ Removed `model_generator/draw.py`
- ✅ Created `shared/drawing/draw_interface.py` with improved functionality

### 2. Extracted Common Functions
- ✅ Moved NURBS functions to `shared/geological/nurbs.py`
- ✅ Moved salt class to `shared/geological/formations.py`

### 3. Fixed Directory Issues
- ✅ Fixed typo: `mdoel_generator` → `model_generator`
- ✅ Fixed spaces: `crystalline rocks` → `crystalline_rocks`

## Migration Instructions

### Replace `%run draw.py` Commands

**Old Code (INSECURE):**
```python
%run draw.py
```

**New Code (SECURE):**
```python
from shared.drawing import run_drawing_interface
run_drawing_interface()
```

### Replace Duplicated NURBS Functions

**Old Code:**
```python
# Duplicated NURBS function in every notebook
def NURBS(left_x, right_x, mid_left_x, ...):
    # 50+ lines of duplicated code
    ...
```

**New Code:**
```python
from shared.geological import create_nurbs_curve

# Use the shared function
curve_points, degrees = create_nurbs_curve(
    left_x, right_x, mid_left_x, ..., 
    nr_points=50, fig=True
)
```

### Replace Duplicated Salt Class

**Old Code:**
```python
# Duplicated salt class in every notebook
class salt:
    def __init__(self, ...):
        # Duplicated implementation
```

**New Code:**
```python
from shared.geological import SaltFormation

# Use the improved shared class
salt_formation = SaltFormation(
    slice_1_parameter=slice_1,
    slice_2_parameter=slice_2,
    formation_name="salt"
)
```

## Files That Need Updates

### High Priority (Security Issues)
1. **`model_generator/model_generator.ipynb`**
   - Replace `%run draw.py` in `draw_X()` and `draw_Y()` methods
   
2. **`block_model_generator/draw.ipynb`** 
   - Replace 4 instances of `%run draw.py`
   
3. **`block_model_generator/GUI.ipynb`**
   - Replace `%run draw.py` in GUI functions

### Medium Priority (Code Duplication)
4. **All salt geometry notebooks:**
   - `geometries/salt/Stock.ipynb`
   - `geometries/salt/pillow.ipynb`
   - `geometries/salt/anticline.ipynb`
   - `geometries/salt/Wall.ipynb`
   - `geometries/salt/Roller.ipynb`
   - `geometries/salt/Sheet.ipynb`
   - `geometries/salt/Flat_Salt.ipynb`

## Example Replacements

### For GUI Notebooks

**Before:**
```python
def draw_X(self):
    %run draw.py
    with open("curve_points.json", "r") as file:
        points = json.load(file)
    slice_x = np.array(points)[-1]
    self.x_points.append(slice_x)
```

**After:**
```python
def draw_X(self):
    from shared.drawing import run_drawing_interface
    run_drawing_interface()
    
    with open("curve_points.json", "r") as file:
        points = json.load(file)
    slice_x = np.array(points)[-1]
    self.x_points.append(slice_x)
```

### For Salt Geometry Notebooks

**Before:**
```python
# Cell with duplicated NURBS function
def NURBS(...):
    # 50+ lines of code

# Cell with duplicated salt class  
class salt:
    # 30+ lines of code

# Usage
curve_points, degree = NURBS(...)
salt_model = salt(...)
```

**After:**
```python
# Import shared modules
from shared.geological import create_nurbs_curve, SaltFormation

# Usage (same interface, cleaner implementation)
curve_points, degree = create_nurbs_curve(...)
salt_model = SaltFormation(...)
```

## Testing Your Changes

After making the updates, test that:

1. **Drawing interface works:** Import and run `run_drawing_interface()`
2. **NURBS curves generate correctly:** Create curves with `create_nurbs_curve()`
3. **Geological models compute:** Use `SaltFormation` to create 3D models
4. **No %run commands remain:** Search for `%run` in your notebooks

## Benefits After Migration

- ✅ **Security:** Removed `%run` command vulnerabilities
- ✅ **Maintainability:** Single source of truth for common functions
- ✅ **Performance:** Optimized algorithms with better error handling
- ✅ **Documentation:** Type hints and comprehensive docstrings
- ✅ **Testing:** Shared modules can be unit tested
- ✅ **Consistency:** Standardized interfaces across all notebooks

## Need Help?

See `examples/using_shared_modules.ipynb` for complete examples of the new patterns.