#!/usr/bin/env python3
"""
stitch_grid.py
Assembles grid tiles (r#_c#_z0.jpg) from the capture folder into one mosaic image.
Designed for rainbow test or real capture data.
"""

import cv2, os, re, numpy as np
from glob import glob

# --- Paths ---
CAPTURE_DIR = os.path.expanduser("~/stitch/capture")
OUTPUT_DIR = os.path.expanduser("~/stitch/output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

final_out = os.path.join(OUTPUT_DIR, "stitched_result.jpg")

# --- Find tiles ---
pattern = re.compile(r"r(\d+)_c(\d+)_z0\.jpg")
tiles = glob(os.path.join(CAPTURE_DIR, "*_z0.jpg"))
if not tiles:
    raise SystemExit(" No tiles found in capture/. Make sure you ran generate_rainbow_grid.py")

# --- Determine grid layout ---
coords = [tuple(map(int, pattern.search(os.path.basename(f)).groups())) for f in tiles]
rows = max(r for r, _ in coords) + 1
cols = max(c for _, c in coords) + 1

print(f" Found {len(tiles)} tiles → grid {rows}x{cols}")

# --- Load and stitch ---
images = {(r, c): cv2.imread(f) for (r, c), f in zip(coords, tiles)}
tile_h, tile_w = next(iter(images.values())).shape[:2]
canvas = np.zeros((tile_h * rows, tile_w * cols, 3), dtype=np.uint8)

for (r, c), img in images.items():
    y0, x0 = r * tile_h, c * tile_w
    canvas[y0:y0 + tile_h, x0:x0 + tile_w] = img
    print(f"Placed tile (r={r}, c={c}) at y={y0}, x={x0}")

# --- Save result ---
cv2.imwrite(final_out, canvas)
print(f" Stitched grid saved → {final_out}")
