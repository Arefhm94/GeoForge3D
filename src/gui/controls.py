# src/gui/widgets/controls.py

import sys
import subprocess
from PySide6.QtCore import QThread, Signal

class ScriptWorker(QThread):
    """
    Worker thread for running scripts without freezing the GUI
    """
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