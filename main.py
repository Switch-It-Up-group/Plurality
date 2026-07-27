import tkinter as tk
import Core, time, json, uuid
import itertools
import keyring
from tkinter import simpledialog

membersfile = Core.MembersFile()
members = membersfile.get_data()

RP = Core.RichPresence(time.time())

krnamespace = "siu-service_ring"
krsname = "Plurality"

if type(keyring.get_password(krnamespace, krsname)) == type(None) or len(keyring.get_password(krnamespace, krsname)) < 2:
    keyring.set_password(krnamespace, krsname, "{}")

kr_data: dict = json.loads(keyring.get_password(krnamespace, krsname))

if "sys_name" in kr_data:
    if kr_data["sys_name"] is None or kr_data["sys_name"] == "":
        newname = simpledialog.askstring("System name", "Looks like you dont have a system name. enter one below")
        kr_data["sys_name"] = newname
        keyring.set_password(krnamespace, krsname, json.dumps(kr_data))
else:
    newname = simpledialog.askstring("System name", "Looks like you dont have a system name. enter one below")
    kr_data["sys_name"] = newname
    keyring.set_password(krnamespace, krsname, json.dumps(kr_data))

if "webhooks" in kr_data:
    if kr_data["webhooks"] is None or kr_data["webhooks"] == "":
        newname = simpledialog.askstring("Discord webhooks", "It doesnt look like you have any discord webhooks. enter any you'd like below seperated with | No spaces. leave it empty for none")
        if len(newname) == 0:
            kr_data["webhooks"] = []
        else:
            kr_data["webhooks"] = newname.split("|")
        keyring.set_password(krnamespace, krsname, json.dumps(kr_data))
else:
    newname = simpledialog.askstring("Discord webhooks", "It doesnt look like you have any discord webhooks. enter any you'd like below seperated with | No spaces. leave it empty for none")
    if len(newname) == 0:
        kr_data["webhooks"] = []
    else:
        kr_data["webhooks"] = newname.split("|")
    keyring.set_password(krnamespace, krsname, json.dumps(kr_data))


WH = Core.WebhookConnector(kr_data["webhooks"], kr_data["sys_name"])
print(kr_data)




root = tk.Tk()
root.title("Plurality")

memberframe = tk.Frame(root)
optionsframe = tk.Frame(root)

def build_members():
    for num, chunk in enumerate(itertools.batched(members.items(), 4)):
        for i, (member, dat) in enumerate(chunk):
            if not "archived" in dat:
                dat["archived"] = False
            if not dat["archived"]:
                demomember = Core.Member(memberframe, member, dat)
                demomember.grid(column=i,row=num,padx=5,pady=3, sticky="nsew")

build_members()

def clear_tk(rt: tk.Tk | tk.Frame | tk.LabelFrame = root):
    for widget in rt.winfo_children():
        widget.destroy()

dropdownalters = {f"{dat["name"]}": uid for uid, dat in members.items()}

frontsel = Core.MultiSelect(optionsframe, dropdownalters, title="Select front")
frontsel.grid(column=0, row=1)

def update_front(fronters):
    RP.update(fronters)
    strfront = ""
    for front in fronters:
        strfront += f"{front} "
    dat = {
        "title": "Current fronts",
        "description": "Current fronts as of now",
        "message": strfront.rstrip(" "),
        "type": 1
    }
    WH.post(dat)

def change_webhooks():
    new = []
    for i in range(simpledialog.askinteger("Webhooks", "How many webhooks? (Max 5 min 0. 0 for none)", initialvalue=1, minvalue=0, maxvalue=5)):
        new.append(simpledialog.askstring("Enter webhook", f"Enter webhook #{i}"))
    kr_data["webhooks"] = new
    keyring.set_password(krnamespace, krsname, json.dumps(kr_data))
    WH.webhooks = new


def make_alter():
    global members, membersfile
    buffer: dict = {
        "color":{
            "red": 0,
            "green": 0,
            "blue": 0
        },
        "archived": False
    }
    for entry in ["name", "pronouns", "description"]:
        buffer[entry] = simpledialog.askstring(entry, f"Please enter alter {entry}.")

    members[str(uuid.uuid7())] = buffer
    membersfile.save_data(members)

def refresh_members():
    global members
    members = membersfile.get_data()
    clear_tk(memberframe)
    build_members()

tk.Button(optionsframe, text="Update front", command=lambda: update_front(frontsel.get_selected_keys())).grid(column=0, row=2, sticky="ew")
tk.Button(optionsframe, text="Update webhooks", command=lambda: change_webhooks()).grid(column=0, row=3, sticky="ew")
tk.Button(optionsframe, text="Refresh", command=lambda: refresh_members()).grid(column=0, row=4, sticky="ew")
tk.Button(optionsframe, text="Create member", command=lambda: make_alter()).grid(column=0, row=0, sticky="new")



memberframe.grid(column=0,row=0, sticky="nsew")
optionsframe.grid(column=1, row=0, padx=5, sticky="nsew")
root.mainloop()




