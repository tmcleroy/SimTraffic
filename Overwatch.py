from Config import *
from LightController import *

class Overwatch:

    def __init__(self, rs, vehics):
        self.rs = rs
        self.vehics = vehics
        self.lc = LightController(self)
        
    def removeVehic(self, vehic):
        self.vehics.remove(vehic)
