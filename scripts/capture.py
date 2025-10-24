#!/usr/bin/env python3
"""
Simple camera capture script (placeholder for gphoto2)
Saves images into ~/stitch/capture/
"""
import os
import datetime

CAPTURE_DIR = os.path.expanduser("~/stitch/capture")
os.makedirs(CAPTURE_DIR, exist_ok=True)

def capture_image():
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{timestamp}.jpg"
    filepath = os.path.join(CAPTURE_DIR, filename)
    print(f"Capturing → {filepath}")

    # Placeholder for camera capture (Windows)
    # On Raspberry Pi, replace this with gphoto2 command:
    # subprocess.run(["sudo", "gphoto2", "--port", "usb:", "--capture-image-and-download", "--filename", filepath])
    with open(filepath, "w") as f:
        f.write("Test image placeholder")

if __name__ == "__main__":
    capture_image()
