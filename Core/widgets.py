import tkinter as tk
from tkinter import ttk
from pathlib import Path
import json


class Member(tk.LabelFrame):
    def __init__(self,parent,uid:str, data:dict):
        super().__init__(parent)

        self.data = data
        self.uid = uid

        self.name = tk.Label(self, text=data["name"])
        self.pronouns = tk.Label(self, text=data["pronouns"])

        self.name.grid(column=0, row=0, padx=5,pady=3, sticky="nsew")
        self.pronouns.grid(column=0, row=1, padx=5,pady=3, sticky="nsew")


class MultiSelect(ttk.Frame):
    def __init__(self, parent, entries: dict, title="Select entries"):
        super().__init__(parent)

        self.entries = entries
        self.title = title
        self.variables = {}
        self.popup = None

        self.button = ttk.Button(
            self,
            text=title,
            command=self.open_popup
        )
        self.button.pack(fill="x")

        for key in self.entries:
            self.variables[key] = tk.BooleanVar(value=False)

    def open_popup(self):
        if self.popup is not None and self.popup.winfo_exists():
            self.popup.lift()
            self.popup.focus_force()
            return

        self.popup = tk.Toplevel(self)
        self.popup.title(self.title)
        self.popup.geometry("350x400")
        self.popup.minsize(250, 200)
        self.popup.transient(self.winfo_toplevel())

        self.popup.protocol("WM_DELETE_WINDOW", self.close_popup)

        container = ttk.Frame(self.popup, padding=10)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(
            container,
            highlightthickness=0
        )

        scrollbar = ttk.Scrollbar(
            container,
            orient="vertical",
            command=canvas.yview
        )

        checkbox_frame = ttk.Frame(canvas)

        checkbox_frame.bind(
            "<Configure>",
            lambda event: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas_window = canvas.create_window(
            (0, 0),
            window=checkbox_frame,
            anchor="nw"
        )

        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfigure(
                canvas_window,
                width=event.width
            )
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        for key, variable in self.variables.items():
            ttk.Checkbutton(
                checkbox_frame,
                text=str(key),
                variable=variable
            ).pack(
                anchor="w",
                fill="x",
                padx=5,
                pady=3
            )

        button_frame = ttk.Frame(self.popup, padding=10)
        button_frame.pack(fill="x")

        ttk.Button(
            button_frame,
            text="Select all",
            command=self.select_all
        ).pack(side="left")

        ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_all
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Done",
            command=self.close_popup
        ).pack(side="right")

    def close_popup(self):
        self.update_button_text()

        if self.popup is not None:
            self.popup.destroy()
            self.popup = None

    def select_all(self):
        for variable in self.variables.values():
            variable.set(True)

    def clear_all(self):
        for variable in self.variables.values():
            variable.set(False)

    def update_button_text(self):
        selected = self.get_selected_keys()

        if not selected:
            text = "Select entries"
        elif len(selected) <= 3:
            text = ", ".join(map(str, selected))
        else:
            text = f"{len(selected)} entries selected"

        self.button.config(text=text)

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

    def set_selected(self, keys):
        selected_keys = set(keys)

        for key, variable in self.variables.items():
            variable.set(key in selected_keys)

        self.update_button_text()
