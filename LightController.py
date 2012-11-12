import threading
from Config import *
from RoadSystem import *
from RoadFeatures import * 
from Vehicle import *

class LightController:

    def __init__(self, overwatch):
        self.ow = overwatch
        self.intersections = self.getIntersections()


    def start(self):
        for intersection in self.intersections:
            intersection.controller.start()
            #intersection.controller.join()
            
            
    def auto(self):
        print('asdfasdfafd')
        
        """
        t = threading.Thread(target=intersection.controller.auto)
        if not t.is_alive():
            t = threading.Thread(target=intersection.controller.auto)
            t.start()
        """
        #ntersection.controller.auto()
    

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

