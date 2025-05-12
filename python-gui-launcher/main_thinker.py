from tkinter import Tk, Button, Label, Text, Entry, StringVar, Frame, scrolledtext, filedialog
from tkinter import ttk  # Add this for progress bar
import subprocess
import sys
import threading
import io
import os
import webbrowser
from tkinter import messagebox

def run_script(script_path, geojson_path, log_area, progress_bar, status_bar):
    def execute():
        # Validate file path before running
        file_path = geojson_path.get()
        if not file_path or not os.path.exists(file_path):
            log_area.insert("end", f"Error: File not found - {file_path}\n")
            log_area.see("end")
            return
            
        # Start progress bar animation and update status
        progress_bar.start(10)
        status_bar.config(text="Running script...")
        
        log_area.insert("end", f"Running {script_path} with file: {file_path}\n")
        log_area.see("end")
        try:
            process = subprocess.Popen(
                [sys.executable, script_path, file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            
            for line in process.stdout:
                log_area.insert("end", line)
                log_area.see("end")
                
            process.wait()
            log_area.insert("end", f"Script completed with return code: {process.returncode}\n")
            log_area.see("end")
        except Exception as e:
            log_area.insert("end", f"Error: {str(e)}\n")
            log_area.see("end")
        finally:
            # Stop progress bar and reset status
            progress_bar.stop()
            status_bar.config(text="Ready")
    
    # Run in a separate thread to avoid freezing the GUI
    thread = threading.Thread(target=execute)
    thread.daemon = True
    thread.start()

def run_create_buildings(geojson_path, log_area, progress_bar, status_bar):
    run_script('src/scripts/create_buildings.py', geojson_path, log_area, progress_bar, status_bar)

def run_create_terrain(geojson_path, log_area, progress_bar, status_bar):
    run_script('src/scripts/create_terrain.py', geojson_path, log_area, progress_bar, status_bar)

def browse_file(geojson_path, path_entry):
    filename = filedialog.askopenfilename(
        title="Select GeoJSON File",
        filetypes=(("GeoJSON files", "*.geojson"), ("All files", "*.*"))
    )
    if filename:
        geojson_path.set(filename)
        # Put cursor at the end of the path
        path_entry.icursor("end")
        # Make the entry field focused
        path_entry.focus_set()
        # Highlight path briefly
        path_entry.selection_range(0, "end")

def open_geojson_website():
    """Open the geojson.io website in the default browser"""
    webbrowser.open("https://geojson.io/")

def clear_log(log_area):
    """Clear the log area"""
    log_area.delete(1.0, "end")
    log_area.insert("end", "Log cleared.\n")

def main():
    root = Tk()
    root.title("Python GUI Launcher")
    root.geometry("800x600")  # Larger window for better visibility
    
    # Add geojson.io button at the top
    top_frame = Frame(root)
    top_frame.pack(fill='x', padx=20, pady=5)
    
    geojson_web_button = Button(
        top_frame, 
        text="Open GeoJSON.io", 
        command=open_geojson_website,
        font=("Arial", 10),
        bg="#4CAF50",
        fg="white",
        padx=10,
        pady=3
    )
    geojson_web_button.pack(side='right')
    
    # GeoJSON file path input with better styling
    file_frame = Frame(root)
    file_frame.pack(pady=10, fill='x', padx=20)
    
    Label(file_frame, text="GeoJSON File:", font=("Arial", 10, "bold")).pack(side='left')
    
    geojson_path = StringVar()
    path_entry = Entry(file_frame, textvariable=geojson_path, width=60, font=("Arial", 10))
    path_entry.pack(side='left', padx=5, expand=True, fill='x')
    
    browse_button = Button(
        file_frame, 
        text="Browse...", 
        command=lambda: browse_file(geojson_path, path_entry),
        font=("Arial", 10),
        bg="#f0f0f0",
        padx=10
    )
    browse_button.pack(side='left')
    
    # Script buttons
    button_frame = Frame(root)
    button_frame.pack(pady=10)
    
    Label(button_frame, text="Select a script to run:", font=("Arial", 11, "bold")).pack()
    
    # Create progress bar
    progress_bar = ttk.Progressbar(root, orient="horizontal", mode="indeterminate", length=200)
    
    # Add status bar (moved up so we can reference it in the button commands)
    status_bar = Label(root, text="Ready", bd=1, relief="sunken", anchor="w")
    
    button1 = Button(
        button_frame, 
        text="Run Create Buildings", 
        command=lambda: run_create_buildings(geojson_path, log_area, progress_bar, status_bar),
        font=("Arial", 10),
        bg="#e0e0e0",
        padx=10,
        pady=5
    )
    button1.pack(pady=5)
    
    button2 = Button(
        button_frame, 
        text="Run Create Terrain", 
        command=lambda: run_create_terrain(geojson_path, log_area, progress_bar, status_bar),
        font=("Arial", 10),
        bg="#e0e0e0",
        padx=10,
        pady=5
    )
    button2.pack(pady=5)
    
    # Log display area
    log_frame = Frame(root)
    log_frame.pack(pady=10, padx=20, fill='both', expand=True)
    
    log_header_frame = Frame(log_frame)
    log_header_frame.pack(fill='x')
    
    Label(log_header_frame, text="Log Output:", font=("Arial", 10, "bold")).pack(side='left', anchor='w')
    
    # Add clear log button
    clear_button = Button(
        log_header_frame, 
        text="Clear Log", 
        command=lambda: clear_log(log_area),
        font=("Arial", 9),
        bg="#f0f0f0",
        padx=5
    )
    clear_button.pack(side='right')
    
    log_area = scrolledtext.ScrolledText(log_frame, height=15, font=("Courier", 9))
    log_area.pack(fill='both', expand=True)
    
    # Set focus to path entry initially
    path_entry.focus_set()
    
    # Place the progress bar above the status bar
    progress_bar.pack(side="bottom", fill="x", padx=10, pady=2)
    
    # Now pack the status bar
    status_bar.pack(side="bottom", fill="x")
    
    root.mainloop()

if __name__ == "__main__":
    main()