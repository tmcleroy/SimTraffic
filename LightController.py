from Config import *
from RoadSystem import *
from RoadFeatures import * 
from Vehicle import *

#currently, this class acts as an overseer for the IntersectionControllers
class LightController:

    def __init__(self, overwatch):
        self.ow = overwatch
        self.intersections = self.getIntersections()

    #start the IntersectionController of each Intersection
    def start(self, mode='independent'):
        for intersection in self.intersections:
            intersection.controller.start()
            

    def setTimingVars(self, yellowTime, minGreenTime, inactivityPause):
        for intersection in self.intersections:
            intersection.controller.setTimingVars(yellowTime, minGreenTime, inactivityPause)

    #returns all intersections governed by this LightController
    def getIntersections(self):
        intersections = []
        for feature in self.ow.rs.features.values():
            if isinstance(feature, Intersection): intersections.append(feature)
        return intersections


    #sets each light to the given state for each Intersection governed by this LightController
    def setAll(self, lights, state):
        for intersection in self.intersections:
            intersection.controller.setLights(lights, state)
