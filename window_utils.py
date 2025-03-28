# window_utils.py
import os
import json
import win32gui

CONFIG_FILE = "positions_config.json"

def load_positions():
    """Loads positions from the configuration file."""
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump({}, f)
        return {}
    with open(CONFIG_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_positions(positions):
    """Saves the updated positions dictionary back to the configuration file."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(positions, f, indent=4)

def get_focused_window_title():
    """Returns the title of the currently focused window."""
    hwnd = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(hwnd) if hwnd else "None"

def get_focused_window_position():
    """Returns the (x, y) of the focused window or None if no window."""
    hwnd = win32gui.GetForegroundWindow()
    if not hwnd:
        return None
    rect = win32gui.GetWindowRect(hwnd)
    return rect[0], rect[1]