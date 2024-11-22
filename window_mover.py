import win32gui
import win32con
import keyboard
import time
from threading import Thread

# Initial positions for shortcuts
positions = {
    "ctrl+alt+1": (-7, -30),
    "ctrl+alt+2": (-7, 35),
}

# Stores the current position to allow incremental adjustments
current_x, current_y = -7, -30

# Max speed settings
INITIAL_DELAY = 0.1  # Initial delay between moves (in seconds)
MIN_DELAY = 0.02  # Minimum delay between moves (fastest speed)
ACCELERATION = 0.9  # Multiplier for delay reduction
MAX_SPEED_INCREMENT = 20  # Max pixels per step

# State variable to track active key presses
running_threads = {}


def move_window(x, y):
    """Moves the currently focused window to (x, y)."""
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, x, y, 0, 0, win32con.SWP_NOSIZE)
    else:
        print("No window is currently in focus.")


def move_focused_window_to_position(hotkey):
    """Callback to move the window to a predefined position."""
    global current_x, current_y
    x, y = positions[hotkey]
    current_x, current_y = x, y
    move_window(x, y)


def adjust_window_position(dx, dy):
    """Adjusts the position of the focused window incrementally."""
    global current_x, current_y

    current_x += dx
    current_y += dy
    move_window(current_x, current_y)


def continuous_adjustment(key, dx, dy):
    """Handles continuous movement with acceleration."""
    global running_threads

    delay = INITIAL_DELAY
    increment = 1  # Start moving 1 pixel at a time

    while key in running_threads and running_threads[key]:
        adjust_window_position(dx * increment, dy * increment)
        time.sleep(delay)

        # Accelerate: Reduce delay and increase increment up to max
        if delay > MIN_DELAY:
            delay *= ACCELERATION
        if increment < MAX_SPEED_INCREMENT:
            increment += 1


def start_moving(key, dx, dy):
    """Starts a background thread to handle continuous movement."""
    global running_threads
    if key in running_threads and running_threads[key]:
        return  # Already running

    running_threads[key] = True
    thread = Thread(target=continuous_adjustment, args=(key, dx, dy), daemon=True)
    thread.start()


def stop_moving(key):
    """Stops the background thread for continuous movement."""
    global running_threads
    if key in running_threads:
        running_threads[key] = False


def main():
    print("Running in background:")
    print("- Press Ctrl+Alt+1 to move the window to (-7, -30).")
    print("- Press Ctrl+Alt+2 to move the window to (-7, 35).")
    print(
        "- Hold Ctrl+Alt+\\ and use arrow keys to adjust the window position with increasing speed."
    )
    print("- Press Ctrl+Alt+Q to quit.")

    # Register hotkeys for predefined positions
    for hotkey in positions.keys():
        keyboard.add_hotkey(hotkey, move_focused_window_to_position, args=(hotkey,))

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
    keyboard.add_hotkey("ctrl+alt+q", lambda: exit())

    # Keep the script running
    keyboard.wait()


if __name__ == "__main__":
    main()
