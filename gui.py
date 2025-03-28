import tkinter as tk
from tkinter import ttk
import os
from window_utils import (
    load_positions,
    save_positions,
    get_focused_window_title,
    get_focused_window_position,
)

CONFIG_FILE = "positions_config.json"


class WindowManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Window Manager")
        self.root.geometry("350x500")  # Slightly taller for extras

        title_font = ("Segoe UI", 12, "bold")
        label_font = ("Segoe UI", 10)

        # --- DARK MODE ---
        dark_bg = "#2e2e2e"
        dark_fg = "#e0e0e0"
        accent = "#444"

        self.root.configure(bg=dark_bg)

        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=dark_bg,
            foreground=dark_fg,
            fieldbackground=dark_bg,
            rowheight=22,
        )
        style.configure(
            "Treeview.Heading", background=accent, foreground=dark_fg, relief="flat"
        )
        style.map("Treeview", background=[("selected", "#555555")])

        style.configure("TButton", background=accent, foreground=dark_fg)
        style.map("TButton", background=[("active", "#555")])

        # Override default tkinter elements
        self.root.option_add("*Background", dark_bg)
        self.root.option_add("*Foreground", dark_fg)
        self.root.option_add("*Button.Background", accent)
        self.root.option_add("*Button.Foreground", dark_fg)
        self.root.option_add("*Entry.Background", "#3a3a3a")
        self.root.option_add("*Entry.Foreground", dark_fg)
        self.root.option_add("*Label.Background", dark_bg)
        self.root.option_add("*Label.Foreground", dark_fg)

        # Title at the top
        tk.Label(root, text="Window Manager", font=title_font).pack(pady=(10, 0))

        tk.Label(root, text="Focused Window:", font=label_font).pack(pady=(5, 0))

        self.focused_window_title = tk.Label(
            root, text="(None)", font=label_font, wraplength=330, justify="center"
        )
        self.focused_window_title.pack(pady=(0, 5))

        self.position_label = tk.Label(root, text="Position: ", font=label_font)
        self.position_label.pack(pady=2)

        # Treeview for hotkeys
        self.tree = ttk.Treeview(
            root, columns=("Hotkey", "X", "Y"), show="headings", height=6
        )
        self.tree.heading("Hotkey", text="Hotkey")
        self.tree.heading("X", text="X")
        self.tree.heading("Y", text="Y")
        self.tree.column("Hotkey", width=140, anchor="center")
        self.tree.column("X", width=80, anchor="center")
        self.tree.column("Y", width=80, anchor="center")
        self.tree.pack(expand=True, fill="both", padx=10, pady=5)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)

        tk.Button(
            button_frame, text="Remove Selected", command=self.remove_selected
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Refresh", command=self.refresh_data).pack(
            side=tk.LEFT, padx=5
        )

        # Controls info
        self.instructions = tk.Label(
            root,
            text=(
                "Controls:\n"
                "- Ctrl+Alt+\\ + Arrow Keys: Nudge window\n"
                "- Ctrl+Alt+S + 0-9: Save current window position\n"
                "- Ctrl+Alt+Q: Quit"
            ),
            justify="left",
            font=("Segoe UI", 9),
        )
        self.instructions.pack(pady=5)

        self.last_json_mtime = None
        self.last_focused = ("", "")

        self.refresh_data()
        self.poll_focused_window()
        self.watch_json_file()

    def refresh_data(self):
        self.positions = load_positions()
        self.tree.delete(*self.tree.get_children())
        for hotkey, (x, y) in self.positions.items():
            self.tree.insert("", "end", values=(hotkey, x, y))

    def remove_selected(self):
        selected = self.tree.selection()
        if not selected:
            return
        for item in selected:
            hotkey = self.tree.item(item, "values")[0]
            del self.positions[hotkey]
        save_positions(self.positions)
        self.refresh_data()

    def poll_focused_window(self):
        title = get_focused_window_title()
        pos = get_focused_window_position()
        if (title, pos) != self.last_focused:
            self.last_focused = (title, pos)
            self.focused_window_title.config(text=title or "N/A")
            self.position_label.config(text=f"Position: {pos or '(N/A)'}")
        self.root.after(500, self.poll_focused_window)

    def watch_json_file(self):
        try:
            mtime = os.path.getmtime(CONFIG_FILE)
            if self.last_json_mtime is None:
                self.last_json_mtime = mtime
            elif mtime != self.last_json_mtime:
                self.last_json_mtime = mtime
                self.refresh_data()
        except FileNotFoundError:
            pass
        self.root.after(1000, self.watch_json_file)


if __name__ == "__main__":
    root = tk.Tk()
    app = WindowManagerGUI(root)
    root.mainloop()
