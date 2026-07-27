from pathlib import Path
import yaml,json,struct
from PIL import Image
import PIL


pimgmagic = b"PLURALITYIMG"
pimgstruct = struct.Struct("<12sQQ")


approot = Path.home() / ".Plurality"
memberdata = approot / "memberdata"

def exists():
    for folder in [approot, memberdata]:
        if not folder.exists():
            folder.mkdir(parents=True)

class MembersFile:
    def __init__(self):
        self.pathfile = memberdata / "members.json"
        self.pathfile.touch()
        if len(self.pathfile.read_text()) < 2:
            self.pathfile.write_text("{}")


    def get_data(self):
        return json.loads(self.pathfile.read_text())
    def save_data(self, data:dict):
        try:
            self.pathfile.write_text(json.dumps(data, indent=4))
        except Exception as e:
            return {
                "status": "Exception",
                "data": {
                    "error": e
                }
            }
        return {
            "status": "Complete",
            "data": data
        }

class Assets:
    def __init__(self):
        self.assetsfolder = approot / "assets"
        if not self.assetsfolder.exists():
            self.assetsfolder.mkdir(parents=True)

    def get_image(self, uid:str, name:str):

        with open(f"{self.assetsfolder.resolve()}/img/member/{uid}/{name}.pluralimg", "rb") as f:
            magic, width, height = pimgstruct.unpack(f.read(pimgstruct.size))
            img = Image.frombytes("RGBA", (width,height), f.read())


            return img, width, height

    def save_image(self,uid:str,name:str, img:Image.Image):
        outbytes = b""
        outbytes += pimgstruct.pack(pimgmagic, img.width,img.height)
        imgrgba = img.convert("RGBA")
        outbytes += imgrgba.tobytes()
        file = self.assetsfolder / f"img/member/{uid}/{name}.pluralimg"
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_bytes(outbytes)
