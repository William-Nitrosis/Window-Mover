import win32gui
import win32con
import keyboard
import time
from threading import Thread
import os
from colorama import Fore, init
from collections import defaultdict
import json

init(autoreset=True)  # Initialize colorama for cross-platform color support

CONFIG_FILE = "positions_config.json"

def load_positions():
    """Loads positions from the configuration file."""
    if not os.path.exists(CONFIG_FILE):
        print(Fore.RED + f"Configuration file '{CONFIG_FILE}' not found. Creating a new one.")
        with open(CONFIG_FILE, "w") as f:
            json.dump({}, f)
        return {}
    with open(CONFIG_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            print(Fore.RED + f"Error reading configuration file: {e}")
            return {}

def save_positions(positions):
    """Saves the updated positions dictionary back to the configuration file."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(positions, f, indent=4)
    print(Fore.GREEN + f"Saved updated positions to '{CONFIG_FILE}'.")

positions = load_positions()  # Load the positions from the file

# Max speed settings
INITIAL_DELAY = 0.1
MIN_DELAY = 0.02
ACCELERATION = 0.9
MAX_SPEED_INCREMENT = 20

# State variables
running_threads = defaultdict(bool)
current_positions = {}

def clear_and_print_menu():
    """Clears the terminal and reprints the menu."""
    os.system("cls" if os.name == "nt" else "clear")
    print(Fore.CYAN + "Running in background:")
    print(Fore.YELLOW + "Hotkeys:")
    for hotkey, (x, y) in positions.items():
        print(f"{Fore.GREEN}  - {hotkey}: Move the window to ({x}, {y})")
    print(Fore.MAGENTA + "- Hold Ctrl+Alt+\\ and use arrow keys to adjust the window position with increasing speed.")
    print(Fore.RED + "- Press Ctrl+Alt+Q to quit.")
    print(Fore.BLUE + "- Press Ctrl+Alt+S + Number to save a new hotkey with the current window position.")
    print()

def move_window(hwnd, x, y):
    """Moves a specific window to (x, y)."""
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, x, y, 0, 0, win32con.SWP_NOSIZE)

def move_focused_window_to_position(x, y):
    """Moves the focused window to the specified position."""
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        current_positions[hwnd] = (x, y)
        move_window(hwnd, x, y)
        window_title = win32gui.GetWindowText(hwnd)
        print(Fore.GREEN + f"Moved window '{window_title}' to ({x}, {y}).")
        clear_menu_after_delay()
    else:
        print(Fore.RED + "No window is currently in focus.")

def save_hotkey_position(number):
    """Saves the current window position as a new hotkey (Ctrl+Alt+Number)."""
    hwnd = win32gui.GetForegroundWindow()
    if not hwnd:
        print(Fore.RED + "No window is currently in focus. Cannot save position.")
        return
    
    # Get the current position of the window
    rect = win32gui.GetWindowRect(hwnd)
    x, y = rect[0], rect[1]
    hotkey = f"ctrl+alt+{number}"
    
    # Update positions and save
    positions[hotkey] = [x, y]
    save_positions(positions)
    print(Fore.GREEN + f"Saved hotkey '{hotkey}' with position ({x}, {y}).")
    clear_menu_after_delay()

def adjust_window_position(dx, dy):
    """Adjusts the position of the focused window incrementally."""
    hwnd = win32gui.GetForegroundWindow()
    if not hwnd:
        print(Fore.RED + "No window is currently in focus.")
        return

    rect = win32gui.GetWindowRect(hwnd)
    current_x, current_y = current_positions.get(hwnd, (rect[0], rect[1]))
    current_x += dx
    current_y += dy
    current_positions[hwnd] = (current_x, current_y)
    move_window(hwnd, current_x, current_y)

def continuous_adjustment(keys, dx, dy):
    """Handles continuous movement with acceleration."""
    delay = INITIAL_DELAY
    increment = 1
    while any(running_threads[k] for k in keys):
        adjust_window_position(dx * increment, dy * increment)
        time.sleep(delay)
        if delay > MIN_DELAY:
            delay *= ACCELERATION
        if increment < MAX_SPEED_INCREMENT:
            increment += 1

def start_moving(key, dx, dy):
    """Starts a background thread to handle continuous movement."""
    if running_threads[key]:
        return
    running_threads[key] = True
    thread = Thread(target=continuous_adjustment, args=([key], dx, dy), daemon=True)
    thread.start()

def stop_moving(key):
    """Stops the background thread for continuous movement."""
    running_threads[key] = False

def clear_menu_after_delay():
    """Clears and reprints the menu after a short delay in a separate thread."""
    def delayed_clear():
        time.sleep(5)
        clear_and_print_menu()
    Thread(target=delayed_clear, daemon=True).start()

def quit_program():
    """Stops the program gracefully."""
    print(Fore.RED + "Exiting program...")
    os._exit(0)

def main():
    clear_and_print_menu()

    # Register hotkeys for predefined positions
    for hotkey, (x, y) in positions.items():
        keyboard.add_hotkey(hotkey, move_focused_window_to_position, args=(x, y))
    
    # Register dynamic saving of new hotkeys
    for i in range(10):  # Numbers 0-9
        keyboard.add_hotkey(f"ctrl+alt+s+{i}", save_hotkey_position, args=(i,))
    
    # Register arrow key adjustments while holding Ctrl+Alt+\
    keyboard.add_hotkey("ctrl+alt+\\+up", start_moving, args=("up", 0, -1))
    keyboard.add_hotkey("ctrl+alt+\\+down", start_moving, args=("down", 0, 1))
    keyboard.add_hotkey("ctrl+alt+\\+left", start_moving, args=("left", -1, 0))
    keyboard.add_hotkey("ctrl+alt+\\+right", start_moving, args=("right", 1, 0))
    
    # Stop movement when the key is released
    keyboard.on_release_key("up", lambda _: stop_moving("up"))
    keyboard.on_release_key("down", lambda _: stop_moving("down"))
    keyboard.on_release_key("left", lambda _: stop_moving("left"))
    keyboard.on_release_key("right", lambda _: stop_moving("right"))

    # Register hotkey to quit the script
    keyboard.add_hotkey("ctrl+alt+q", quit_program)

    # Keep the script running
    keyboard.wait()

if __name__ == "__main__":
    main()
