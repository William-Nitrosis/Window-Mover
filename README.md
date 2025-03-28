# 🪟 Window-Mover

**Window-Mover** is a lightweight tool for quickly positioning windows on your screen using keyboard shortcuts — with both a colorful console version and a modern dark-themed GUI.


## ✨ Features
- Move focused windows with hotkeys (`Ctrl+Alt+<key>`)
- Fine-tune position with arrow keys (`Ctrl+Alt+\`)
- Save positions instantly (`Ctrl+Alt+S + <number>`)
- GUI with live updates, dark mode, and click-to-manage interface
- Configurable positions saved in `positions_config.json`


## 📦 Requirements
Install dependencies with:

```bash
pip install keyboard pywin32 colorama
```

(Optional for future mic/volume features):

```bash
pip install pycaw comtypes
```


## 🚀 Usage
### Console Mode
```bash
python window_mover.py
```

- Uses hotkeys to move and save window positions
- Press `Ctrl+Alt+Q` to quit

### GUI Mode
```bash
python gui.py
```

- Clean interface to view, add, and remove hotkey positions
- Automatically refreshes on focus or config changes


## 🛠️ Build Executables
To build both versions into `.exe` files:
```bash
python build_exe.py
```

Outputs:
- `build/window_mover.exe` – console version
- `build/gui.exe` – GUI version


## 📝 Config
Positions are saved in:
```json
{
  "ctrl+alt+1": [100, 100],
  "ctrl+alt+2": [200, 200]
}
```

You can edit `positions_config.json` manually or use the GUI.


## 🪟 Enjoy faster, cleaner window control!
