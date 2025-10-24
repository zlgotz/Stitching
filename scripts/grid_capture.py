#!/usr/bin/env python3
"""
Grid Capture Script
Takes a sequence of images in a defined grid pattern (for stitching)
"""

import os
import datetime
import time

CAPTURE_DIR = os.path.expanduser("~/stitch/capture")
os.makedirs(CAPTURE_DIR, exist_ok=True)

ROWS = 3   # number of rows in grid
COLS = 3   # number of columns in grid
DELAY = 1  # seconds to wait between captures (simulate move time)

def capture_image(row, col):
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"row{row}_col{col}_{timestamp}.jpg"
    filepath = os.path.join(CAPTURE_DIR, filename)
    print(f"Capturing ({row}, {col}) → {filepath}")

    # Placeholder for actual camera capture
    # On Raspberry Pi, replace this with gphoto2 command:
    # subprocess.run(["sudo", "gphoto2", "--port", "usb:", "--capture-image-and-download", "--filename", filepath])
    with open(filepath, "w") as f:
        f.write(f"Simulated image for grid position ({row},{col})")

def run_grid_capture(rows, cols):
    for r in range(rows):
        # Determine direction for this row
        if r % 2 == 0:
            col_range = range(cols)
        else:
            col_range = range(cols - 1, -1, -1)

        for c in col_range:
            capture_image(r, c)
            time.sleep(DELAY)

if __name__ == "__main__":
    print(f"Starting grid capture {ROWS}x{COLS}")
    run_grid_capture(ROWS, COLS)
    print("Grid capture complete!")
