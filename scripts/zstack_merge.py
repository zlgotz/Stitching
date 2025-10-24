#!/usr/bin/env python3
"""
zstack_merge.py
Combines multiple Z images into a single all-in-focus image using OpenCV.
"""

import cv2, numpy as np, os, re
from glob import glob

CAPTURE_DIR = os.path.expanduser("~/stitch/capture")
OUTPUT_DIR = os.path.expanduser("~/stitch/output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Group files by XY position (ignore z)
pattern = re.compile(r"r(\d+)_c(\d+)_z\d+\.jpg")
images = glob(os.path.join(CAPTURE_DIR, "*.jpg"))

groups = {}
for path in images:
    m = pattern.search(os.path.basename(path))
    if not m:
        continue
    key = (int(m.group(1)), int(m.group(2)))
    groups.setdefault(key, []).append(path)

for (r, c), files in groups.items():
    stack = [cv2.imread(f).astype(np.float32)/255.0 for f in sorted(files)]
    merge = cv2.createMergeMertens().process(stack)
    merge = np.clip(merge * 255, 0, 255).astype(np.uint8)
    outpath = os.path.join(OUTPUT_DIR, f"r{r}_c{c}_merged.jpg")
    cv2.imwrite(outpath, merge)
    print(f"Merged {len(files)} layers → {outpath}")
