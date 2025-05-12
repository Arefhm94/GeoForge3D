from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QLabel, QLineEdit, QTextEdit, QFileDialog, QProgressBar, QFrame, QSplitter)
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, QThread, Signal, QUrl
from PySide6.QtGui import QFont
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings
import subprocess
import sys
import os

# Replace the single flag with multiple flags
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu --disable-software-rasterizer --disable-dev-shm-usage"

# Worker thread for running scripts without freezing the GUI
class ScriptWorker(QThread):
    output_ready = Signal(str)
    script_finished = Signal(int)
    
    def __init__(self, script_path, file_path):
        super().__init__()
        self.script_path = script_path
        self.file_path = file_path
        
    def run(self):
        try:
            process = subprocess.Popen(
                [sys.executable, self.script_path, self.file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            
            for line in process.stdout:
                self.output_ready.emit(line)
                
            process.wait()
            self.script_finished.emit(process.returncode)
        except Exception as e:
            self.output_ready.emit(f"Error: {str(e)}\n")
            self.script_finished.emit(1)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python GUI Launcher")
        self.resize(800, 600)
        
        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create a splitter to allow resizing
        self.main_splitter = QSplitter(Qt.Vertical)
        main_layout.addWidget(self.main_splitter, 1)  # Give splitter a stretch factor
        
        # Add web view for geojson.io
        web_frame = QFrame()
        web_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        web_layout = QVBoxLayout(web_frame)
        web_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        
        web_header_frame = QFrame()
        web_header_layout = QHBoxLayout(web_header_frame)
        web_header_layout.setContentsMargins(0, 0, 0, 0)
        
        web_label = QLabel("GeoJSON.io Embedded View:")
        web_label.setFont(QFont("Arial", 10, QFont.Bold))
        web_header_layout.addWidget(web_label)
        
        spacer_web = QWidget()
        web_header_layout.addWidget(spacer_web, 1)
        
        toggle_web_button = QPushButton("Toggle Web View")
        toggle_web_button.clicked.connect(self.toggle_web_view)
        web_header_layout.addWidget(toggle_web_button)
        
        web_layout.addWidget(web_header_frame)
        
        # Set up download handler for the web view
        profile = QWebEngineProfile.defaultProfile()
        profile.downloadRequested.connect(self.handle_download)
        
        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl("https://geojson.io/"))
        self.web_view.setMinimumHeight(200)
        self.web_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        web_layout.addWidget(self.web_view, 1)  # Add stretch factor
        
        # Create a widget for all content below the web view
        bottom_content = QWidget()
        bottom_content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        bottom_layout = QVBoxLayout(bottom_content)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add both parts to the splitter
        self.main_splitter.addWidget(web_frame)
        self.main_splitter.addWidget(bottom_content)
        
        # Set initial sizes (adjust as needed)
        self.main_splitter.setSizes([300, 300])
        
        # File path input
        file_frame = QFrame()
        file_layout = QHBoxLayout(file_frame)
        file_layout.setContentsMargins(0, 0, 0, 0)
        
        file_label = QLabel("GeoJSON File:")
        file_label.setFont(QFont("Arial", 10, QFont.Bold))
        file_layout.addWidget(file_label)
        
        self.path_entry = QLineEdit()
        self.path_entry.setFont(QFont("Arial", 10))
        file_layout.addWidget(self.path_entry, 1)  # stretch factor
        
        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self.browse_file)
        file_layout.addWidget(browse_button)
        
        bottom_layout.addWidget(file_frame)
        
        # Script buttons
        button_frame = QFrame()
        button_layout = QVBoxLayout(button_frame)
        
        script_label = QLabel("Select a script to run:")
        script_label.setFont(QFont("Arial", 11, QFont.Bold))
        script_label.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(script_label)
        
        buildings_button = QPushButton("Run Create Buildings")
        buildings_button.setMinimumWidth(200)
        buildings_button.clicked.connect(self.run_create_buildings)
        button_layout.addWidget(buildings_button, 0, Qt.AlignCenter)
        
        terrain_button = QPushButton("Run Create Terrain")
        terrain_button.setMinimumWidth(200)
        terrain_button.clicked.connect(self.run_create_terrain)
        button_layout.addWidget(terrain_button, 0, Qt.AlignCenter)
        
        bottom_layout.addWidget(button_frame)
        
        # Log area
        log_frame = QFrame()
        log_layout = QVBoxLayout(log_frame)
        
        log_header_frame = QFrame()
        log_header_layout = QHBoxLayout(log_header_frame)
        log_header_layout.setContentsMargins(0, 0, 0, 0)
        
        log_header = QLabel("Log Output:")
        log_header.setFont(QFont("Arial", 10, QFont.Bold))
        log_header_layout.addWidget(log_header)
        
        spacer2 = QWidget()
        log_header_layout.addWidget(spacer2, 1)
        
        clear_button = QPushButton("Clear Log")
        clear_button.clicked.connect(self.clear_log)
        log_header_layout.addWidget(clear_button)
        
        log_layout.addWidget(log_header_frame)
        
        self.log_area = QTextEdit()
        self.log_area.setFont(QFont("Courier", 9))
        self.log_area.setReadOnly(True)
        log_layout.addWidget(self.log_area)
        
        bottom_layout.addWidget(log_frame, 1)  # stretch factor to make it expand
        
        # Progress bar and status bar
        self.progress_bar = QProgressBar()
        bottom_layout.addWidget(self.progress_bar)
        
        self.status_bar = QLabel("Ready")
        self.status_bar.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        bottom_layout.addWidget(self.status_bar)
        
        # Set focus to path entry
        self.path_entry.setFocus()
        
        # Initialize worker thread
        self.worker = None
        
    def browse_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select GeoJSON File",
            "",
            "GeoJSON files (*.geojson);;All files (*.*)"
        )
        if filename:
            self.path_entry.setText(filename)
            self.path_entry.setFocus()
            self.path_entry.selectAll()
            
    def clear_log(self):
        """Clear the log area"""
        self.log_area.clear()
        self.log_area.append("Log cleared.\n")
        
    def run_script(self, script_path):
        # Validate file path before running
        file_path = self.path_entry.text()
        if not file_path or not os.path.exists(file_path):
            self.log_area.append(f"Error: File not found - {file_path}\n")
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
    
    def update_log(self, text):
        self.log_area.append(text)
        # Scroll to bottom
        vbar = self.log_area.verticalScrollBar()
        vbar.setValue(vbar.maximum())
        
    def script_completed(self, return_code):
        self.log_area.append(f"Script completed with return code: {return_code}\n")
        # Reset progress bar and status
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100 if return_code == 0 else 0)
        self.status_bar.setText("Ready")
        
    def run_create_buildings(self):
        self.run_script('src/scripts/create_buildings.py')
        
    def run_create_terrain(self):
        self.run_script('src/scripts/create_terrain.py')

    def toggle_web_view(self):
        """Toggle the visibility of the web view"""
        if self.web_view.isVisible():
            self.web_view.hide()
        else:
            self.web_view.show()

    def handle_download(self, download):
        """Handle file downloads from the web view"""
        # Get suggested filename from the download 
        file_name = download.suggestedFileName()
        
        if not file_name:  # If no filename is suggested, use a default
            file_name = "downloaded_file.geojson"
        
        # Show save dialog
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            os.path.join(os.path.expanduser("~"), file_name),
            "GeoJSON Files (*.geojson);;All Files (*.*)"
        )
        
        if save_path:
            # Set the download directory and filename separately
            download_dir = os.path.dirname(save_path)
            download_filename = os.path.basename(save_path)
            
            # Set download location using the current API
            download.setDownloadDirectory(download_dir)
            download.setDownloadFileName(download_filename)
            download.accept()
            
            # Automatically update the file path field if it's a GeoJSON file
            if save_path.lower().endswith('.geojson'):
                self.path_entry.setText(save_path)
                self.log_area.append(f"Downloaded GeoJSON file to: {save_path}\n")
                self.log_area.append("File path automatically updated.\n")
            else:
                self.log_area.append(f"Downloaded file to: {save_path}\n")
        else:
            # If user cancels the save dialog
            download.cancel()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    
    
# To evaluate the likelihood of unfavorable stationary conditions due to wind direction and velocities, in Table 4 1 a wind direction frequency weighted average of the air ventilation rate was used to estimate the daily replenishment period. The replenishment period represents the time required to uniformly refresh the entire volume of the air compartment.