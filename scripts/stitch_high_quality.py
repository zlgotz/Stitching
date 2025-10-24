#!/usr/bin/env python3
"""
stitch_high_quality.py
High-quality stitching tuned for gantry-style (translation) captures using OpenCV.
"""

import os
import cv2
from glob import glob

CAPTURE_DIR = os.path.expanduser("~/stitch/capture")
OUTPUT_DIR  = os.path.expanduser("~/stitch/output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Starting OpenCV high-quality stitching...")

tiles = sorted(glob(os.path.join(CAPTURE_DIR, "*_z0.jpg")))
print(f"Found {len(tiles)} tiles in {CAPTURE_DIR}")

if not tiles:
    raise SystemExit(" No tiles found. Run simulate_gantry_capture.py first.")

images = [cv2.imread(t) for t in tiles]
if any(img is None for img in images):
    raise SystemExit(" One or more tiles could not be read (invalid images).")

# Use translation-based stitching model (for flat surface scans)
stitcher = cv2.Stitcher_create(cv2.Stitcher_SCANS)
status, pano = stitcher.stitch(images)

if status == cv2.Stitcher_OK:
    outpath = os.path.join(OUTPUT_DIR, "stitched_result_high_quality.jpg")
    cv2.imwrite(outpath, pano)
    print(f" High-quality panorama saved → {outpath}")
else:
    print(f" Stitching failed with status code {status}")
