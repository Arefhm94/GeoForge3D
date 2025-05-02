"""Building Terrain Modeler GUI Main Window"""
import os

from PySide6.QtWidgets import QFileDialog

def handle_web_download(parent_window, download, path_entry, log_area):
    """
    Handle file downloads from the web view
    
    Args:
        parent_window: The parent window for showing dialogs
        download: The download object from the QWebEngineProfile
        path_entry: The QLineEdit widget to update with the download path
        log_area: The QTextEdit widget for logging download information
    """
    # Get suggested filename from the download
    file_name = download.suggestedFileName()
    
    if not file_name:  # If no filename is suggested, use a default
        file_name = "downloaded_file.geojson"
    
    save_path, _ = QFileDialog.getSaveFileName(
        parent_window,
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
            path_entry.setText(save_path)
            log_area.append(f"Downloaded GeoJSON file to: {save_path}\n")
            log_area.append("File path automatically updated.\n")
        else:
            log_area.append(f"Downloaded file to: {save_path}\n")
    else:
        # If user cancels the save dialog
        download.cancel()
