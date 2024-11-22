import win32gui
import win32con
import keyboard
import time
from threading import Thread
import os
from colorama import Fore, Style, init
from collections import defaultdict

init(autoreset=True)  # Initialize colorama for cross-platform color support

# Define positions for shortcuts
# Structure: {hotkey: (x, y)}
# - hotkey: The key combination to trigger the action.
# - x, y: The target screen coordinates to move the window.
positions = {
    "ctrl+alt+1": (-7, -30),
    "ctrl+alt+2": (-7, 35),
    "ctrl+alt+3": (100, 100),
}

# Max speed settings
INITIAL_DELAY = 0.1  # Initial delay between moves (in seconds)
MIN_DELAY = 0.02  # Minimum delay between moves (fastest speed)
ACCELERATION = 0.9  # Multiplier for delay reduction
MAX_SPEED_INCREMENT = 20  # Max pixels per step

# State variables
running_threads = defaultdict(bool)  # Tracks active threads for continuous movement
current_positions = {}  # Tracks current positions of windows by their handles


def clear_and_print_menu():
    """Clears the terminal and reprints the menu."""
    os.system("cls" if os.name == "nt" else "clear")
    print(Fore.CYAN + "Running in background:")
    print(Fore.YELLOW + "Hotkeys:")
    for hotkey, (x, y) in positions.items():
        print(f"{Fore.GREEN}  - {hotkey}: Move the window to ({x}, {y})")
    print(Fore.MAGENTA + "- Hold Ctrl+Alt+\\ and use arrow keys to adjust the window position with increasing speed.")
    print(Fore.RED + "- Press Ctrl+Alt+Q to quit.")
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


def adjust_window_position(dx, dy):
    """Adjusts the position of the focused window incrementally."""
    hwnd = win32gui.GetForegroundWindow()
    if not hwnd:
        print(Fore.RED + "No window is currently in focus.")
        return

    # Get the current position of the window
    rect = win32gui.GetWindowRect(hwnd)
    current_x, current_y = current_positions.get(hwnd, (rect[0], rect[1]))

    # Update position
    current_x += dx
    current_y += dy
    current_positions[hwnd] = (current_x, current_y)
    move_window(hwnd, current_x, current_y)


def continuous_adjustment(keys, dx, dy):
    """Handles continuous movement with acceleration."""
    delay = INITIAL_DELAY
    increment = 1  # Start moving 1 pixel at a time

    while any(running_threads[k] for k in keys):
        adjust_window_position(dx * increment, dy * increment)
        time.sleep(delay)
        
        # Accelerate
        if delay > MIN_DELAY:
            delay *= ACCELERATION
        if increment < MAX_SPEED_INCREMENT:
            increment += 1


def start_moving(key, dx, dy):
    """Starts a background thread to handle continuous movement."""
    global running_threads
    if running_threads[key]:
        return  # Already running

    running_threads[key] = True
    thread = Thread(target=continuous_adjustment, args=([key], dx, dy), daemon=True)
    thread.start()


def stop_moving(key):
    """Stops the background thread for continuous movement."""
    global running_threads
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
    os._exit(0)  # Immediately terminates the process


def main():
    clear_and_print_menu()

    # Register hotkeys for predefined positions
    for hotkey, (x, y) in positions.items():
        keyboard.add_hotkey(hotkey, move_focused_window_to_position, args=(x, y))

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
