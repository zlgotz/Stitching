#!/usr/bin/env python3
"""
simulate_gantry_capture.py
Splits a given input image into a grid of overlapping tiles
to simulate how the gantry would capture them.
"""

import os
import cv2
import numpy as np

# --- SETTINGS ---
INPUT_IMAGE = os.path.expanduser("~/stitch/sample_input.jpg")  # change this to your test image
CAPTURE_DIR = os.path.expanduser("~/stitch/capture")
os.makedirs(CAPTURE_DIR, exist_ok=True)

ROWS, COLS = 3, 3          # grid shape (like gantry passes)
OVERLAP = 0.15             # 15% overlap between adjacent tiles (simulates camera FOV overlap)

# --- Load image ---
img = cv2.imread(INPUT_IMAGE)
if img is None:
    raise SystemExit(f"Could not open input image: {INPUT_IMAGE}")

h, w = img.shape[:2]
print(f"Loaded input: {INPUT_IMAGE} ({w}x{h})")

# --- Compute crop sizes ---
tile_w = int(w / (COLS - (COLS - 1) * OVERLAP))
tile_h = int(h / (ROWS - (ROWS - 1) * OVERLAP))
step_x = int(tile_w * (1 - OVERLAP))
step_y = int(tile_h * (1 - OVERLAP))

print(f"Simulating {ROWS}x{COLS} grid with {OVERLAP*100:.0f}% overlap")
print(f"Tile size: {tile_w}x{tile_h} | Step size: {step_x}x{step_y}")

# --- Generate and save tiles ---
for r in range(ROWS):
    for c in range(COLS):
        x0 = c * step_x
        y0 = r * step_y
        x1 = min(x0 + tile_w, w)
        y1 = min(y0 + tile_h, h)

        tile = img[y0:y1, x0:x1]
        filename = f"r{r}_c{c}_z0.jpg"
        filepath = os.path.join(CAPTURE_DIR, filename)
        cv2.imwrite(filepath, tile)
        print(f" Saved {filename} ({x0}:{x1}, {y0}:{y1})")

# --- Save reference for comparison ---
ref_path = os.path.join(CAPTURE_DIR, "reference_full.jpg")
cv2.imwrite(ref_path, img)
print(f"\n Simulation complete! Tiles saved to {CAPTURE_DIR}")
print(f"Full reference image → {ref_path}")
