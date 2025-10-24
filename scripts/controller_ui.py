
#!/usr/bin/env python3
"""
controller_ui.py
Extended GUI for capture control + stitching options.
"""

import os
import threading
import tkinter as tk
from tkinter import ttk
from capture_core import run_capture, stop_capture
import subprocess

# --- Main window ---
root = tk.Tk()
root.title("Stitch Capture Controller")
root.geometry("480x420")

# --- Layout containers ---
frame_controls = ttk.Frame(root, padding=10)
frame_controls.pack(fill="x")

frame_log = ttk.Frame(root, padding=10)
frame_log.pack(fill="both", expand=True)

# --- Capture parameters ---
ttk.Label(frame_controls, text="Rows:").grid(row=0, column=0)
rows_var = tk.IntVar(value=3)
ttk.Entry(frame_controls, textvariable=rows_var, width=5).grid(row=0, column=1)

ttk.Label(frame_controls, text="Cols:").grid(row=0, column=2)
cols_var = tk.IntVar(value=3)
ttk.Entry(frame_controls, textvariable=cols_var, width=5).grid(row=0, column=3)

ttk.Label(frame_controls, text="Z-stack:").grid(row=1, column=0)
z_var = tk.IntVar(value=1)
ttk.Entry(frame_controls, textvariable=z_var, width=5).grid(row=1, column=1)

ttk.Label(frame_controls, text="Delay (s):").grid(row=1, column=2)
delay_var = tk.DoubleVar(value=0.2)
ttk.Entry(frame_controls, textvariable=delay_var, width=5).grid(row=1, column=3)

# --- Stitching mode dropdown ---
ttk.Label(frame_controls, text="Stitching Mode:").grid(row=2, column=0)
stitch_mode = tk.StringVar(value="fast")
mode_menu = ttk.Combobox(frame_controls, textvariable=stitch_mode, values=["fast", "high_quality"], state="readonly", width=15)
mode_menu.grid(row=2, column=1, columnspan=2)

# --- Buttons ---
def start_capture_thread():
    def task():
        run_capture(rows_var.get(), cols_var.get(), z_var.get(), delay_var.get(), log_callback=log)
    threading.Thread(target=task, daemon=True).start()

def stop_capture_thread():
    stop_capture()
    log("Capture stopped by user.")

def run_stitch_thread():
    def task():
        mode = stitch_mode.get()
        if mode == "fast":
            log("Running fast (grid) stitching...")
            subprocess.run(["python", "scripts/stitch_grid.py"])
        else:
            log("Running high-quality OpenCV stitching...")
            subprocess.run(["python", "scripts/stitch_high_quality.py"])
    threading.Thread(target=task, daemon=True).start()

ttk.Button(frame_controls, text="Start Capture", command=start_capture_thread).grid(row=3, column=0, pady=5)
ttk.Button(frame_controls, text="Stop Capture", command=stop_capture_thread).grid(row=3, column=1, pady=5)
ttk.Button(frame_controls, text="Run Stitching", command=run_stitch_thread).grid(row=3, column=2, columnspan=2, pady=5)

# --- Log display ---
log_box = tk.Text(frame_log, height=15, wrap="word")
log_box.pack(fill="both", expand=True)

def log(message):
    log_box.insert("end", message + "\n")
    log_box.see("end")

root.mainloop()
