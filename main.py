import json
import sys
from pathlib import Path

from tkinter import ttk
import tkinter as tk

import itertools as it
import uuid


approot = Path.home() / ".Plurality"
membersdir = approot / "memberdata"
assets = approot / "assets"
pics = assets / "img"
memberpics = pics / "member"

directories = [approot,membersdir,assets,pics,memberpics]

alterjson = membersdir / "members.json"
alterjson.touch()
frontjson = membersdir / "fronters.json"
frontjson.touch()

for folder in directories:
    if not folder.exists():
        folder.mkdir()

def rtn_cmd(inp:str):
    word = inp.split()
    cmd = word[0].lower()
    return word, cmd

def questions(quest:list):
    resp = {}
    for Q in quest:
        answer = input(f"{Q} > ")
        resp[Q] = answer
    return resp

alters:dict = json.loads(alterjson.read_text())

def save():
    alterjson.write_text(json.dumps(alters, indent=True))

def t_or_f(q = "Are you sure?"):
    print(q, "(Y/N)")
    a = input("(Y/N) > ")
    if a.lower() == "y":
        return True
    else:
        return False


def add_mem(name:str, description:str= "", pronouns:str="They/Them", archived:bool = False, color:tuple = (0,0,0)):
    r,g,b = color
    alters[str(uuid.uuid4())] = {
        "name": name,
        "pronouns": pronouns,
        "description": description,
        "color": {
        "red": r,
        "green": g,
        "blue": b
        },
        "archived": archived
    }

    save()

def rem_mem(name:str):
    for alter in alters:
        if alters[alter][name] == name:
            alters.pop(alter)
    save()

def set_arc(name:str, archived: bool):
    for alter in alters:
        if alters[alter][name] == name:
            alters[alter]["archived"] = archived
    save()

print("-"*50)
print("Welcome to plurality")
print("-"*50)
strtcmds = """
            list | List a object | Params | -alters [-a] 
            help | Show these commands
            add | Add an alter. usage: Fill out the prompts
            archive | Archive a alter. Usage: Fill out the prompts
            remove | Remove a alter. Usage: Fill out the prompts

            exit | Exit plurality
"""
print(strtcmds)

while True:
    inp = input("Plurality > ")
    words, cmd = rtn_cmd(inp)
    if cmd == "exit":
        break
    elif cmd == "list":
        for alter in alters:
            dat = alters[alter]
            print(alter, dat["pronouns"], f"||Archived? {dat["archived"]}||")

    elif cmd == "help":
        print(strtcmds)

    elif cmd == "remove":
        REM_IN = questions(["name"])
        if t_or_f():
            rem_mem(REM_IN["name"])
            print("Member removed")
        else:
            print("No action taken")

    elif cmd == "add":
        if len(words) < 1:
            print("not enough parameters USAGE: add <Name> <Parameters>")
            continue
        else:
            adat = questions(["name", "description", "pronouns"])
            add_mem(adat["name"], adat["description"], adat["pronouns"])

    elif cmd == "archive":
        ARCHIVE_IN = questions(["name"])
        if t_or_f():
            set_arc(ARCHIVE_IN["name"], True)
        else:
            print("No action taken.")


    else:
        print("What?")

print("Thank you for using plurality")
save()
