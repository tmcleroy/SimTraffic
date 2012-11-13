from Config import *
from RoadSystem import *
from RoadFeatures import * 
from Vehicle import *

class LightController:

    def __init__(self, overwatch):
        self.ow = overwatch
        self.intersections = self.getIntersections()


    def start(self, mode='independent'):
        for intersection in self.intersections:
            intersection.controller.start()
            

    def getIntersections(self):
        intersections = []
        for feature in self.ow.rs.features.values():
            if isinstance(feature, Intersection): intersections.append(feature)
        return intersections


    def setAll(self, lights, state):
        for intersection in self.intersections:
            intersection.controller.setLights(lights, state)


    def transAllToState(self, lights, state):
        for intersection in self.intersections:
            intersection.controller.transToState(lights, state)

