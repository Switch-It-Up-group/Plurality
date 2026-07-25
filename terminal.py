import plurality as P
from pathlib import Path
import uuid
import time

core = P.Core()
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
print("-"*50)
print("Welcome to plurality")
print("-"*50)
strtcmds = """
            index | Indexes all of the alters and rebuilds the list of objects.
            
            list | Lists all alters
            help | Show these commands
            add | Add an alter. usage: Fill out the prompts
            remove | Remove a alter. Usage: Fill out the prompts

            exit | Exit plurality
"""
print(strtcmds)

while True:
    inp = input("Plurality > ")
    words, cmd = rtn_cmd(inp)
    if cmd == "exit":
        break

    elif cmd == "help":
        print(strtcmds)

    elif cmd == "index":
        index()

    elif cmd == "add":
        dat = questions(["name", "pronouns", "description"])
        core.make_member(dat["name"], dat["description"], dat["pronouns"])
        index()

    elif cmd == "search":
        sinp = input("Search > ")
        search(sinp)

    elif cmd == "remove":
        matches = []
        quest = questions(["name"])
        for uid in alters:
            alter = alters[uid]
            if quest["name"].lower() in alter.name.lower():
                matches.append(f"{alter.name}\x00{uid}")
        resp = options(matches, exit=1).split("\x00")
        if resp == ["exit-peruserrequest","exit-peruserrequest"]:
            continue
        subject:P.Alter = alters[resp[1]]
        code = subject.delete()
        if code == 0:
            print("Done. Reindexing plurality in")
            count_sleep(3)
            index()
        elif code == 1:
            print("Incorrect uuid start. Aborting...")

    elif cmd == "list":
        for alter in alters:
            alter:P.Alter = alters[alter]
            print(alter.name, alter.pronouns, '"', alter.description, '"')
    else:
        print("What?")

print("Thank you for using plurality")