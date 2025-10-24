#!/usr/bin/env python3
"""
motion_serial.py
Handles serial communication with Arduino/ESP motion controller.
Includes a simulation mode for testing on Windows.
"""

import time
import sys

try:
    import serial  # pyserial library
except ImportError:
    serial = None

# === Configuration ===
DEFAULT_PORT = "COM3" if sys.platform.startswith("win") else "/dev/ttyUSB0"
BAUD_RATE = 115200
SIMULATION = True  # set to False on the Pi when real hardware is connected


class MotionController:
    def __init__(self, port=DEFAULT_PORT, baud=BAUD_RATE, simulation=SIMULATION):
        self.simulation = simulation
        if not simulation:
            if serial is None:
                raise RuntimeError("pyserial not installed. Run 'pip install pyserial'.")
            try:
                self.ser = serial.Serial(port, baud, timeout=2)
                time.sleep(2)  # allow controller to boot
                print(f"[Serial] Connected to {port} at {baud} baud.")
            except Exception as e:
                print(f"[Serial ERROR] Could not open port {port}: {e}")
                self.simulation = True
        else:
            print("[Motion] Simulation mode enabled – no hardware connection.")

    # ---- Commands ----
    def send(self, cmd):
        """Send a command to the controller."""
        if self.simulation:
            print(f"[SIM] -> {cmd}")
            time.sleep(0.2)
            return "ok"

        line = (cmd.strip() + "\n").encode("utf-8")
        self.ser.write(line)
        return self._wait_for_ok()

    def _wait_for_ok(self):
        """Wait for controller to respond with 'ok'."""
        while True:
            response = self.ser.readline().decode().strip()
            if response:
                print(f"[Serial] <- {response}")
            if "ok" in response.lower() or "done" in response.lower():
                return response

    def move(self, x=None, y=None, z=None, f=3000):
        """Convenience wrapper to move the gantry."""
        parts = []
        if x is not None: parts.append(f"X{x}")
        if y is not None: parts.append(f"Y{y}")
        if z is not None: parts.append(f"Z{z}")
        cmd = f"G1 {' '.join(parts)} F{f}"
        return self.send(cmd)

    def home(self):
        return self.send("G28")  # standard G-code home

    def close(self):
        if not self.simulation:
            self.ser.close()
            print("[Serial] Connection closed.")
