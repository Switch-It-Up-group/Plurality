from pypresence import Presence
from tkinter import messagebox

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
        self.fronters = ["Al", "DJ", "Dogday"]

    def update(self, fronters:list):
        self.fronters = fronters
        buff = ""
        buffer = ""
        for num, fronter in enumerate(fronters):
            if num % 2 == 1:
                buff += f"{fronter}, "
            elif num % 2 == 0:
                buffer += f"{fronter}, "
        if self.rpc_works:
            self.rpc.update(
                start=self.start,
                state=buff,
                details=buffer
            )
        else:
            print("Unable to update. RPC Out of order")