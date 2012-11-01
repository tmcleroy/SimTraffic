from Config import *
from RoadSystem import *
from RoadFeatures import * 
from Vehicle import *

class LightController:

    def __init__(self, overwatch):
        self.ow = overwatch
        self.intersections = self.getIntersections()
        

    def getIntersections(self):
        intersections = []
        for feature in self.ow.rs.features.values():
            if isinstance(feature, Intersection): intersections.append(feature)
        return intersections


    def setAllLights(self, state):
        for intersection in self.intersections:
            intersection.controller.setAllLights(state)

    def transAllToState(self, state):
        for intersection in self.intersections:
            intersection.controller.transAllToState(state)
