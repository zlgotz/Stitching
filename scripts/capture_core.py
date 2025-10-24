
#!/usr/bin/env python3
"""
capture_core.py
Handles grid + Z-stack capture logic.
Now integrated with motion_serial for simulated movement.
"""

import os, time, datetime
from motion_serial import MotionController

CAPTURE_DIR = os.path.expanduser("~/stitch/capture")
os.makedirs(CAPTURE_DIR, exist_ok=True)

running = False


def run_capture(rows, cols, zlevels, delay, log_callback=print):
    """
    Main grid + Z-stack loop with simulated motion control.
    log_callback: function used to send log messages (e.g., to UI)
    """
    global running
    running = True

    # Initialize motion system
    motion = MotionController(simulation=True)  # change to False on Raspberry Pi
    motion.home()
    log_callback(f"System homed. Starting grid capture {rows}x{cols} with {zlevels} Z-steps each.")

    try:
        for r in range(rows):
            if not running:
                log_callback("Capture stopped.")
                break

            # Determine direction (boustrophedon pattern)
            col_range = range(cols) if r % 2 == 0 else range(cols - 1, -1, -1)

            for c in col_range:
                if not running:
                    break

                log_callback(f"Moving to (row={r}, col={c})")
                motion.move(x=c * 10, y=r * 10)  # simulate 10mm grid spacing
                time.sleep(delay)

                for z in range(zlevels):
                    if not running:
                        break

                    log_callback(f"  Moving to Z-level {z}")
                    motion.move(z=z * 0.2)  # simulate Z-step of 0.2mm
                    capture_image(r, c, z, log_callback)
                    time.sleep(delay)

                # Return to starting Z position after each stack
                motion.move(z=0)
                time.sleep(0.2)

        log_callback("Grid capture complete.")
    finally:
        motion.close()
        running = False


def capture_image(row, col, z, log_callback=print):
    """Simulate a camera capture."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"r{row}_c{col}_z{z}_{timestamp}.jpg"
    filepath = os.path.join(CAPTURE_DIR, filename)
    with open(filepath, "w") as f:
        f.write(f"Simulated image for (r={row}, c={col}, z={z})\n")
    log_callback(f"📸 Captured → {filename}")


def stop_capture():
    """Stops the running capture gracefully."""
    global running
    running = False
