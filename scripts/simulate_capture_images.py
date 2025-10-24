#!/usr/bin/env python3
"""
simulate_capture_images.py
Creates a set of fake image tiles (r#_c#_z0.jpg) with unique patterns,
so they behave like real camera captures for testing the stitching pipeline.
"""

import os, cv2, numpy as np

CAPTURE_DIR = os.path.expanduser("~/stitch/capture")
os.makedirs(CAPTURE_DIR, exist_ok=True)

ROWS, COLS = 3, 3
IMG_SIZE = (480, 640)  # height, width in pixels

print(f"Generating simulated capture grid {ROWS}x{COLS} → {CAPTURE_DIR}")

for r in range(ROWS):
    for c in range(COLS):
        # make a colored gradient tile
        img = np.zeros((IMG_SIZE[0], IMG_SIZE[1], 3), np.uint8)
        color = (
            int(80 + 60 * np.sin(r)),
            int(80 + 60 * np.cos(c)),
            int(80 + 60 * np.sin(r + c)),
        )
        img[:] = color

        # add identifying text
        label = f"r{r}_c{c}"
        cv2.putText(
            img,
            label,
            (50, 240),
            cv2.FONT_HERSHEY_SIMPLEX,
            2.0,
            (255, 255, 255),
            4,
            cv2.LINE_AA,
        )

        filename = f"r{r}_c{c}_z0.jpg"
        path = os.path.join(CAPTURE_DIR, filename)
        cv2.imwrite(path, img)
        print(f"Saved {path}")

print("\n Simulated capture complete — all tiles are valid JPEGs.")
