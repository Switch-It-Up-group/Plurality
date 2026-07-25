import json
from pathlib import Path
import uuid

def check_alter(uid, db:dict):
    if uid in db:
        return True
    else:
        return False

class Alter:
    def __init__(self, core, uid:str):
        dat = core.altersdb[uid]
        self.core = core
        self.uid = uid
        self.name = dat["name"]
        self.pronouns = dat["pronouns"]
        self.description = dat["description"]
        self.color:dict = dat["color"]
        self.archived:bool = dat["archived"]

    def update_db(self):
        dat = self.core.altersdb[self.uid]
        dat["name"] = self.name
        dat["pronouns"] = self.pronouns
        dat["description"] = self.description
        dat["color"] = self.color
        dat["archived"] = self.archived
    def archive(self):
        self.archived = True
        self.update_db()
        self.core.save()

    def delete(self, user = 0):
        if user == 0:
            print("Are you sure?")
            print(f"Type the start of the member's uuid ({self.uid.split("-")[0]}) EXACTLY to confirm")
            response = input("DANGER > ")
            if response == self.uid.split("-")[0]:
                self.core.altersdb.pop(self.uid)
                self.core.save()
                return 0
            else:
                return 1
        elif user == 1:
            self.core.altersdb.pop(self.uid)
            self.core.save()
            return 0
