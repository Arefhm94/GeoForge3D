"""Building Terrain Modeler GUI Main Window"""
import os
from typing import List, Optional, Dict

from PySide6.QtWidgets import (QMainWindow, QWidget, QPushButton, QLabel, QLineEdit, 
                              QTextEdit, QFileDialog, QProgressBar, QFrame, QSplitter, QTabWidget)
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QSizePolicy, QMessageBox
from PySide6.QtCore import Qt, QUrl, QSettings
from PySide6.QtGui import QFont, QCloseEvent
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineProfile
from vtkmodules.vtkRenderingCore import vtkRenderer, vtkActor
from vtkmodules.vtkRenderingOpenGL2 import vtkOpenGLPolyDataMapper
from vtkmodules.vtkIOGeometry import vtkSTLReader
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera

from src.gui.controls import ScriptWorker
from src.utils.file_handlers import handle_web_download


class MainWindow(QMainWindow):
    """
    Main window for the Building Terrain Modeler application.
    This window contains the main interface for user interaction, including
    file input, processing buttons, log area, and a web view for GeoJSON.io.
    """
    def __init__(self) -> None:
        """Initialize the main window and set up the UI components."""
        super().__init__()
        self.setWindowTitle("Building Terrain Modeler")
        
        # Application settings
        self.settings = QSettings("BuildingTerrainModeler", "Application")
        
        # Initialize state variables
        self.worker: Optional[ScriptWorker] = None
        self.stl_actors: Dict[str, vtkActor] = {}  # Track loaded STL actors
        
        # Set up main window size based on screen or saved settings
        self._setup_window_geometry()
        
        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create main horizontal splitter
        self.main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.main_splitter, 1)
        
        # Left sidebar for controls and logging
        self.sidebar = QWidget()
        self.sidebar.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(5, 5, 5, 5)
        
        # Right content area for web view and STL viewer
        self.content_area = QWidget()
        self.content_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        content_layout = QVBoxLayout(self.content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add both parts to the splitter
        self.main_splitter.addWidget(self.sidebar)
        self.main_splitter.addWidget(self.content_area)
        
        # Load saved splitter sizes or use defaults (30% sidebar, 70% content)
        self._restore_splitter_state()
        
        # Setup UI components
        self._setup_file_input(sidebar_layout)
        self._setup_script_buttons(sidebar_layout)
        self._setup_log_area(sidebar_layout)
        
        # Progress bar and status in sidebar
        self.progress_bar = QProgressBar()
        sidebar_layout.addWidget(self.progress_bar)
        
        self.status_bar = QLabel("Ready")
        self.status_bar.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        sidebar_layout.addWidget(self.status_bar)
        
        # Create tab widget for content area
        self.tabs = QTabWidget()
        content_layout.addWidget(self.tabs)
        
        # Setup web view in content area
        self._setup_web_view()
        
        # Set focus to path entry
        self.path_entry.setFocus()
    
    def _setup_window_geometry(self) -> None:
        """Set up the window geometry based on screen size or saved settings."""
        # Try to restore saved window geometry
        if self.settings.contains("geometry"):
            self.restoreGeometry(self.settings.value("geometry"))
        else:
            # Use default size based on screen resolution
            screen = self.screen()
            screen_rect = screen.availableGeometry()
            screen_width = screen_rect.width()
            screen_height = screen_rect.height()
            self.resize(int(screen_width * 0.8), int(screen_height * 0.8))
    
    def _restore_splitter_state(self) -> None:
        """Restore splitter state from saved settings or use defaults."""
        if self.settings.contains("splitterSizes"):
            self.main_splitter.restoreState(self.settings.value("splitterSizes"))
        else:
            # Set default sizes (30% sidebar, 70% content)
            self.main_splitter.setSizes([300, 700])
    
    def _setup_web_view(self) -> None:
        """Set up the web view component in a dedicated tab."""
        # Create a web view tab
        web_tab = QWidget()
        web_layout = QVBoxLayout(web_tab)
        web_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header for web view
        web_header_frame = QFrame()
        web_header_layout = QHBoxLayout(web_header_frame)
        web_header_layout.setContentsMargins(0, 0, 0, 0)
        web_header_layout.setSpacing(0)

        # Web header label and spacer
        web_label = QLabel("GeoJSON.io Map Editor")
        web_label.setFont(QFont("Arial", 10, QFont.Bold))
        web_header_layout.addWidget(web_label)
        
        spacer_web = QWidget()
        web_header_layout.addWidget(spacer_web, 1)
        
        # Reload button
        reload_button = QPushButton("Reload")
        reload_button.clicked.connect(self._reload_web_view)
        web_header_layout.addWidget(reload_button)

        web_layout.addWidget(web_header_frame)
        web_layout.setSpacing(0)

        # Set up download handler for the web view
        profile = QWebEngineProfile.defaultProfile()
        profile.downloadRequested.connect(self.handle_download)

        # Create web view
        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl("https://geojson.io/"))
        self.web_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.web_view.loadFinished.connect(self.on_page_load_finished)
        web_layout.addWidget(self.web_view, 1)
        
        # Add the web tab to the tab widget
        self.tabs.addTab(web_tab, "GeoJSON Editor")

    def _reload_web_view(self) -> None:
        """Reload the web view."""
        self.web_view.reload()
        self.log_area.append("Reloading GeoJSON.io editor...\n")
    
    def on_page_load_finished(self, ok: bool) -> None:
        """
        Handle webpage load completion and customize the GeoJSON.io interface.
        
        Args:
            ok: Boolean indicating if the page loaded successfully
        """
        if ok:
            # JavaScript to hide the sidebar in GeoJSON.io for more map space
            js_code = """
            """
            self.web_view.page().runJavaScript(js_code)
            self.log_area.append("GeoJSON editor loaded successfully.\n")
        else:
            self.log_area.append("Error: Failed to load GeoJSON editor.\n")
    
    def _setup_file_input(self, parent_layout: QVBoxLayout) -> None:
        """
        Set up the file input section.
        
        Args:
            parent_layout: The layout to add the file input section to
        """
        section_label = QLabel("File Input")
        section_label.setFont(QFont("Arial", 12, QFont.Bold))
        parent_layout.addWidget(section_label)
        
        file_frame = QFrame()
        file_layout = QHBoxLayout(file_frame)
        file_layout.setContentsMargins(0, 0, 0, 0)
        
        file_label = QLabel("GeoJSON File:")
        file_label.setFont(QFont("Arial", 10))
        file_layout.addWidget(file_label)
        
        self.path_entry = QLineEdit()
        self.path_entry.setFont(QFont("Arial", 10))
        self.path_entry.setPlaceholderText("Select or download a GeoJSON file...")
        
        # Restore last used file path if available
        last_path = self.settings.value("lastFilePath", "")
        if last_path and os.path.exists(last_path):
            self.path_entry.setText(last_path)
            
        file_layout.addWidget(self.path_entry, 1)  # stretch factor
        
        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self.browse_file)
        file_layout.addWidget(browse_button)
        
        parent_layout.addWidget(file_frame)
        
        # Add a separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        parent_layout.addWidget(separator)
    
    def _setup_script_buttons(self, parent_layout: QVBoxLayout) -> None:
        """
        Set up the script buttons section.
        
        Args:
            parent_layout: The layout to add the script buttons to
        """
        section_label = QLabel("Processing")
        section_label.setFont(QFont("Arial", 12, QFont.Bold))
        parent_layout.addWidget(section_label)
        
        button_frame = QFrame()
        button_layout = QVBoxLayout(button_frame)
        button_layout.setSpacing(10)
        
        buildings_button = QPushButton("Generate Building Models")
        buildings_button.setMinimumHeight(40)
        buildings_button.clicked.connect(self.run_create_buildings)
        buildings_button.setToolTip("Generate 3D building models from GeoJSON file")
        button_layout.addWidget(buildings_button)
        
        terrain_button = QPushButton("Generate Terrain Model")
        terrain_button.setMinimumHeight(40)
        terrain_button.clicked.connect(self.run_create_terrain)
        terrain_button.setToolTip("Generate 3D terrain model from GeoJSON file")
        button_layout.addWidget(terrain_button)
        
        export_button = QPushButton("Export STL Files")
        export_button.setMinimumHeight(40)
        export_button.clicked.connect(self.export_stl_files)
        export_button.setToolTip("Export 3D models as STL files")
        button_layout.addWidget(export_button)
        
        load_stl_button = QPushButton("Load STL File")
        load_stl_button.setMinimumHeight(40)
        load_stl_button.clicked.connect(self.load_stl_file)
        load_stl_button.setToolTip("View STL files in the 3D viewer")
        button_layout.addWidget(load_stl_button)
        
        parent_layout.addWidget(button_frame)
        
        # Add a separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        parent_layout.addWidget(separator)
    
    def _setup_log_area(self, parent_layout: QVBoxLayout) -> None:
        """
        Set up the log area section.
        
        Args:
            parent_layout: The layout to add the log area to
        """
        log_header_frame = QFrame()
        log_header_layout = QHBoxLayout(log_header_frame)
        log_header_layout.setContentsMargins(0, 0, 0, 0)
        
        log_header = QLabel("Process Log")
        log_header.setFont(QFont("Arial", 12, QFont.Bold))
        log_header_layout.addWidget(log_header)
        
        spacer = QWidget()
        log_header_layout.addWidget(spacer, 1)
        
        clear_button = QPushButton("Clear Log")
        clear_button.clicked.connect(self.clear_log)
        clear_button.setToolTip("Clear the log area")
        log_header_layout.addWidget(clear_button)
        
        save_log_button = QPushButton("Save Log")
        save_log_button.clicked.connect(self.save_log)
        save_log_button.setToolTip("Save the log to a file")
        log_header_layout.addWidget(save_log_button)
        
        parent_layout.addWidget(log_header_frame)
        
        self.log_area = QTextEdit()
        self.log_area.setFont(QFont("Courier", 9))
        self.log_area.setReadOnly(True)
        self.log_area.setMinimumHeight(200)  # Ensure log area has enough vertical space
        parent_layout.addWidget(self.log_area, 1)  # stretch factor to make it expand
        
        # Initial log message
        self.log_area.append("Building Terrain Modeler initialized and ready.\n")
    
    def browse_file(self) -> None:
        """Browse for a GeoJSON file."""
        # Get the directory of the current file path, if any
        current_path = self.path_entry.text()
        start_dir = os.path.dirname(current_path) if current_path else ""
        
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select GeoJSON File",
            start_dir,
            "GeoJSON files (*.geojson);;All files (*.*)"
        )
        if filename:
            self.path_entry.setText(filename)
            self.path_entry.setFocus()
            self.path_entry.selectAll()
            
            # Save the file path for future use
            self.settings.setValue("lastFilePath", filename)
            
            self.log_area.append(f"Selected file: {filename}\n")
    
    def save_log(self) -> None:
        """Save the log area content to a file."""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Log File",
            "",
            "Text files (*.txt);;All files (*.*)"
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.log_area.toPlainText())
                self.log_area.append(f"Log saved to: {filename}\n")
            except Exception as e:
                self.log_area.append(f"Error saving log: {str(e)}\n")
    
    def clear_log(self) -> None:
        """Clear the log area."""
        self.log_area.clear()
        self.log_area.append("Log cleared.\n")
        
    def run_script(self, script_path: str) -> None:
        """
        Run a script using the ScriptWorker thread.
        
        Args:
            script_path: Path to the script to run
        """
        # Validate file path before running
        file_path = self.path_entry.text()
        if not file_path:
            self.log_area.append("Error: No file selected. Please select a GeoJSON file.\n")
            QMessageBox.warning(self, "No File Selected", 
                                "Please select a GeoJSON file before running the script.")
            return
            
        if not os.path.exists(file_path):
            self.log_area.append(f"Error: File not found - {file_path}\n")
            QMessageBox.warning(self, "File Not Found", 
                                f"The selected file does not exist:\n{file_path}")
            return
            
        # Start progress bar animation and update status
        self.progress_bar.setRange(0, 0)  # Indeterminate mode
        self.status_bar.setText("Running script...")
        
        self.log_area.append(f"Running {script_path} with file: {file_path}\n")
        
        # Create and start worker thread
        self.worker = ScriptWorker(script_path, file_path)
        self.worker.output_ready.connect(self.update_log)
        self.worker.script_finished.connect(self.script_completed)
        self.worker.start()
    
    def update_log(self, text: str) -> None:
        """
        Update the log area with new text.
        
        Args:
            text: Text to append to the log area
        """
        self.log_area.append(text)
        # Scroll to bottom
        vbar = self.log_area.verticalScrollBar()
        vbar.setValue(vbar.maximum())
    
    def script_completed(self, return_code: int) -> None:
        """
        Handle script completion.
        
        Args:
            return_code: Return code from the script execution
        """
        self.log_area.append(f"Script completed with return code: {return_code}\n")
        # Reset progress bar and status
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100 if return_code == 0 else 0)
        self.status_bar.setText("Ready" if return_code == 0 else "Error")
        
        if return_code == 0:
            # Check if any output files were created
            self._check_for_output_files()
    
    def _check_for_output_files(self) -> None:
        """Check for output files created by the scripts and offer to load them."""
        # This would check common output directories for STL files
        output_dir = "./output"  # Adjust this to match your project structure
        
        if os.path.exists(output_dir):
            stl_files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) 
                        if f.lower().endswith('.stl')]
            
            if stl_files:
                self.log_area.append(f"Found {len(stl_files)} STL file(s) in output directory.\n")
                
                # Ask if user wants to load them
                response = QMessageBox.question(
                    self, 
                    "STL Files Found",
                    f"Found {len(stl_files)} STL file(s) in the output directory.\nWould you like to load them?",
                    QMessageBox.Yes | QMessageBox.No
                )
                
                if response == QMessageBox.Yes:
                    self.load_stl_models(stl_files)
    
    def run_create_buildings(self) -> None:
        """Run the building creation script."""
        self.run_script('src/modeling/building.py')
    
    def run_create_terrain(self) -> None:
        """Run the terrain creation script."""
        self.run_script('src/modeling/terrain.py')
    
    def export_stl_files(self) -> None:
        """Export models as STL files."""
        self.run_script('src/modeling/stl_export.py')

    def handle_download(self, download) -> None:
        """
        Handle file downloads from the web view.
        
        Args:
            download: The download request object
        """
        handle_web_download(self, download, self.path_entry, self.log_area)

    def load_stl_file(self) -> None:
        """Load one or more STL files and display them in the 3D viewer."""
        # Get the directory of the current file path, if any
        current_path = self.path_entry.text()
        start_dir = os.path.dirname(current_path) if current_path else ""
        
        filenames, _ = QFileDialog.getOpenFileNames(
            self,
            "Select STL Files",
            start_dir,
            "STL files (*.stl);;All files (*.*)"
        )
        if filenames:
            self.load_stl_models(filenames)

    def load_stl_models(self, filenames: List[str]) -> None:
        """
        Load and display STL models in the 3D viewer.
        
        Args:
            filenames: List of STL file paths to load
        """
        # Create or get the STL viewer tab
        stl_tab = self._get_or_create_stl_tab()
        
        # Load each STL file
        for filename in filenames:
            try:
                self._load_stl_file(filename)
                self.log_area.append(f"Loaded STL file: {os.path.basename(filename)}\n")
            except Exception as e:
                self.log_area.append(f"Error loading STL file {os.path.basename(filename)}: {str(e)}\n")
        
        # Reset camera to show all actors
        if self.renderer.GetActors().GetNumberOfItems() > 0:
            self.renderer.ResetCamera()
        
        # Render the scene
        self.vtk_widget.GetRenderWindow().Render()
        
        # Switch to the STL viewer tab
        self.tabs.setCurrentWidget(stl_tab)

    def _get_or_create_stl_tab(self) -> QWidget:
        """
        Get the existing STL viewer tab or create a new one if it doesn't exist.
        
        Returns:
            QWidget: The STL viewer tab
        """
        # Check if we already have an STL viewer tab
        stl_tab = None
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) == "STL Viewer":
                stl_tab = self.tabs.widget(i)
                break
                
        if stl_tab is None:
            # Create a new STL viewer tab
            stl_tab = QWidget()
            stl_layout = QVBoxLayout(stl_tab)
            stl_layout.setContentsMargins(0, 0, 0, 0)
            
            # Create a control panel at the top
            control_frame = QFrame()
            control_layout = QHBoxLayout(control_frame)
            control_layout.setContentsMargins(5, 5, 5, 5)
            
            # Add controls
            reset_view_button = QPushButton("Reset View")
            reset_view_button.clicked.connect(self._reset_stl_view)
            control_layout.addWidget(reset_view_button)
            
            clear_button = QPushButton("Clear All")
            clear_button.clicked.connect(self._clear_stl_view)
            control_layout.addWidget(clear_button)
            
            # Add spacer
            spacer = QWidget()
            control_layout.addWidget(spacer, 1)
            
            # Add filter control
            filter_label = QLabel("File Filter:")
            control_layout.addWidget(filter_label)
            
            self.filter_entry = QLineEdit()
            self.filter_entry.setPlaceholderText("Filter files by name...")
            self.filter_entry.textChanged.connect(self._apply_stl_filter)
            control_layout.addWidget(self.filter_entry)
            
            stl_layout.addWidget(control_frame)
            
            # Create VTK widget
            self.vtk_widget = QVTKRenderWindowInteractor(stl_tab)
            stl_layout.addWidget(self.vtk_widget, 1)  # Give it most of the space
            
            # Set up VTK components
            self.renderer = vtkRenderer()
            render_window = self.vtk_widget.GetRenderWindow()
            render_window.AddRenderer(self.renderer)
            
            self.interactor = render_window.GetInteractor()
            self.interactor.SetInteractorStyle(vtkInteractorStyleTrackballCamera())
            
            # Set up renderer properties
            self.renderer.SetBackground(0.1, 0.1, 0.1)  # Dark background
            
            # Initialize the STL actors dictionary if it doesn't exist
            if not hasattr(self, 'stl_actors'):
                self.stl_actors = {}
                
            # Add the tab to the tab widget
            self.tabs.addTab(stl_tab, "STL Viewer")
            
        return stl_tab
    
    def _load_stl_file(self, filename: str) -> None:
        """
        Load an STL file and add it to the renderer.
        
        Args:
            filename: Path to the STL file to load
        """
        # Check if the file already exists in our actors dictionary
        if filename in self.stl_actors:
            # File already loaded, make sure it's visible
            self.stl_actors[filename].VisibilityOn()
            return
            
        # Create STL reader
        reader = vtkSTLReader()
        reader.SetFileName(filename)
        reader.Update()
        
        # Check if the reader has output
        if reader.GetOutput().GetNumberOfPoints() == 0:
            raise ValueError("STL file contains no points")
            
        # Create mapper and actor
        mapper = vtkOpenGLPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())
        
        actor = vtkActor()
        actor.SetMapper(mapper)
        
        # Add actor to renderer
        self.renderer.AddActor(actor)
        
        # Store the actor in our dictionary
        self.stl_actors[filename] = actor
    
    def _reset_stl_view(self) -> None:
        """Reset the camera view to show all actors."""
        if hasattr(self, 'renderer'):
            self.renderer.ResetCamera()
            self.vtk_widget.GetRenderWindow().Render()
    
    def _clear_stl_view(self) -> None:
        """Clear all STL models from the viewer."""
        if hasattr(self, 'renderer') and hasattr(self, 'stl_actors'):
            # Ask for confirmation
            response = QMessageBox.question(
                self, 
                "Clear STL Viewer",
                "Are you sure you want to clear all models from the viewer?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if response == QMessageBox.Yes:
                # Remove all actors from the renderer
                for actor in self.stl_actors.values():
                    self.renderer.RemoveActor(actor)
                    
                # Clear the actors dictionary
                self.stl_actors.clear()
                
                # Update the display
                self.vtk_widget.GetRenderWindow().Render()
                self.log_area.append("Cleared all models from STL viewer.\n")
    
    def _apply_stl_filter(self, filter_text: str) -> None:
        """
        Apply a filter to show/hide STL models based on filename.
        
        Args:
            filter_text: Text to filter filenames by
        """
        if hasattr(self, 'stl_actors'):
            filter_text = filter_text.lower()
            
            for filename, actor in self.stl_actors.items():
                base_name = os.path.basename(filename).lower()
                
                if not filter_text or filter_text in base_name:
                    actor.VisibilityOn()
                else:
                    actor.VisibilityOff()
                    
            # Update the display
            if hasattr(self, 'vtk_widget'):
                self.vtk_widget.GetRenderWindow().Render()
    
    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Handle the window close event.
        
        Args:
            event: The close event
        """
        # Save window state and settings
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("splitterSizes", self.main_splitter.saveState())
        
        # Save the last used file path
        file_path = self.path_entry.text()
        if file_path:
            self.settings.setValue("lastFilePath", file_path)
            
        # Accept the close event
        event.accept()
