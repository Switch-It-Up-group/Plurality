import tkinter as tk
import Core, time, json
import itertools
import keyring

membersfile = Core.MembersFile()
members = membersfile.get_data()

RP = Core.RichPresence(time.time())

krnamespace = "tdjs_siu-service_ring"
krsname = "Plurality"

if type(keyring.get_password(krnamespace, krsname)) == type(None) or len(keyring.get_password(krnamespace, krsname)) < 2:
    keyring.set_password(krnamespace, krsname, "{}")

kr_data = json.loads(keyring.get_password(krnamespace, krsname))


root = tk.Tk()



root.title("Plurality")

for num, chunk in enumerate(itertools.batched(members.items(), 4)):
    for i, (member, dat) in enumerate(chunk):
        demomember = Core.Member(member, dat)
        demomember.grid(column=i,row=num,padx=5,pady=3, sticky="nsew")

dropdownalters = {f"{dat["name"]}": uid for uid, dat in members.items()}

frontsel = Core.MultiSelectDropdown(root, dropdownalters)
frontsel.grid(column=4, row=len(members)+1)

def update_front(fronters):
    RP.update(fronters)

tk.Button(root, text="Update front", command=lambda: update_front(frontsel.get_selected_keys())).grid(column=4, row=len(members)+2)

root.mainloop()



