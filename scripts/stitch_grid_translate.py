#!/usr/bin/env python3
"""
stitch_grid_translate.py
Grid-based translational stitching (for flat gantry scans)
"""

import os
import cv2
import numpy as np
from glob import glob
import re

CAPTURE_DIR = os.path.expanduser("~/stitch/capture")
OUTPUT_DIR = os.path.expanduser("~/stitch/output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def parse_tile_name(fname):
    """Extract row and column from filename like r1_c2_z0.jpg"""
    m = re.search(r"r(\d+)_c(\d+)", os.path.basename(fname))
    return int(m.group(1)), int(m.group(2))

tiles = sorted(glob(os.path.join(CAPTURE_DIR, "*_z0.jpg")))
if not tiles:
    raise SystemExit("❌ No tiles found. Run simulate_gantry_capture.py first.")

# Load all tiles
images = {parse_tile_name(f): cv2.imread(f) for f in tiles}
rows = max(r for r, _ in images.keys()) + 1
cols = max(c for _, c in images.keys()) + 1
print(f" Found {len(images)} tiles ({rows}x{cols})")

h, w, _ = next(iter(images.values())).shape
overlap = 0.15  # same as simulator

# Compute canvas dimensions
step_x = int(round(w * (1 - overlap)))
step_y = int(round(h * (1 - overlap)))
canvas_w = step_x * (cols - 1) + w
canvas_h = step_y * (rows - 1) + h

canvas = np.zeros((canvas_h, canvas_w, 3), dtype=np.float32)
weight = np.zeros((canvas_h, canvas_w), dtype=np.float32)

# Create smooth blending mask
alpha_x = np.linspace(0, 1, w)
alpha_x = np.minimum(alpha_x, alpha_x[::-1])
alpha_y = np.linspace(0, 1, h)
blend_mask = np.outer(alpha_y, alpha_x)
blend_mask = np.dstack([blend_mask] * 3)

# Stitch tiles row by row
for (r, c), img in images.items():
    y = r * step_y
    x = c * step_x

    roi_h = min(h, canvas_h - y)
    roi_w = min(w, canvas_w - x)

    roi = canvas[y:y + roi_h, x:x + roi_w]
    wmask = weight[y:y + roi_h, x:x + roi_w]

    img_crop = img[:roi_h, :roi_w].astype(np.float32)
    mask_crop = blend_mask[:roi_h, :roi_w]

    roi[:] += img_crop * mask_crop
    wmask[:] += mask_crop[:, :, 0]

# Normalize blended output
weight[weight == 0] = 1
canvas = (canvas / weight[..., None]).astype(np.uint8)

out_path = os.path.join(OUTPUT_DIR, "stitched_grid_result.jpg")
cv2.imwrite(out_path, canvas)
print(f" Grid-based translational stitch saved → {out_path}")

