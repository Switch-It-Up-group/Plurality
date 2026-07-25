from pathlib import Path
import json

approot = Path.home() / ".Plurality"
membersdir = approot / "memberdata"
assets = approot / "assets"
pics = assets / "img"
memberpics = pics / "member"

directories = [approot, membersdir, assets, pics, memberpics]

for folder in directories:
    if not folder.exists():
        folder.mkdir()

alterjson = membersdir / "members.json"
alterjson.touch()
frontjson = membersdir / "fronters.json"
frontjson.touch()

class PluralityFile:
    def __init__(self):
        self.approot = approot
        self.membersdir = membersdir
        self.assets = assets
        self.pics = pics
        self.memberpics =memberpics

        self.directories = [self.approot, self.membersdir, self.assets, self.pics, self.memberpics]

        for folder in self.directories:
            if not folder.exists():
                folder.mkdir()

        self.alterjson = alterjson
        self.frontjson = frontjson

        files = [self.frontjson, self.alterjson]

        for file in files:
            file.touch()