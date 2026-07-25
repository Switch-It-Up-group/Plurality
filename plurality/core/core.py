import json
import uuid
import keyring
from pathlib import Path
from .alters import Alter
from .fileman import PluralityFile as PF

pf = PF()


class Core:
    def __init__(self):

        self.altersdb = json.loads(pf.alterjson.read_text())
        self.frontdb = json.loads(pf.frontjson.write_text())


    def save(self):
        pf.alterjson.write_text(json.dumps(self.altersdb, indent=4))
        pf.frontjson.write_text(json.dumps(self.frontdb, indent=4))

    def gen_uid(self):
        return str(uuid.uuid7())

    def make_member(self, name:str, desc:str, pronouns:str):
        uid = self.gen_uid()
        self.altersdb[uid] = {
            "name": name,
            "pronouns": pronouns,
            "description": desc,
            "color":{
            "red": 0,
            "green": 0,
            "blue":0
        },
            "archived": False
        }
        self.save()
        return uid