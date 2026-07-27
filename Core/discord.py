from pypresence import Presence
from tkinter import messagebox
import requests as web
import Core.helpers as help


CLIENT_ID = "1530665857456410654"

class RichPresence:
    def __init__(self, start):
        self.rpc = Presence(CLIENT_ID)
        self.rpc_works = True
        try:
            self.rpc.connect()
            self.rpc.update(
                start=start,
                state="Waiting for fronters...",
                details="Gathering..."
            )
        except ConnectionRefusedError as error:
            self.rpc_works = False
            print("You had an error:", error)
            print("Rich presence will not work. make sure you have a webhook setup for updates. else everything stays here.")
            messagebox.showerror("Plurality has an error", f"Plurality's Discord RPC had an error! {error}. plurality will still work. we hope")
        self.start = start
        self.fronters = ["Fallback1", "Fallback2", "Fallback3"]

    def update(self, fronters:list):
        self.fronters = fronters
        buff = ""
        buffer = ""
        for num, fronter in enumerate(fronters):
            if num % 2 == 1:
                if len(f"{fronter}, ") + len(buff) < 128:
                    buff += f"{fronter}, "
            elif num % 2 == 0:
                if len(f"{fronter}, ") + len(buffer) < 128:
                    buffer += f"{fronter}, "
        if self.rpc_works:
            self.rpc.update(
                start=self.start,
                state=buff,
                details=buffer
            )
        else:
            print("Unable to update. RPC Out of order")

class WebhookConnector:
    def __init__(self, webhooks:list[str], sysname: str = "Generic System"):
        self.webhooks = webhooks
        self.sysname = sysname

    def post(self, data:dict):
        utypes = [("Generic notification", help.decimal_color_rgb((148,148,148))), ("Front Update", help.decimal_color_rgb((148,130,255)))]
        try:
            ty = int(data["type"])
        except:
            ty = 0

        typ, color = utypes[ty]

        dat = {
            "username": f"Plurality | {self.sysname}",
            "embeds": [
                {
                    "title": typ,
                    "description": f"{self.sysname}",
                    "color": color,
                    "fields": [
                        {
                            "name": data.get("title", f"generic title"),
                            "value": data.get("message", "Unable to get content")
                        }
                    ]

                }
            ]
        }
        for webhook in self.webhooks:
            response = web.post(
                url=webhook,
                json=dat,
                timeout=5
            )
            if response.status_code == 204:
                print("Webhook sent successfully")
            else:
                print(f"Failed: {response.status_code}")
                print(response.text)