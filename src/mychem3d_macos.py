#!/usr/bin/env python3
"""
MyChem3D macOS Compatibility Version

OpenGL 2.1/GLSL 1.20 compatible version for macOS M1 and older systems.
This version automatically loads when OpenGL 4.3+ is not available.
"""

import sys
import json
import os
import numpy as np
from math import sin, cos, pi
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QAction, QStatusBar, QMessageBox, QFileDialog
from PyQt5.QtOpenGL import QGLWidget
from PyQt5.QtCore import QTimer
from OpenGL.GL import *
from OpenGL.arrays import vbo
import glm

# Import MyChem classes
from mychem_space import Space
from mychem_atom import Atom

class MyChem3DGLWidget(QGLWidget):
    def __init__(self, space):
        super().__init__()
        self.space = space
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16)  # ~60 FPS
        
        # Demo atoms data
        self.atoms = []
        self.molecule_groups = []  # Support for multiple molecules in one scene
        self.current_group_offset = glm.vec3(0, 0, 0)  # Offset for new molecules
        self.load_demo_molecule()
        
        # Camera
        self.camera_pos = glm.vec3(0, 0, 2)
        self.camera_target = glm.vec3(0, 0, 0)
        self.rotation = 0.0
        
        # Mouse control
        self.last_x = 400
        self.last_y = 300
        self.yaw = -90.0
        self.pitch = 0.0
        
    def load_demo_molecule(self):
        """Load default demo molecule - checks for demo mode"""
        import os
        
        # Check for demo mode from launcher
        demo_mode = os.environ.get('MYCHEM3D_DEMO', 'water')
        
        if demo_mode == 'fullerene' and os.path.exists('examples/nanotubes/fullerene.json'):
            print("🔬 Loading Fullerene demo from launcher...")
            self.load_molecule_from_json('examples/nanotubes/fullerene.json')
        elif demo_mode == 'water' and os.path.exists('examples/simple/H2O.json'):
            print("🧬 Loading Water demo from launcher...")
            print(f"📁 File path: examples/simple/H2O.json")
            self.load_molecule_from_json('examples/simple/H2O.json')
            print(f"✅ Loaded {len(self.atoms)} atoms total")
        else:
            # Default fallback - simple water molecule with better visibility
            print("🧬 Using fallback water molecule (H2O.json not found)")
            self.atoms = [
                {'pos': glm.vec3(0, 0, 0), 'color': glm.vec4(1, 0, 0, 1), 'radius': 0.15, 'type': 2},       # O - Red (type 2)
                {'pos': glm.vec3(0.25, 0, 0), 'color': glm.vec4(1, 1, 1, 1), 'radius': 0.10, 'type': 1},    # H - White
                {'pos': glm.vec3(-0.2, 0.15, 0), 'color': glm.vec4(1, 1, 1, 1), 'radius': 0.10, 'type': 1}, # H - White
            ]
        
        # Clear demo mode after use
        if 'MYCHEM3D_DEMO' in os.environ:
            del os.environ['MYCHEM3D_DEMO']
        
    def get_atom_color_and_radius(self, atom_type):
        """Get color and radius for atom type - using project's custom numbering"""
        atom_properties = {
            1:  {'color': glm.vec4(1.0, 1.0, 1.0, 1.0), 'radius': 0.10},  # Hydrogen - White - Better visibility
            2:  {'color': glm.vec4(1.0, 0.0, 0.0, 1.0), 'radius': 0.15},  # Oxygen (in H2O) - Red - Increased size
            4:  {'color': glm.vec4(0.3, 0.3, 0.3, 1.0), 'radius': 0.12},  # Carbon (in CH4) - Dark gray
            6:  {'color': glm.vec4(1.0, 1.0, 0.0, 1.0), 'radius': 0.14},  # Carbon - Yellow (like in screenshots)
            7:  {'color': glm.vec4(0.0, 0.0, 1.0, 1.0), 'radius': 0.12},  # Nitrogen - Blue
            8:  {'color': glm.vec4(1.0, 0.0, 0.0, 1.0), 'radius': 0.15},  # Oxygen - Red - Increased size
            15: {'color': glm.vec4(0.5, 0.25, 0.2, 1.0), 'radius': 0.18},  # Phosphorus - Brown
            16: {'color': glm.vec4(1.0, 1.0, 0.0, 1.0), 'radius': 0.16},  # Sulfur - Yellow
            11: {'color': glm.vec4(0.7, 0.7, 0.9, 1.0), 'radius': 0.14},  # Sodium - Light blue
            17: {'color': glm.vec4(0.0, 1.0, 0.0, 1.0), 'radius': 0.13},  # Chlorine - Green
        }
        
        return atom_properties.get(atom_type, {
            'color': glm.vec4(0.7, 0.7, 0.7, 1.0), 
            'radius': 0.06
        })
        
    def add_molecule_from_json(self, file_path, offset=None):
        """Add molecule from JSON file to current scene (keeps existing molecules)"""
        if offset is None:
            offset = self.current_group_offset
            
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                
            if 'atoms' not in data:
                return False
                
            new_atoms = []
            
            # Find center and bounds of molecule for positioning
            center_x = sum(atom['x'] for atom in data['atoms']) / len(data['atoms'])
            center_y = sum(atom['y'] for atom in data['atoms']) / len(data['atoms'])
            center_z = sum(atom['z'] for atom in data['atoms']) / len(data['atoms'])
            
            # Calculate bounds for auto-scaling
            min_x = min(atom['x'] for atom in data['atoms'])
            max_x = max(atom['x'] for atom in data['atoms'])
            min_y = min(atom['y'] for atom in data['atoms'])
            max_y = max(atom['y'] for atom in data['atoms'])
            min_z = min(atom['z'] for atom in data['atoms'])
            max_z = max(atom['z'] for atom in data['atoms'])
            
            # Calculate scale factor to fit molecule in view
            range_x = max_x - min_x
            range_y = max_y - min_y
            range_z = max_z - min_z
            max_range = max(range_x, range_y, range_z)
            
            # Scale factor: smaller molecules get better scaling for visibility
            if max_range > 100:  # Large molecule (like fullerene, ATP)
                scale_factor = 0.01 / max_range  # Adaptive scaling
            elif max_range < 30:  # Very small molecules like H2O (range ~20) - realistic bond lengths
                scale_factor = 0.018  # Realistic molecular scale avoiding atom overlap (~0.25-0.27)
            else:  # Medium molecules like CH4, NH3
                scale_factor = 0.02  # Slightly larger for visibility
            
            for atom_data in data['atoms']:
                atom_type = atom_data.get('type', 1)
                
                # Convert coordinates with adaptive scaling
                x = (atom_data['x'] - center_x) * scale_factor
                y = (atom_data['y'] - center_y) * scale_factor  
                z = (atom_data['z'] - center_z) * scale_factor
                
                # Get properties for this atom type
                props = self.get_atom_color_and_radius(atom_type)
                
                # Apply offset for multiple molecules
                final_pos = glm.vec3(x + offset.x, y + offset.y, z + offset.z)
                
                atom = {
                    'pos': final_pos,
                    'color': props['color'],
                    'radius': props['radius'],
                    'type': atom_type
                }
                new_atoms.append(atom)
            
            # Add new atoms to main list
            self.atoms.extend(new_atoms)
            
            # Store as a group for future reference
            self.molecule_groups.append({
                'name': os.path.basename(file_path),
                'atoms': new_atoms,
                'offset': offset
            })
            
            print(f"Added {len(new_atoms)} atoms from {os.path.basename(file_path)} (Total: {len(self.atoms)})")
            print(f"Scale factor used: {scale_factor}, Max range: {max_range}")
            
            # Debug: Print first few atoms' positions and properties
            for i, atom in enumerate(new_atoms[:3]):  # Show max 3 atoms
                print(f"  Atom {i+1}: type={atom['type']}, pos=({atom['pos'].x:.3f}, {atom['pos'].y:.3f}, {atom['pos'].z:.3f}), radius={atom['radius']:.3f}")
            
            # Adjust camera for total number of atoms
            if len(self.atoms) > 50:  # Large scene
                self.camera_pos = glm.vec3(0, 0, 4)  # Move camera back
            elif len(self.atoms) > 20:  # Medium scene
                self.camera_pos = glm.vec3(0, 0, 3)
            else:  # Small scene
                self.camera_pos = glm.vec3(0, 0, 2)
            
            # Update offset for next molecule
            self.current_group_offset += glm.vec3(2, 0, 0)  # Next molecule to the right
            
            return True
            
        except Exception as e:
            print(f"Error loading molecule: {e}")
            return False
    
    def load_molecule_from_json(self, file_path):
        """Load single molecule from JSON file (clears existing scene)"""
        self.clear_scene()
        return self.add_molecule_from_json(file_path, glm.vec3(0, 0, 0))
    
    def clear_scene(self):
        """Clear all molecules from scene"""
        self.atoms = []
        self.molecule_groups = []
        self.current_group_offset = glm.vec3(0, 0, 0)
        
    def load_from_space(self):
        """Load atoms from Space object"""
        if not self.space or not self.space.atoms:
            return
            
        self.atoms = []
        
        # Find bounds for centering
        if len(self.space.atoms) > 0:
            min_x = min(atom.pos.x for atom in self.space.atoms)
            max_x = max(atom.pos.x for atom in self.space.atoms)
            min_y = min(atom.pos.y for atom in self.space.atoms)
            max_y = max(atom.pos.y for atom in self.space.atoms)
            min_z = min(atom.pos.z for atom in self.space.atoms)
            max_z = max(atom.pos.z for atom in self.space.atoms)
            
            center_x = (min_x + max_x) / 2
            center_y = (min_y + max_y) / 2
            center_z = (min_z + max_z) / 2
        else:
            center_x = center_y = center_z = 0
            
        for space_atom in self.space.atoms:
            # Convert coordinates
            x = (space_atom.pos.x - center_x) * 0.001
            y = (space_atom.pos.y - center_y) * 0.001
            z = (space_atom.pos.z - center_z) * 0.001
            
            # Get properties
            props = self.get_atom_color_and_radius(space_atom.type)
            
            atom = {
                'pos': glm.vec3(x, y, z),
                'color': props['color'],
                'radius': props['radius'],
                'type': space_atom.type
            }
            self.atoms.append(atom)
            
        print(f"Loaded {len(self.atoms)} atoms from Space")

    def initializeGL(self):
        print("=== MyChem3D macOS Compatible OpenGL ===")
        
        # Safe OpenGL info retrieval
        vendor = glGetString(GL_VENDOR)
        renderer = glGetString(GL_RENDERER) 
        version = glGetString(GL_VERSION)
        glsl_version = glGetString(GL_SHADING_LANGUAGE_VERSION)
        
        print("Vendor:", vendor.decode() if vendor else "Unknown")
        print("Renderer:", renderer.decode() if renderer else "Unknown")
        print("Version:", version.decode() if version else "Unknown")
        print("GLSL Version:", glsl_version.decode() if glsl_version else "Unknown")
        
        glClearColor(0.1, 0.1, 0.2, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Create simple shaders
        self.create_shaders()
        self.create_sphere()
        
    def create_shaders(self):
        """Create basic GLSL 1.20 shaders"""
        vertex_source = """
        #version 120
        attribute vec3 position;
        attribute vec3 normal;
        uniform mat4 mvp;
        uniform vec4 color;
        varying vec4 vertColor;
        varying vec3 vertNormal;
        
        void main() {
            gl_Position = mvp * vec4(position, 1.0);
            vertColor = color;
            vertNormal = normal;
        }
        """
        
        fragment_source = """
        #version 120
        varying vec4 vertColor;
        varying vec3 vertNormal;
        
        void main() {
            vec3 light = normalize(vec3(1.0, 1.0, 1.0));
            float intensity = max(dot(normalize(vertNormal), light), 0.3);
            gl_FragColor = vec4(vertColor.rgb * intensity, vertColor.a);
        }
        """
        
        # Compile shaders
        vertex_shader = self.compile_shader(vertex_source, GL_VERTEX_SHADER)
        fragment_shader = self.compile_shader(fragment_source, GL_FRAGMENT_SHADER)
        
        if not vertex_shader or not fragment_shader:
            print("Shader compilation failed!")
            return
            
        # Create program
        self.program = glCreateProgram()
        glAttachShader(self.program, vertex_shader)
        glAttachShader(self.program, fragment_shader)
        glLinkProgram(self.program)
        
        if not glGetProgramiv(self.program, GL_LINK_STATUS):
            error = glGetProgramInfoLog(self.program).decode()
            print(f"Shader linking failed: {error}")
            return
            
        # Get locations
        self.mvp_loc = glGetUniformLocation(self.program, "mvp")
        self.color_loc = glGetUniformLocation(self.program, "color")
        self.position_loc = glGetAttribLocation(self.program, "position")
        self.normal_loc = glGetAttribLocation(self.program, "normal")
        
        print("Shaders created successfully!")
        
    def compile_shader(self, source, shader_type):
        shader = glCreateShader(shader_type)
        glShaderSource(shader, source)
        glCompileShader(shader)
        
        if not glGetShaderiv(shader, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(shader).decode()
            print(f"Shader compilation error: {error}")
            return None
        return shader
        
    def create_sphere(self):
        """Create simple sphere geometry"""
        vertices = []
        
        # Simple UV sphere
        lat_segments = 12
        lon_segments = 12
        
        for lat in range(lat_segments + 1):
            theta = lat * pi / lat_segments
            sin_theta = sin(theta)
            cos_theta = cos(theta)
            
            for lon in range(lon_segments + 1):
                phi = lon * 2 * pi / lon_segments
                sin_phi = sin(phi)
                cos_phi = cos(phi)
                
                x = cos_phi * sin_theta
                y = cos_theta
                z = sin_phi * sin_theta
                
                # Position and normal (same for unit sphere)
                vertices.extend([x, y, z, x, y, z])
        
        self.sphere_vertices = np.array(vertices, dtype=np.float32)
        self.sphere_vbo = vbo.VBO(self.sphere_vertices)
        
        # Create indices
        indices = []
        for lat in range(lat_segments):
            for lon in range(lon_segments):
                first = lat * (lon_segments + 1) + lon
                second = first + lon_segments + 1
                
                indices.extend([first, second, first + 1])
                indices.extend([second, second + 1, first + 1])
        
        self.sphere_indices = np.array(indices, dtype=np.uint32)
        self.num_indices = len(self.sphere_indices)
        
        # Create index buffer
        self.ibo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ibo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.sphere_indices.nbytes, self.sphere_indices, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        
    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        if not hasattr(self, 'program'):
            return
            
        glUseProgram(self.program)
        
        # Update rotation
        self.rotation += 1.0
        
        # Create matrices
        view = glm.lookAt(self.camera_pos, self.camera_target, glm.vec3(0, 1, 0))
        projection = glm.perspective(glm.radians(45), self.width()/self.height() if self.height() > 0 else 1, 0.1, 100.0)
        
        # Render atoms
        self.sphere_vbo.bind()
        
        if self.position_loc >= 0:
            glEnableVertexAttribArray(self.position_loc)
            glVertexAttribPointer(self.position_loc, 3, GL_FLOAT, GL_FALSE, 24, None)
            
        if self.normal_loc >= 0:
            glEnableVertexAttribArray(self.normal_loc)
            glVertexAttribPointer(self.normal_loc, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ibo)
        
        for atom in self.atoms:
            # Model matrix
            model = glm.mat4(1.0)
            model = model * glm.translate(glm.mat4(1.0), atom['pos'])
            model = model * glm.scale(glm.mat4(1.0), glm.vec3(atom['radius']))
            model = model * glm.rotate(glm.mat4(1.0), glm.radians(self.rotation), glm.vec3(0, 1, 0))
            
            mvp = projection * view * model
            
            # Set uniforms
            glUniformMatrix4fv(self.mvp_loc, 1, GL_FALSE, glm.value_ptr(mvp))
            glUniform4f(self.color_loc, atom['color'].x, atom['color'].y, atom['color'].z, atom['color'].w)
            
            # Draw
            glDrawElements(GL_TRIANGLES, self.num_indices, GL_UNSIGNED_INT, None)
        
        # Cleanup
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        if self.position_loc >= 0:
            glDisableVertexAttribArray(self.position_loc)
        if self.normal_loc >= 0:
            glDisableVertexAttribArray(self.normal_loc)
        self.sphere_vbo.unbind()
        glUseProgram(0)

class MyChem3DMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MyChem3D - macOS Compatible")
        self.setGeometry(100, 100, 800, 600)
        
        # Create Space
        self.space = Space()
        
        # Create GL widget
        self.gl_widget = MyChem3DGLWidget(self.space)
        self.setCentralWidget(self.gl_widget)
        
        # Create menu
        self.create_menu()
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("MyChem3D macOS Compatible - Ready")
        
    def create_menu(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        load_action = QAction('Load Molecule...', self)
        load_action.triggered.connect(self.load_molecule)
        file_menu.addAction(load_action)
        
        add_action = QAction('Add Molecule to Scene...', self)
        add_action.triggered.connect(self.add_molecule)
        file_menu.addAction(add_action)
        
        file_menu.addSeparator()
        
        clear_action = QAction('Clear Scene', self)
        clear_action.triggered.connect(self.clear_scene_action)
        file_menu.addAction(clear_action)
        
        file_menu.addSeparator()
        
        # Quick load submenu
        quick_menu = file_menu.addMenu('Quick Load')
        
        water_action = QAction('Water (H2O)', self)
        water_action.triggered.connect(lambda: self.quick_load('examples/simple/H2O.json'))
        quick_menu.addAction(water_action)
        
        methane_action = QAction('Methane (CH4)', self)
        methane_action.triggered.connect(lambda: self.quick_load('examples/alkane/methane.json'))
        quick_menu.addAction(methane_action)
        
        co2_action = QAction('Carbon Dioxide (CO2)', self)
        co2_action.triggered.connect(lambda: self.quick_load('examples/simple/Co2.json'))
        quick_menu.addAction(co2_action)
        
        ammonia_action = QAction('Ammonia (NH3)', self)
        ammonia_action.triggered.connect(lambda: self.quick_load('examples/simple/NH3.json'))
        quick_menu.addAction(ammonia_action)
        
        quick_menu.addSeparator()
        
        # Complex molecules submenu
        complex_menu = quick_menu.addMenu('Complex Molecules')
        
        fullerene_action = QAction('Fullerene (C60)', self)
        fullerene_action.triggered.connect(lambda: self.quick_load('examples/nanotubes/fullerene.json'))
        complex_menu.addAction(fullerene_action)
        
        nanotube_action = QAction('Carbon Nanotube', self)
        nanotube_action.triggered.connect(lambda: self.quick_load('examples/nanotubes/nanotube108.json'))
        complex_menu.addAction(nanotube_action)
        
        atp_action = QAction('ATP (Energy Molecule)', self)
        atp_action.triggered.connect(lambda: self.quick_load('examples/life/ATP.json'))
        complex_menu.addAction(atp_action)
        
        benzene_action = QAction('Benzene Ring', self)
        benzene_action.triggered.connect(lambda: self.quick_load('examples/cyclic/benzene.json'))
        complex_menu.addAction(benzene_action)
        
        caffeine_action = QAction('Caffeine', self)
        caffeine_action.triggered.connect(lambda: self.quick_load('examples/cyclic/geterocyclic/caffeine.json'))
        complex_menu.addAction(caffeine_action)
        
        quick_menu.addSeparator()
        
        # Create Scene submenu
        scene_menu = quick_menu.addMenu('Create Scene')
        
        biochem_action = QAction('Biochemistry Demo', self)
        biochem_action.triggered.connect(self.create_biochemistry_scene)
        scene_menu.addAction(biochem_action)
        
        organic_action = QAction('Organic Chemistry', self)
        organic_action.triggered.connect(self.create_organic_scene)
        scene_menu.addAction(organic_action)
        
        nano_action = QAction('Nanotechnology', self)
        nano_action.triggered.connect(self.create_nano_scene)
        scene_menu.addAction(nano_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def load_molecule(self):
        """Open file dialog to load molecule"""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self,
            "Load Molecule",
            "examples/",
            "JSON files (*.json);;All files (*)"
        )
        
        if file_path:
            if self.load_molecule_file(file_path):
                atom_count = len(self.space.atoms)
                self.status_bar.showMessage(f"Loaded {os.path.basename(file_path)} - {atom_count} atoms")
            else:
                QMessageBox.warning(self, "Error", "Failed to load molecule file")
                
    def quick_load(self, file_path):
        """Quick load predefined molecules"""
        if os.path.exists(file_path):
            if self.load_molecule_file(file_path):
                atom_count = len(self.space.atoms)
                self.status_bar.showMessage(f"Loaded {os.path.basename(file_path)} - {atom_count} atoms")
            else:
                QMessageBox.warning(self, "Error", f"Failed to load {file_path}")
        else:
            QMessageBox.warning(self, "Error", f"File not found: {file_path}")
            
    def load_molecule_file(self, file_path):
        """Load molecule from file into both Space and GL widget"""
        try:
            # Load into Space
            with open(file_path, 'r') as f:
                data = json.load(f)
                
            if 'atoms' not in data:
                return False
                
            # Clear existing atoms
            self.space.atoms.clear()
            
            # Load atoms into Space
            for atom_data in data['atoms']:
                atom = Atom(
                    atom_data['x'], 
                    atom_data['y'], 
                    atom_data['z'], 
                    atom_data['type']
                )
                if 'r' in atom_data:
                    atom.r = atom_data['r']
                if 'm' in atom_data:
                    atom.m = atom_data['m']
                if 'q' in atom_data:
                    atom.q = atom_data['q']
                    
                self.space.atoms.append(atom)
            
            # Load into GL widget for rendering
            result = self.gl_widget.load_molecule_from_json(file_path)
            
            print(f"Loaded {len(self.space.atoms)} atoms into Space and GL widget")
            return result
            
        except Exception as e:
            print(f"Error loading molecule: {e}")
            return False
            
    def add_molecule(self):
        """Add molecule to existing scene"""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self,
            "Add Molecule to Scene",
            "examples/",
            "JSON files (*.json);;All files (*)"
        )
        
        if file_path:
            if self.gl_widget.add_molecule_from_json(file_path):
                atom_count = len(self.gl_widget.atoms)
                group_count = len(self.gl_widget.molecule_groups)
                self.status_bar.showMessage(f"Added {os.path.basename(file_path)} - Scene: {group_count} molecules, {atom_count} atoms")
            else:
                QMessageBox.warning(self, "Error", "Failed to add molecule to scene")
    
    def clear_scene_action(self):
        """Clear all molecules from scene"""
        self.gl_widget.clear_scene()
        self.space.atoms.clear()
        self.status_bar.showMessage("Scene cleared")
    
    def create_biochemistry_scene(self):
        """Create a biochemistry demonstration scene"""
        self.gl_widget.clear_scene()
        self.space.atoms.clear()
        
        # Add water molecules
        if os.path.exists('examples/simple/H2O.json'):
            self.gl_widget.add_molecule_from_json('examples/simple/H2O.json', glm.vec3(-2, 0, 0))
            self.gl_widget.add_molecule_from_json('examples/simple/H2O.json', glm.vec3(-1, 1, 0))
            self.gl_widget.add_molecule_from_json('examples/simple/H2O.json', glm.vec3(-1, -1, 0))
        
        # Add ATP (energy molecule)
        if os.path.exists('examples/life/ATP.json'):
            self.gl_widget.add_molecule_from_json('examples/life/ATP.json', glm.vec3(1, 0, 0))
        
        # Add amino acid
        if os.path.exists('examples/aminoacids/glycine.json'):
            self.gl_widget.add_molecule_from_json('examples/aminoacids/glycine.json', glm.vec3(0, 2, 0))
        
        atom_count = len(self.gl_widget.atoms)
        group_count = len(self.gl_widget.molecule_groups)
        self.status_bar.showMessage(f"Biochemistry scene created - {group_count} molecules, {atom_count} atoms")
    
    def create_organic_scene(self):
        """Create an organic chemistry demonstration scene"""
        self.gl_widget.clear_scene()
        self.space.atoms.clear()
        
        # Add methane
        if os.path.exists('examples/alkane/methane.json'):
            self.gl_widget.add_molecule_from_json('examples/alkane/methane.json', glm.vec3(-2, 0, 0))
        
        # Add benzene
        if os.path.exists('examples/cyclic/benzene.json'):
            self.gl_widget.add_molecule_from_json('examples/cyclic/benzene.json', glm.vec3(0, 0, 0))
        
        # Add caffeine
        if os.path.exists('examples/cyclic/geterocyclic/caffeine.json'):
            self.gl_widget.add_molecule_from_json('examples/cyclic/geterocyclic/caffeine.json', glm.vec3(2, 0, 0))
        
        atom_count = len(self.gl_widget.atoms)
        group_count = len(self.gl_widget.molecule_groups)
        self.status_bar.showMessage(f"Organic chemistry scene created - {group_count} molecules, {atom_count} atoms")
    
    def create_nano_scene(self):
        """Create a nanotechnology demonstration scene"""
        self.gl_widget.clear_scene()
        self.space.atoms.clear()
        
        # Add fullerene
        if os.path.exists('examples/nanotubes/fullerene.json'):
            self.gl_widget.add_molecule_from_json('examples/nanotubes/fullerene.json', glm.vec3(0, 0, 0))
        
        # Add carbon nanotube
        if os.path.exists('examples/nanotubes/nanotube108.json'):
            self.gl_widget.add_molecule_from_json('examples/nanotubes/nanotube108.json', glm.vec3(3, 0, 0))
        
        atom_count = len(self.gl_widget.atoms)
        group_count = len(self.gl_widget.molecule_groups)
        self.status_bar.showMessage(f"Nanotechnology scene created - {group_count} molecules, {atom_count} atoms")
    
    def show_about(self):
        QMessageBox.about(self, "About", 
                         "MyChem3D macOS Compatible\n\n"
                         "OpenGL 2.1 / GLSL 1.20 compatible\n"
                         "3D Molecular Visualization\n\n"
                         "Features:\n"
                         "• Single and multiple molecule loading\n"
                         "• Complex molecule support (Fullerene, ATP, etc.)\n"
                         "• Scene composition tools\n"
                         "• Automatic OpenGL detection\n\n"
                         "Automatically loaded for macOS M1 and older systems.")

def main():
    print("=== MyChem3D macOS Compatible ===")
    print("Starting OpenGL 2.1 compatible version...")
    
    app = QApplication(sys.argv)
    
    try:
        window = MyChem3DMainWindow()
        window.show()
        
        print("MyChem3D macOS Compatible window opened successfully!")
        print("Use File menu to load molecules from examples/")
        
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()