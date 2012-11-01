from Config import *
from RoadSystem import *
from RoadFeatures import * 
from Vehicle import *
from LightController import *

class Overwatch:

    def __init__(self, rs, vehics):
        self.rs = rs
        self.vehics = vehics
        self.lc = LightController(self)


"""
    def setAllLights(self, state):
        for feature in self.rs.features.values():
            if isinstance(feature, LightPole) : feature.setAllLights(state)
    

"""
