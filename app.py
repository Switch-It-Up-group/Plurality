import plurality as P
from pathlib import Path
import json

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox,simpledialog

import uuid
import time

core = P.Core()
buffer:dict
alters = {}

def questions(quest:list):
    resp = {}
    for question in quest:
        answer = input(f"{question} > ")
        resp[question]=answer
    return resp

def options(opt:list, exit:int = 0):
    for num, option in enumerate(opt):
        print(f"[{num}]: {option}")
    print("Select an option")
    if exit == 1:
        print("exit to exit")
    response = input("Options > ")
    if response.lower() == "exit":
        return "exit-peruserrequest\x00exit-peruserrequest"
    for num, option in enumerate(opt):
        if str(num) == response:
            return option
        else:
            continue
    print("I dont have that in index.")
    return options(opt, exit=exit)


def t_or_f(q = "Are you sure?"):
    print(q, "(Y/N)")
    a = input("(Y/N) > ")
    if a.lower() == "y":
        return True
    else:
        return False

def count_sleep(s):
    t = s
    for i in range(s):
        print(f"{t}...")
        t -= 1
        time.sleep(1)

def rtn_cmd(inp:str):
    if len(inp) < 1:
        inp = str(uuid.uuid4())
    word = inp.split()
    cmd = word[0].lower()
    return word, cmd

def search(s=""):
    print("Searching for", s)
    matches = []
    for alter in alters:
        dat = alters[alter]
        name = dat.name
        if s.lower() in name.lower():
            matches.append(f"{name}\x00{alter}")
    for result in matches:
        r = result.split("\x00")
        print(r[0], r[1])


def index():
    global alters
    alters = {}
    for alter in core.altersdb:
        member = P.Alter(core, alter)
        alters[member.uid] = member
        print("indexed", alter, member.name)

index()
root = tk.Tk()
root.title("Plurality")
root.geometry("500x600")

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

controls = tk.Frame(root)
controls.grid(row=0, column=0, columnspan=2, sticky="ew")

container = tk.Frame(root)
container.grid(row=1, column=0, columnspan=2, sticky="nsew")

container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

canvas = tk.Canvas(container)
scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)

af = tk.Frame(canvas)
af_window = canvas.create_window((0, 0), window=af, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set)

canvas.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")


def update_scroll_region(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))


def resize_af(event):
    canvas.itemconfig(af_window, width=event.width)


def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


def on_linux_scroll_up(event):
    canvas.yview_scroll(-1, "units")


def on_linux_scroll_down(event):
    canvas.yview_scroll(1, "units")


af.bind("<Configure>", update_scroll_region)
canvas.bind("<Configure>", resize_af)

canvas.bind_all("<MouseWheel>", on_mousewheel)
canvas.bind_all("<Button-4>", on_linux_scroll_up)
canvas.bind_all("<Button-5>", on_linux_scroll_down)


def yn_popups(quest: list):
    resp = {}

    for question in quest:
        answer = messagebox.askyesno(message=question)
        resp[question] = answer

    return resp


def quest_popups(quest: list):
    resp = {}

    for question in quest:
        answer = simpledialog.askstring(question, f"Enter {question}:")
        resp[question] = answer

    return resp


def delete(uid: str):
    dele = messagebox.askyesno("Warning", message="Are you sure?")
    print(dele)

    if dele:
        dat: P.Alter = alters[uid]
        dat.delete(user=1)

        messagebox.showinfo(message=f"Member {dat.name} Deleted.")

        alters.pop(uid)
        reindex()
    else:
        messagebox.showinfo(message="No action taken")


def reindex():
    index()

    for widget in af.winfo_children():
        widget.destroy()

    for num, uid in enumerate(alters):
        alter = alters[uid]
        alter: P.Alter = alter

        tk.Label(
            af,
            text=f"{alter.name} {alter.pronouns}"
        ).grid(row=num, column=0, sticky="w", padx=5, pady=2)

        tk.Button(
            af,
            text="Delete",
            command=lambda uauid=uid: delete(uauid)
        ).grid(row=num, column=1, sticky="e", padx=5, pady=2)

        tk.Button(
            af,
            text="Rename",
            command=lambda uauid=uid: rename(uauid)
        ).grid(row=num, column=2, sticky="e", padx=5, pady=2)

    update_scroll_region()


def new():
    info = quest_popups(["name", "pronouns", "description"])

    if info["name"] is None or info["pronouns"] is None or info["description"] is None:
        messagebox.showinfo(message="No member created.")
        return

    core.make_member(info["name"], info["description"], info["pronouns"])
    reindex()

def rename(uid:str):
    alter:P.Alter = alters[uid]
    name = simpledialog.askstring("Name", f"Enter new name for {alter.name} ({alter.uid.split("-")[0]})")
    alter.name = name
    alter.update_db()
    core.save()
    reindex()

tk.Button(controls, text="ReIndex", command=reindex).grid(row=0, column=0)
tk.Button(controls, text="New", command=new).grid(row=0, column=1)

reindex()

if __name__ == '__main__':
    root.mainloop()