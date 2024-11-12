import win32gui
import win32con


def move_focused_window_to_top_left():
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        # Move the window
        win32gui.SetWindowPos(
            hwnd, win32con.HWND_TOP, -7, -30, 0, 0, win32con.SWP_NOSIZE
        )
    else:
        print("No window is currently in focus.")


if __name__ == "__main__":
    move_focused_window_to_top_left()
