import time, threading
from threading import *


class IntersectionController:

    def __init__(self, p1, p2, p3, p4, r1, r2, r3 ,r4):
        self.pole1 = p1
        self.pole2 = p2
        self.pole3 = p3
        self.pole4 = p4
        self.poles = [self.pole1, self.pole2, self.pole3, self.pole4]

        self.road1 = r1
        self.road2 = r2
        self.road3 = r3
        self.road4 = r4
        self.roads = [self.road1, self.road2, self.road3, self.road4]

        self.oddPoles = [self.poles[0], self.poles[2]]
        self.evenPoles = [self.poles[1], self.poles[3]]

        self.prev = self.getMostPopulatedRoad()
        self.prevfc = 0


    def auto(self, mode):
        if mode == "mostPopulated":
            #if the most populated road changes from even to odd, change flow
            if not (self.getMostPopulatedRoad().isEven() == self.prev.isEven()):
                if self.getMostPopulatedRoad().isEven():
                    self.evenStraightFlow()
                else:
                    self.oddStraightFlow()
            self.prev = self.getMostPopulatedRoad()
                    

    def getMostPopulatedRoad(self):
        #default
        max = self.road1
        for road in self.roads:
            if road.getNumVehicles() > max.getNumVehicles(): max = road
        return max


    def oddStraightFlow(self):
        self.setStatesXtoY("go", "slow")
        t = Timer(3, self.setOddEvenState, ["odd","go"])
        u = Timer(3, self.setOddEvenState, ["even","stop"])
        t.start()
        u.start()
        
    def evenStraightFlow(self):
        self.setStatesXtoY("go", "slow")
        t = Timer(3, self.setOddEvenState, ["odd","stop"])
        u = Timer(3, self.setOddEvenState, ["even","go"])
        t.start()
        u.start()



    def oddLeftOnlyFlow(self):
        for pole in self.oddPoles:
            pole.light1.setState("left-green")
            pole.light2.setState("stop")

        for pole in self.evenPoles:
            pole.light1.setState("stop")
            pole.light2.setState("stop")


    def evenLeftOnlyFlow(self):
        for pole in self.evenPoles:
            pole.light1.setState("left-green")
            pole.light2.setState("stop")

        for pole in self.oddPoles:
            pole.light1.setState("stop")
            pole.light2.setState("stop")


    def specificRoadFlow(self, road):
        road -= 1
        self.poles[road].light1.setState("left-green")
        self.poles[road].light2.setState("go")

        for pole in self.poles:
            if self.poles.index(pole) != road:
                pole.light1.setState("stop")
                pole.light2.setState("stop")

    #iterates through each pole and sets it's
    #lights states to y if they are currently x
    def setStatesXtoY(self, x, y):
        for pole in self.poles:
            if pole.light1.state == x: pole.light1.setState(y)
            if pole.light2.state == x: pole.light2.setState(y)

    #oe is either "odd" or "even", state is the state to
    #which either all odds or evens will be set
    def setOddEvenState(self, oe, state):
        if   oe == "odd":                        
            for pole in self.oddPoles:
                pole.light1.setState(state)
                pole.light2.setState(state)
        elif oe == "even":
            for pole in self.evenPoles:
                pole.light1.setState(state)
                pole.light2.setState(state)


    def setAll(self, state):
        for pole in self.poles:
            pole.light1.setState(state)
            pole.light2.setState(state)




