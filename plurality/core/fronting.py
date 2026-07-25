import json
import uuid
from pathlib import Path
from .fileman import PluralityFile as PF
from .core import Core

pf = PF()

class Front:
    def __init__(self, core:Core):
        self.core = core

    def check_front(self, uid):
        pass