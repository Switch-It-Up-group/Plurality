import tkinter as tk
from tkinter import ttk
from pathlib import Path
import json


class Member(tk.LabelFrame):
    def __init__(self,uid:str, data:dict):
        super().__init__()

        self.data = data
        self.uid = uid

        self.name = tk.Label(self, text=data["name"])
        self.pronouns = tk.Label(self, text=data["pronouns"])

        self.name.grid(column=0, row=0, padx=5,pady=3)
        self.pronouns.grid(column=0, row=1, padx=5,pady=3)


class MultiSelectDropdown(ttk.Frame):
    def __init__(self, parent, entries: dict):
        super().__init__(parent)

        self.entries = entries
        self.variables = {}
        self.popup = None

        self.button = ttk.Button(
            self,
            text="Select entries",
            command=self.toggle_popup
        )
        self.button.pack(fill="x")

        for key in self.entries:
            self.variables[key] = tk.BooleanVar(value=False)

    def toggle_popup(self):
        if self.popup is not None and self.popup.winfo_exists():
            self.close_popup()
        else:
            self.open_popup()

    def open_popup(self):
        self.popup = tk.Toplevel(self)
        self.popup.overrideredirect(True)

        x = self.button.winfo_rootx()
        y = self.button.winfo_rooty() + self.button.winfo_height()

        self.popup.geometry(f"+{x}+{y}")

        frame = ttk.Frame(self.popup, padding=5)
        frame.pack(fill="both", expand=True)

        for key, variable in self.variables.items():
            ttk.Checkbutton(
                frame,
                text=key,
                variable=variable,
                command=self.update_button_text
            ).pack(anchor="w", fill="x")

        ttk.Button(
            frame,
            text="Done",
            command=self.close_popup
        ).pack(fill="x", pady=(5, 0))

    def close_popup(self):
        if self.popup is not None:
            self.popup.destroy()
            self.popup = None

    def update_button_text(self):
        selected = self.get_selected_keys()

        self.button.config(
            text=", ".join(selected) if selected else "Select entries"
        )

    def get_selected_keys(self):
        return [
            key
            for key, variable in self.variables.items()
            if variable.get()
        ]

    def get_selected_values(self):
        return [
            self.entries[key]
            for key in self.get_selected_keys()
        ]

    def get_selected_dict(self):
        return {
            key: self.entries[key]
            for key in self.get_selected_keys()
        }
