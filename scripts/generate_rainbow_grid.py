#!/usr/bin/env python3
"""
generate_rainbow_grid.py
Creates a large rainbow gradient image, then slices it into a grid (like captured tiles).
"""

import os, cv2, numpy as np

CAPTURE_DIR = os.path.expanduser("~/stitch/capture")
os.makedirs(CAPTURE_DIR, exist_ok=True)

# --- SETTINGS ---
ROWS, COLS = 3, 3      # grid layout
TILE_SIZE = 300        # each output tile (px)
FULL_W = TILE_SIZE * COLS
FULL_H = TILE_SIZE * ROWS

# --- Create rainbow gradient ---
gradient = np.zeros((FULL_H, FULL_W, 3), dtype=np.uint8)
for y in range(FULL_H):
    for x in range(FULL_W):
        hue = int(180 * x / FULL_W)  # 0–180 hue range in OpenCV HSV
        sat = 255
        val = int(255 * (1 - y / FULL_H * 0.5))  # darker toward bottom
        gradient[y, x] = [hue, sat, val]

rainbow_bgr = cv2.cvtColor(gradient, cv2.COLOR_HSV2BGR)

# --- Slice into grid tiles ---
for r in range(ROWS):
    for c in range(COLS):
        y0, x0 = r * TILE_SIZE, c * TILE_SIZE
        tile = rainbow_bgr[y0:y0 + TILE_SIZE, x0:x0 + TILE_SIZE]
        filename = f"r{r}_c{c}_z0.jpg"
        cv2.imwrite(os.path.join(CAPTURE_DIR, filename), tile)

cv2.imwrite(os.path.join(CAPTURE_DIR, "rainbow_full.jpg"), rainbow_bgr)
print(f"Rainbow grid generated in {CAPTURE_DIR}")
