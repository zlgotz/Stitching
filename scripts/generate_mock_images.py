#!/usr/bin/env python3
"""
generate_mock_images.py
Creates a grid of sample images with slight shifts/blurs for Z-stack + stitching tests.
"""

import os, cv2, numpy as np

CAPTURE_DIR = os.path.expanduser("~/stitch/capture")
os.makedirs(CAPTURE_DIR, exist_ok=True)

ROWS, COLS, Z_LEVELS = 3, 3, 3

for r in range(ROWS):
    for c in range(COLS):
        for z in range(Z_LEVELS):
            # create a color pattern that changes with position
            img = np.zeros((300, 300, 3), dtype=np.uint8)
            color = (r * 80 + 30, c * 80 + 30, z * 80)
            img[:] = color

            # simulate focus blur based on z
            blur = 1 + 2 * z
            img = cv2.GaussianBlur(img, (blur*2+1, blur*2+1), 0)

            filename = f"r{r}_c{c}_z{z}.jpg"
            cv2.imwrite(os.path.join(CAPTURE_DIR, filename), img)

print("Mock images generated in", CAPTURE_DIR)
