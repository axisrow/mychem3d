#!/usr/bin/env python3
"""
MyChem3D - 3D Molecular Visualization Tool

Main entry point with automatic OpenGL version detection.
Supports both modern OpenGL 4.3+ and legacy OpenGL 2.1+ systems.
"""

import os
import sys
import platform
import traceback
import time
from typing import cast # Import cast for type hinting

# GUI imports
try:
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                                QWidget, QPushButton, QLabel, QFrame, QTextEdit, QGroupBox, QStyle) # Import QStyle
    from PyQt5.QtCore import Qt, QTimer
    from PyQt5.QtGui import QFont, QPalette, QColor, QPixmap, QIcon, QGuiApplication
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False

def add_src_to_path():
    """Add src directory to Python path"""
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

def detect_opengl_support():
    """Detect OpenGL version and capabilities"""
    try:
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtOpenGL import QGLWidget
        from OpenGL import GL
        
        print("🔍 Detecting OpenGL capabilities...")
        
        # Create temporary app if needed
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
            temp_app = True
        else:
            temp_app = False
            
        # Create temporary OpenGL context
        widget = QGLWidget()
        widget.makeCurrent()
        
        # Get OpenGL version
        version_string = GL.glGetString(GL.GL_VERSION)
        if version_string:
            version_string = version_string.decode()
            print(f"📊 Detected OpenGL: {version_string}")
            
            # Parse version number
            version_parts = version_string.split()
            if len(version_parts) > 0:
                version_num = version_parts[0]
                try:
                    major, minor = map(int, version_num.split('.')[:2])
                    
                    # Check capabilities
                    if major > 4 or (major == 4 and minor >= 3):
                        print("✅ Full OpenGL 4.3+ support detected")
                        return "full"
                    else:
                        print(f"⚠️  OpenGL {major}.{minor} - using compatibility mode")
                        return "compat"
                except ValueError:
                    print("⚠️  Could not parse OpenGL version - using compatibility mode")
                    return "compat"
        
        if temp_app:
            app.quit()
            
    except Exception as e:
        print(f"⚠️  OpenGL detection failed: {e}")
        
    # Platform-based fallback
    if platform.system() == "Darwin":
        print("🍎 macOS detected - using compatibility mode")
        return "compat"
    else:
        print("🖥️  Assuming full OpenGL support")
        return "full"

def run_full_version():
    """Run full-featured OpenGL 4.3+ version"""
    try:
        print("🚀 Starting full-featured version...")
        from src.mychem3d import mychemApp
        app = mychemApp()
        time.sleep(1)
        app.run()
    except ImportError as e:
        print(f"❌ Failed to import full version: {e}")
        print("🔄 Falling back to compatibility version...")
        run_compat_version()
    except Exception as e:
        print(f"❌ Full version failed: {e}")
        traceback.print_exc()
        print("🔄 Falling back to compatibility version...")
        run_compat_version()

def run_compat_version():
    """Run OpenGL 2.1+ compatibility version"""
    try:
        print("🚀 Starting compatibility version...")
        from src.mychem3d_macos import main as compat_main
        compat_main()
    except ImportError as e:
        print(f"❌ Failed to import compatibility version: {e}")
        print("💡 Please check that all dependencies are installed:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Compatibility version failed: {e}")
        traceback.print_exc()
        sys.exit(1)

def show_help():
    """Show help information"""
    print("""
MyChem3D - 3D Molecular Visualization Tool

Usage:
    python main.py [options]

Options:
    --help, -h      Show this help message
    --gui           Force GUI launcher (default if PyQt5 available)
    --cli           Force command-line mode (no GUI)
    --demo          Quick Demo - Water molecule (H2O)
    --complex       Complex Demo - Fullerene (C60)
    --full          Force full OpenGL 4.3+ version
    --compat        Force compatibility OpenGL 2.1+ version
    --version       Show version information

Examples:
    python main.py                 # Show GUI launcher (default)
    python main.py --demo          # Quick water molecule demo
    python main.py --complex       # Fullerene (C60) demo
    python main.py --cli           # Command-line auto-detection
    python main.py --compat        # Force compatibility mode
    python main.py --full          # Force full-featured mode

GUI Features:
    • Visual OpenGL detection with system information
    • Color-coded recommendations (green = recommended)
    • Quick Demo and Complex Molecule testing
    • Built-in help and documentation
    • Modern, user-friendly interface

Requirements:
    - Python 3.7+
    - PyQt5 (for GUI launcher)
    - OpenGL 2.1+ (compatibility mode) or 4.3+ (full mode)
    - NumPy, PyGLM, PIL

For more information, see README.md
""")

class MyChem3DLauncher(QMainWindow):
    """GUI Launcher for MyChem3D with OpenGL detection and version selection"""
    
    def __init__(self):
        super().__init__()
        self.opengl_mode = None
        self.selected_action = None
        self.init_ui()
        self.detect_system()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("🧪 MyChem3D Launcher")
        self.setFixedSize(600, 500)
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #f0f0f5, stop:1 #e8e8f0);
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 8px;
                margin: 10px;
                padding-top: 15px;
                background: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 10px;
                color: #333;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f0f0f0);
                border: 2px solid #cccccc;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
                color: #333;
                min-height: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e8f4fd, stop:1 #d0e8fc);
                border-color: #4CAF50;
            }
            QPushButton:pressed {
                background: #c0c0c0;
            }
            .recommended {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #d4edda, stop:1 #c3e6cb);
                border-color: #4CAF50;
                color: #155724;
            }
            .warning {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #fff3cd, stop:1 #ffeaa7);
                border-color: #ffc107;
                color: #856404;
            }
            QLabel {
                color: #333;
                font-size: 11px;
            }
            .title {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
            }
            .subtitle {
                font-size: 12px;
                color: #7f8c8d;
            }
        """)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(10)
        
        # Title
        title_label = QLabel("🧪 MyChem3D - 3D Molecular Visualization")
        title_label.setProperty("class", "title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        subtitle_label = QLabel("Advanced molecular visualization with automatic OpenGL detection")
        subtitle_label.setProperty("class", "subtitle")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle_label)
        
        # System info group
        self.system_group = QGroupBox("🖥️ System Information")
        system_layout = QVBoxLayout(self.system_group)
        self.system_info_label = QLabel("Detecting system capabilities...")
        self.opengl_info_label = QLabel("Scanning OpenGL support...")
        system_layout.addWidget(self.system_info_label)
        system_layout.addWidget(self.opengl_info_label)
        layout.addWidget(self.system_group)
        
        # Version selection group
        version_group = QGroupBox("🚀 Version Selection")
        version_layout = QVBoxLayout(version_group)
        
        # Auto-detect button
        self.auto_btn = QPushButton("🔍 Auto-Detect (Recommended)")
        self.auto_btn.setProperty("class", "recommended")
        self.auto_btn.clicked.connect(self._launch_auto_version)
        version_layout.addWidget(self.auto_btn)
        
        # Full version button
        self.full_btn = QPushButton("⚡ Full-Featured Version (OpenGL 4.3+)")
        self.full_btn.clicked.connect(self._launch_full_version)
        version_layout.addWidget(self.full_btn)
        
        # Compatibility button
        self.compat_btn = QPushButton("🛡️ Compatibility Version (OpenGL 2.1+)")
        self.compat_btn.clicked.connect(self._launch_compat_version)
        version_layout.addWidget(self.compat_btn)
        
        layout.addWidget(version_group)
        
        # Quick actions group
        actions_group = QGroupBox("⚡ Quick Actions")
        actions_layout = QHBoxLayout(actions_group)
        
        demo_btn = QPushButton("🧬 Quick Demo")
        demo_btn.clicked.connect(self.quick_demo)
        actions_layout.addWidget(demo_btn)
        
        test_btn = QPushButton("🔬 Test Complex")
        test_btn.clicked.connect(self.test_complex)
        actions_layout.addWidget(test_btn)
        
        help_btn = QPushButton("❓ Help")
        help_btn.clicked.connect(self.show_help_gui)
        actions_layout.addWidget(help_btn)
        
        layout.addWidget(actions_group)
        
        # Exit button
        exit_btn = QPushButton("❌ Exit")
        exit_btn.clicked.connect(self._handle_exit)
        layout.addWidget(exit_btn)
        
        # Status bar equivalent
        self.status_label = QLabel("Ready to launch MyChem3D...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
        layout.addWidget(self.status_label)
        
    def detect_system(self):
        """Detect system capabilities in background"""
        # Update system info immediately
        system_info = f"Platform: {platform.system()} {platform.release()}"
        if platform.system() == "Darwin":
            system_info += f" ({platform.machine()})"
        self.system_info_label.setText(system_info)
        
        # Set up timer for OpenGL detection
        QTimer.singleShot(500, self.detect_opengl_async)
        
    def detect_opengl_async(self):
        """Detect OpenGL capabilities asynchronously"""
        try:
            self.opengl_mode = detect_opengl_support()
            
            if self.opengl_mode == "full":
                opengl_text = "✅ OpenGL 4.3+ detected - Full features available"
                self.auto_btn.setText("🔍 Auto-Detect → Full Version (Recommended)")
                self.full_btn.setProperty("class", "recommended")
                self.compat_btn.setProperty("class", "")
            else:
                opengl_text = "⚠️ OpenGL 2.1 detected - Compatibility mode recommended"
                self.auto_btn.setText("🔍 Auto-Detect → Compatibility Version (Recommended)")
                self.compat_btn.setProperty("class", "recommended")
                self.full_btn.setProperty("class", "warning")
                
            self.opengl_info_label.setText(opengl_text)
            
            # Refresh styles
            # Use QApplication.style() directly for Pylance compatibility
            app_style = cast(QStyle, QApplication.style())
            if app_style: # Ensure style object exists
                app_style.unpolish(self.full_btn)
                app_style.polish(self.full_btn)
                app_style.unpolish(self.compat_btn)
                app_style.polish(self.compat_btn)
            
            self.status_label.setText("System detection complete. Choose your preferred version.")
            
        except Exception as e:
            self.opengl_info_label.setText(f"❌ Detection failed: {str(e)}")
            self.status_label.setText("Detection failed, but you can still choose manually.")
    
    def launch_version(self, version):
        """Launch selected version with proper event loop handling"""
        self.status_label.setText(f"Starting {version} version...")
        
        # Close the launcher properly and schedule the launch
        self.version_to_launch = version
        QTimer.singleShot(100, self.delayed_launch)
        self.close()
    
    def delayed_launch(self):
        """Launch the selected version after GUI is closed"""
        print(f"🚀 Delayed launch triggered for version: {getattr(self, 'version_to_launch', 'unknown')}")
        
        # Hide the launcher window but keep QApplication running
        self.hide()
        
        # Launch immediately without quitting the app
        self.do_launch()
    
    def do_launch(self):
        """Actually launch the version"""
        try:
            version = getattr(self, 'version_to_launch', 'auto')
            print(f"🎯 Launching version: {version}")
            
            # Try direct launch first (preferred)
            if version == "auto":
                if self.opengl_mode == "full":
                    print("🔧 Launching full version...")
                    self.launch_direct_full()
                else:
                    print("🔧 Launching compatibility version...")
                    self.launch_direct_compat()
            elif version == "full":
                print("🔧 Launching full version...")
                self.launch_direct_full()
            elif version == "compat":
                print("🔧 Launching compatibility version...")
                self.launch_direct_compat()
                
        except Exception as e:
            print(f"❌ Launch failed: {str(e)}")
            import traceback
            traceback.print_exc()
            # Show launcher again on failure
            self.show()
    
    def launch_direct_compat(self):
        """Launch compatibility version directly in same process"""
        try:
            print("🔧 Importing compatibility version...")
            from src.mychem3d_macos import main as compat_main
            print("🚀 Starting compatibility version...")
            compat_main()
        except Exception as e:
            print(f"❌ Direct compatibility launch failed: {e}")
            # Fallback to subprocess
            self.launch_subprocess_compat()
    
    def launch_direct_full(self):
        """Launch full version directly in same process"""
        try:
            print("🔧 Importing full version...")
            from src.mychem3d import mychemApp
            print("🚀 Starting full version...")
            app = mychemApp()
            app.run()
        except Exception as e:
            print(f"❌ Direct full launch failed: {e}")
            # Fallback to subprocess
            self.launch_subprocess_full()
    
    def launch_subprocess_compat(self):
        """Fallback: launch compatibility version in subprocess"""
        import subprocess
        print("🔄 Falling back to subprocess launch...")
        try:
            subprocess.Popen([sys.executable, sys.argv[0], '--compat'])
            # Close launcher after successful subprocess launch
            QTimer.singleShot(1000, self._close_launcher)
        except Exception as e:
            print(f"❌ Subprocess launch failed: {e}")
            self.show()
    
    def launch_subprocess_full(self):
        """Fallback: launch full version in subprocess"""
        import subprocess
        print("🔄 Falling back to subprocess launch...")
        try:
            subprocess.Popen([sys.executable, sys.argv[0], '--full'])
            # Close launcher after successful subprocess launch
            QTimer.singleShot(1000, self._close_launcher)
        except Exception as e:
            print(f"❌ Subprocess launch failed: {e}")
            self.show()

    def _launch_auto_version(self):
        """Helper to launch auto version"""
        self.launch_version("auto")

    def _launch_full_version(self):
        """Helper to launch full version"""
        self.launch_version("full")

    def _launch_compat_version(self):
        """Helper to launch compatibility version"""
        self.launch_version("compat")
    def _handle_exit(self):
        """Handle exit button click by closing the window."""
        self.close()

    def _close_launcher(self):
        """Helper method to close the launcher window."""
        self.close()
    
    def quick_demo(self):
        """Launch with a quick demo"""
        self.status_label.setText("Starting quick demo...")
        # Set environment variable for demo mode
        os.environ['MYCHEM3D_DEMO'] = 'water'
        self.launch_version("auto")
    
    def test_complex(self):
        """Launch with complex molecule test"""
        self.status_label.setText("Starting complex molecule test...")
        # Set environment variable for complex test
        os.environ['MYCHEM3D_DEMO'] = 'fullerene'
        self.launch_version("auto")
    
    def show_help_gui(self):
        """Show help in GUI"""
        from PyQt5.QtWidgets import QDialog, QTextEdit, QVBoxLayout
        
        help_dialog = QDialog(self)
        help_dialog.setWindowTitle("MyChem3D Help")
        help_dialog.setFixedSize(500, 400)
        
        layout = QVBoxLayout(help_dialog)
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setPlainText("""
MyChem3D - 3D Molecular Visualization Tool

FEATURES:
• Dual OpenGL Support (4.3+ full features, 2.1+ compatibility)
• Complex molecule visualization (Fullerene, ATP, Nanotubes)
• Multiple molecule scenes
• Real-time 3D rendering
• Cross-platform support

VERSIONS:
• Full Version: Modern OpenGL 4.3+ with compute shaders
• Compatibility: OpenGL 2.1+ for older systems and macOS M1

QUICK START:
1. Use Auto-Detect for best experience
2. Try Quick Demo for immediate visualization
3. Test Complex molecules for advanced features

CONTROLS:
• Mouse + Left: Rotate camera
• Mouse + Right: Pan camera
• Mouse Wheel: Zoom in/out
• Shift + controls: Fine movement

SUPPORTED MOLECULES:
• Simple: Water, Methane, CO2, Ammonia
• Complex: Fullerene (C60), Carbon Nanotubes, ATP
• Organic: Benzene, Caffeine, Amino acids
• Create custom scenes with multiple molecules

For more information, see README.md
        """)
        layout.addWidget(text_edit)
        help_dialog.exec_()

def show_gui_launcher():
    """Show GUI launcher if PyQt5 is available"""
    if not GUI_AVAILABLE:
        return False
        
    # Ensure QApplication instance exists
    app = None
    if QApplication.instance() is None:
        app = QApplication(sys.argv)
        should_exec = True
    else:
        app = QApplication.instance()
        should_exec = False
    
    launcher = MyChem3DLauncher()
    launcher.show()
    
    # Center window on screen
    primary_screen = QGuiApplication.primaryScreen()
    if primary_screen: # Check if primaryScreen is not None
        screen_geometry = primary_screen.geometry()
        launcher.move(
            (screen_geometry.width() - launcher.width()) // 2,
            (screen_geometry.height() - launcher.height()) // 2
        )
    else:
        print("Warning: Could not get primary screen geometry. Window may not be centered.")
    
    # Only exec if we created the QApplication
    if should_exec and app:
        cast(QApplication, app).exec_()
    
    return True

def main():
    """Main entry point"""
    # Add src to path first
    add_src_to_path()
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg in ['--help', '-h']:
            show_help()
            return
            
        elif arg == '--version':
            print("MyChem3D version 2.1 - OpenGL 2.1+ compatible")
            return
            
        elif arg == '--full':
            print("=" * 50)
            print("🧪 MyChem3D - 3D Molecular Visualization")
            print("=" * 50)
            print("🔧 Forcing full-featured mode...")
            run_full_version()
            return
            
        elif arg == '--compat':
            print("=" * 50)
            print("🧪 MyChem3D - 3D Molecular Visualization")
            print("=" * 50)
            print("🔧 Forcing compatibility mode...")
            run_compat_version()
            return
            
        elif arg == '--cli':
            # CLI mode - original behavior
            print("=" * 50)
            print("🧪 MyChem3D - 3D Molecular Visualization")
            print("=" * 50)
            
            # Auto-detect OpenGL capabilities
            opengl_mode = detect_opengl_support()
            
            # Run appropriate version
            if opengl_mode == "full":
                run_full_version()
            else:
                run_compat_version()
            return
            
        elif arg == '--demo':
            # Quick Demo - Water molecule
            print("=" * 50)
            print("🧪 MyChem3D - Quick Demo (Water)")
            print("=" * 50)
            os.environ['MYCHEM3D_DEMO'] = 'water'
            print("🧬 Starting Quick Demo with water molecule...")
            run_compat_version()
            return
            
        elif arg == '--complex':
            # Test Complex - Fullerene molecule
            print("=" * 50)
            print("🧪 MyChem3D - Complex Demo (Fullerene)")
            print("=" * 50)
            os.environ['MYCHEM3D_DEMO'] = 'fullerene'
            print("🔬 Starting Complex Demo with fullerene (C60)...")
            run_compat_version()
            return
            
        elif arg == '--gui':
            # Force GUI mode
            if show_gui_launcher():
                return
            else:
                print("❌ GUI not available (PyQt5 not installed)")
                print("Falling back to CLI mode...")
                
        else:
            print(f"❌ Unknown argument: {arg}")
            print("Use --help for usage information")
            return
    
    # Default behavior: Try GUI first, fallback to CLI
    if GUI_AVAILABLE:
        try:
            show_gui_launcher()
            return
        except Exception as e:
            print(f"⚠️ GUI launcher failed: {e}")
            print("Falling back to CLI mode...")
    
    # Fallback to CLI mode
    print("=" * 50)
    print("🧪 MyChem3D - 3D Molecular Visualization")
    print("=" * 50)
    print("💡 Tip: Install PyQt5 for GUI launcher")
    
    # Auto-detect OpenGL capabilities
    opengl_mode = detect_opengl_support()
    
    # Run appropriate version
    if opengl_mode == "full":
        run_full_version()
    else:
        run_compat_version()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        traceback.print_exc()
        sys.exit(1)
