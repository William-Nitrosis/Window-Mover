# **Window-Mover**

Window-Mover is a Python script that lets you move windows around your screen using customizable keyboard shortcuts. It also allows you to dynamically add new shortcuts to move windows to specific positions and supports fine-tuned movement using arrow keys with adjustable speed.


## **Features**
- **Predefined Hotkeys**: Move the currently focused window to preset positions using key combinations.
- **Dynamic Shortcut Creation**: Create new shortcuts on-the-fly by saving the current window position to a hotkey (`Ctrl+Alt+S + Number`).
- **Fine-tuned Adjustments**: Move windows pixel-by-pixel with adjustable speed using arrow keys (`Ctrl+Alt+\\` + Arrow Keys).
- **Customizable Configuration**: Load and save all shortcuts in a JSON file (`positions_config.json`), allowing you to persist configurations across sessions.
- **Hotkey Management**: Automatically refresh and apply new configurations after saving a new shortcut.
- **Cross-platform**: Designed for Windows with simple configuration and use.


## **Requirements**
- Python 3.10 or later
- Libraries:
  - `keyboard`
  - `win32gui`
  - `win32con`
  - `colorama`

Install dependencies with:
```bash
pip install keyboard pywin32 colorama
```

**OR**

Download the exe from the releases page.


## **How It Works**

### **Hotkeys**
- **Predefined Window Positions**:
  - Use `Ctrl+Alt+<key>` to move the currently focused window to a predefined position.
  - Example: `Ctrl+Alt+1` moves the window to position `(-7, -30)`.

- **Dynamic Shortcut Creation**:
  - To create a new shortcut:
    1. Move a window to your desired position.
    2. Hold `Ctrl+Alt+S` and press a number (e.g., `1`).
    3. The current window's position is saved to the configuration file as `Ctrl+Alt+<number>`.

- **Fine-tuned Movement**:
  - Hold `Ctrl+Alt+\\` and press the arrow keys to move the window in small increments.
  - Movement speed increases the longer the arrow key is held.

- **Quit the Program**:
  - Press `Ctrl+Alt+Q` to exit the program.


## **How to Use**
1. **Run the Script**:
   - Execute the script with `python window_mover.py`.

2. **Predefined Positions**:
   - The script comes with some default hotkeys defined in the `positions_config.json` file:
     ```json
     {
         "ctrl+alt+1": [-7, -30],
         "ctrl+alt+2": [-7, 35],
         "ctrl+alt+3": [100, 100]
     }
     ```
   - Modify these positions or add your own in the JSON file.

3. **Create New Hotkeys**:
   - Move the window to a desired position.
   - Hold `Ctrl+Alt+S` and press a number key to save this position.

4. **Move Windows**:
   - Use the hotkey (`Ctrl+Alt+<key>`) to move the window to the saved position.

5. **Adjust Window Position**:
   - Hold `Ctrl+Alt+\\` and use the arrow keys for precise movement.




## **GUI Version (Optional)**

If you prefer not to use the terminal, a dark-mode GUI version is also included!

### **Features**
- Shows currently focused window and its screen position
- View, add, and remove all saved hotkey positions
- Automatically refreshes when the active window changes or the config file is updated
- Fully keyboard-free interface with built-in help
- Clean, minimal dark theme

### **Usage**
1. Run `gui.exe` (from the build folder) or `python gui.py`
2. The interface will open, showing your current focused window and saved hotkeys
3. Use the "Remove Selected" or "Refresh" buttons as needed
4. Hotkeys added via the console will sync automatically with the GUI (and vice versa)

### 🔄 Building Both Versions

Both versions can be built using:

```bash
python build_exe.py
```

This creates:
- `build/window_mover.exe` (console version)
- `build/gui.exe` (GUI version)

## **File Structure**
- **`window_mover.py`**: The main script.
- **`positions_config.json`**: The configuration file that stores all hotkeys and their corresponding positions.


## **Customization**
1. **Editing Configuration**:
   - Open `positions_config.json` in a text editor.
   - Add or modify positions using the format:
     ```json
     {
         "ctrl+alt+<key>": [x, y]
     }
     ```
   - Save the file and restart the script.

2. **Dynamic Updates**:
   - No need to restart! Save positions on-the-fly using `Ctrl+Alt+S + <number>`.


## **Example**
1. Move a window to position `(200, 300)`.
2. Hold `Ctrl+Alt+S` and press `1`.
3. The window's position is saved as `Ctrl+Alt+1`.
4. Press `Ctrl+Alt+1` to move the window to `(200, 300)` whenever needed.


## **Known Issues**
- Only works on Windows (due to reliance on `win32gui` and `win32con`).
- Requires administrator privileges if hotkeys don't respond in some applications.


## **Contributing**
Feel free to submit issues, suggestions, or pull requests to improve the project. Contributions are always welcome!


## **License**
This script is distributed under the MIT License. See `LICENSE` for more details.


With **Window-Mover**, you can save time and effort by efficiently managing your windows with hotkeys. Happy window managing! 🎉