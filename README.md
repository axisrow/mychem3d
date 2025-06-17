# MyChem3D - 3D Molecular Visualization Tool

A pseudochemical 3D molecular simulator with cross-platform OpenGL support.

## Features
- **PyQt5** GUI with OpenGL rendering
- **Dual OpenGL Support**: 
  - Modern OpenGL 4.3+ with compute shaders (full version)
  - Legacy OpenGL 2.1+ compatibility (macOS M1, older systems)
- **Automatic Detection**: Chooses appropriate renderer based on system capabilities
- **Real-time 3D Visualization**: Interactive molecular models with lighting
- **Multiple File Formats**: JSON-based molecule loading
- **Cross-Platform**: Windows, macOS (including M1), Linux

## Quick Start

### Installation
```bash
python -m pip install pillow numpy pyglm pyopengl pyqt5
```

### Running the Application

**GUI Launcher (Default):**
```bash
# Launch with GUI menu (default)
python main.py

# Force GUI launcher
python main.py --gui
```

**Command Line Options:**
```bash
# Quick Demo - Water molecule (recommended!)
python main.py --demo

# Complex Demo - Fullerene C60
python main.py --complex

# Command-line mode (no GUI)
python main.py --cli

# Force compatibility mode
python main.py --compat

# Force full-featured mode
python main.py --full

# Show help
python main.py --help
```

### GUI Launcher Features
- **🔍 Automatic OpenGL Detection** - Visually shows your system capabilities
- **🎨 Color-Coded Recommendations** - Green for recommended, yellow for warnings
- **🧬 Quick Demo** - Instant water molecule visualization
- **🔬 Test Complex** - Fullerene (C60) for testing complex molecules
- **❓ Built-in Help** - Complete documentation within the GUI
- **🖥️ System Information** - Platform and OpenGL details displayed

## System Requirements
- **Python 3.7+**
- **OpenGL 2.1+** (compatibility mode) or **4.3+** (full mode)
- **PyQt5, NumPy, PyGLM, PIL**

## Tested Systems
- ✅ **macOS M1** (OpenGL 2.1 Metal - auto-detected)
- ✅ **Intel Iris Xe Graphics** (OpenGL 4.3+)
- ✅ **Windows 10/11** with modern GPUs
- ✅ **Linux** with Mesa drivers

## Project Structure
```
mychem3d/
├── main.py              # Main entry point with auto-detection
├── src/                 # Core application modules
│   ├── mychem3d.py      # Full OpenGL 4.3+ version
│   ├── mychem3d_macos.py # OpenGL 2.1+ compatibility version
│   ├── mychem_space.py  # Space and physics simulation
│   └── mychem_atom.py   # Atom class definitions
├── examples/            # Sample molecule files
│   ├── simple/          # Basic molecules (H2O, CO2, etc.)
│   ├── alkane/          # Alkane series
│   └── ...              # Other chemical families
├── shaders/             # OpenGL shader files
└── utils/               # Utility modules
```

## Loading Molecules

### Quick Load (Built-in Examples)
The application includes a **File > Quick Load** menu with molecules:

**Simple Molecules:**
- **Water (H2O)**
- **Methane (CH4)** 
- **Carbon Dioxide (CO2)**
- **Ammonia (NH3)**

**Complex Molecules:**
- **Fullerene (C60)** - 60 carbon atoms in soccer ball structure
- **Carbon Nanotube** - 108+ carbon atoms in cylindrical structure
- **ATP** - Adenosine triphosphate (energy molecule)
- **Benzene Ring** - Aromatic hydrocarbon
- **Caffeine** - Stimulant molecule

### Scene Creation
**File > Quick Load > Create Scene** offers pre-built molecular scenes:
- **Biochemistry Demo** - Water, ATP, and amino acids
- **Organic Chemistry** - Methane, benzene, and caffeine
- **Nanotechnology** - Fullerene and carbon nanotubes

### Multiple Molecule Support
- **Load Molecule** - Replace current scene with single molecule
- **Add Molecule to Scene** - Add molecule to existing scene
- **Clear Scene** - Remove all molecules
- Automatic camera adjustment based on scene complexity
- Real-time atom counting in status bar

### Custom Molecules
Load custom molecules via **File > Load Molecule...** using JSON format:
```json
{
  "atoms": [
    {"x": 515.0, "y": 500.0, "z": 500.0, "type": 8},
    {"x": 575.0, "y": 500.0, "z": 500.0, "type": 1},
    {"x": 485.0, "y": 540.0, "z": 500.0, "type": 1}
  ]
}
```

**Atom Types Supported:**
- Type 1: Hydrogen (White)
- Type 6: Carbon (Yellow) 
- Type 7: Nitrogen (Blue)
- Type 8: Oxygen (Red)
- Type 15: Phosphorus (Brown)
- Type 16: Sulfur (Yellow)
- Type 11: Sodium (Light Blue)
- Type 17: Chlorine (Green)

## Controls and Usage
-    Mouse + left button  -  rotate camera
-    Mouse + right button - move camera left and right
-     +shift - gently
-    Mouse wheel - move camera forward and back

 In merge mode (adding atoms or files):
- enter or click - do merge 
- mouse wheel - change parameter
- mouse wheel + shift - slow change
- mouse wheel + control - move camera forward and back
- g - move,  x,y,z for select axis
- r - rotate object, x,y,z for select rotate axis
- a - rotate object in special axis, setted in selection mode


Selection atoms
1. molecule selection mode
  -  click an atom, then use the mouse wheel to add neighboring atoms to the selection
  -  ctrl + click  - append/remove to/from selection
  -  enter or click on selection - go to merge mode with selected atoms
  -  also "r" and "g" - go to merge mode with move and rotation
  -  <delete> - delete selected
  -  ctrl + alt + s - save selected atoms
  -  "b" - try to bond two selected atoms with selected nodes, resutl in statusbar
  -   middle button for change selected node in selected atom
  - Right mouse button on selected - context menu for actions
  - a new atom can be grown from the selected atom node using the numeric keys
  - "a" - set axis in direction of selected node

## Troubleshooting

### Qt5 Platform Plugin Error (Windows)
**Error**: `could not find or load the Qt platform plugin "windows"`
**Solution**: Set environment variable:
```bash
set QT_QPA_PLATFORM_PLUGIN_PATH=%PythonPath%\Lib\site-packages\PyQt5\Qt5\plugins\platforms
```

### OpenGL Issues
- **macOS M1**: Automatically uses OpenGL 2.1 compatibility mode
- **Older Systems**: Use `python main.py --compat` to force compatibility mode
- **Modern GPUs**: Application auto-detects OpenGL 4.3+ support

### Performance Issues
- Try compatibility mode: `python main.py --compat`
- Reduce molecule complexity
- Check GPU drivers are up to date

### GUI Launcher Issues
- **"Event loop already running"**: Fixed in v2.1 - GUI properly closes before launching
- **Segmentation fault**: Fixed - proper Qt application lifecycle management
- **Quick Demo not working**: Fixed in v2.1 - direct process launch with fallback to subprocess
- **Nothing happens after clicking**: Fixed - improved error handling and debugging output

### Quick Start (If GUI doesn't work)
**Simple CLI commands that always work:**
```bash
# 🧬 Quick water molecule demo
python main.py --demo

# 🔬 Amazing fullerene (C60) demo  
python main.py --complex
```

These commands bypass GUI completely and work reliably!

### Debug Mode
If having issues, try:
```bash
# Full compatibility mode
python main.py --compat

# Command-line auto-detection
python main.py --cli
```

## Warning
⚠️ **This application may create misconceptions about chemical interactions.** Use for educational and visualization purposes only.



## GUI Launcher Screenshots

**Main Launcher Interface:**
The GUI launcher automatically detects your system and recommends the best version:

![GUI Launcher](images/launcher-demo.png)

**Complex Molecular Scenes:**
Create impressive visualizations like in the original demos:

![Demo Scene 1](images/demo1.PNG?raw=true)
![Demo Scene 2](images/demo2.JPG?raw=true)

**How to recreate demo scenes:**
1. **For Demo 1 (Nanotechnology)**: Use `File > Quick Load > Create Scene > Nanotechnology`
2. **For Demo 2 (Complex Biochemistry)**: Use `File > Quick Load > Create Scene > Biochemistry Demo`
3. **Custom Scenes**: Use `File > Add Molecule to Scene` to combine multiple molecules

