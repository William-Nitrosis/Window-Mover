import win32gui
import win32con
import keyboard

# Initial positions for shortcuts
positions = {
    "ctrl+alt+1": (-7, -30),
    "ctrl+alt+2": (-7, 35),
}

# Stores the current position to allow incremental adjustments
current_x, current_y = -7, -30

def move_window(x, y):
    """Moves the currently focused window to (x, y)."""
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        win32gui.SetWindowPos(
            hwnd, win32con.HWND_TOP, x, y, 0, 0, win32con.SWP_NOSIZE
        )
    else:
        print("No window is currently in focus.")

def move_focused_window_to_position(hotkey):
    """Callback to move the window to a predefined position."""
    global current_x, current_y
    x, y = positions[hotkey]
    current_x, current_y = x, y
    move_window(x, y)

def adjust_window_position(dx, dy):
    """Adjusts the position of the focused window by (dx, dy)."""
    global current_x, current_y
    current_x += dx
    current_y += dy
    move_window(current_x, current_y)

def main():
    print("Running in background:")
    print("- Press Ctrl+Alt+1 to move the window to (-7, -30).")
    print("- Press Ctrl+Alt+2 to move the window to (-7, 35).")
    print("- Hold Ctrl+Alt+\\ and use arrow keys to adjust the window position 1 pixel at a time.")
    print("- Press Ctrl+Alt+Q to quit.")

    # Register hotkeys for predefined positions
    for hotkey in positions.keys():
        keyboard.add_hotkey(hotkey, move_focused_window_to_position, args=(hotkey,))

    # Register arrow key adjustments while holding Ctrl+Alt+\
    keyboard.add_hotkey("ctrl+alt+\\+up", adjust_window_position, args=(0, -1))
    keyboard.add_hotkey("ctrl+alt+\\+down", adjust_window_position, args=(0, 1))
    keyboard.add_hotkey("ctrl+alt+\\+left", adjust_window_position, args=(-1, 0))
    keyboard.add_hotkey("ctrl+alt+\\+right", adjust_window_position, args=(1, 0))

    # Register hotkey to quit the script
    keyboard.add_hotkey("ctrl+alt+q", lambda: exit())

    # Keep the script running
    keyboard.wait()

if __name__ == "__main__":
    main()
