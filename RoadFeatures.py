import pygame
from Config import *
from IntersectionController import IntersectionController

#this file contains the features that make up a RoadSystem

class Road:
    def __init__(self, name, id, screen, lines, lane1, lane2, segmentSize, roadColor=road_grey, lineColor=road_line_yellow, layer=0):
        self.name = name
        self.id = id
        self.screen = screen
        self.roadColor = roadColor
        self.lineColor = lineColor
        self.lines = lines
        self.lanes = [lane1,lane2]
        self.segmentSize = segmentSize
        self.isDrawable = True
        self.layer = layer
        self.rect = None
        self.setDraw()


    def __repr__(self):
        return "Road Object: "+self.name

    def getNumVehicles(self):
        return len(self.lane1.vehicles+self.lane2.vehicles)

    def isOdd(self):
        return self.id%2

    def isEven(self):
        return not self.isOdd()

    def setDraw(self):
        lineRect = pygame.draw.lines(self.screen, self.lineColor, False, self.lines)
        if self.id == 1 or self.id == 3:
            lineRect.width *= self.segmentSize * 4
            lineRect.x -= lineRect.width/2
        elif self.id == 2 or self.id == 4:
            lineRect.height *= self.segmentSize * 4
            lineRect.y -= lineRect.height/2
        self.rect = lineRect

    def draw(self):
        pygame.draw.rect(self.screen, self.roadColor, self.rect)
        pygame.draw.lines(self.screen, self.lineColor, False, self.lines)



class Lane:

    def __init__(self, id, rules=''):
        self.id = id
        self.vehicles = []
		
        self.rules = rules
        self.allowsStraight = "straight" in rules
        self.allowsRight =  "right" in rules
        self.allowsLeft = "left" in rules

    def __repr__(self):
        return "Lane Object: "+self.name

    def getLastVehicle(self):
        if len(self.vehicles)>0: return self.vehicles[-1]
        else: return False
        
class Anchor:
    def __init__(self, name, screen, x=0, y=0, color=purple, width=2, height=2, layer=0):
        self.name = name
        self.x = x
        self.y = y
        self.screen = screen
        self.color = color
        self.width = width
        self.height = height
        self.isDrawable = False
        self.layer = layer

    def __repr__(self):
        return "Anchor Object: "+self.name

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x-(self.width/2), self.y-(self.height/2), self.width, self.height), 0)

class Intersection:
    def __init__(self, name, anchor, poles):
        self.name = name
        self.x, self.y = anchor.x, anchor.y
        self.poles = poles
        self.controller = IntersectionController(self, TIMING)
        self.isDrawable = False

    def __repr__(self):
        return "Intersection Object: "+self.name

class Entrance:
    def __init__(self, name, screen, poleStack=[], x=0, y=0, width=5, height=5, color=green, id=0, layer=1):
        self.name = name
        self.id = id
        self.screen = screen
        self.poleStack = poleStack
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.road = None
        self.isDrawable = False#True
        self.layer = layer

    def __repr__(self):
        return "Entrance Object: "+self.name

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x-(self.height/2), self.y-(self.width/2), self.width, self.height), 0)

class Exit:
    def __init__(self, name, screen, x=0, y=0, width=5, height=5, color=red, id=0, layer=1):
        self.name = name
        self.id = id
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.isDrawable = False#True
        self.layer = layer

    def __repr__(self):
        return "Exit Object: "+self.name

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x-(self.height/2), self.y-(self.width/2), self.width, self.height), 0)



class LightPole:

    def __init__(self, name, id, screen, light1, light2, x=0, y=0, width=5, height=5, color=black, layer=1):
        self.name = name
        self.id = int(id)
        self.screen = screen
        self.lights = [light1,light2]
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.vehics = []
        self.isDrawable = True
        self.layer = layer


    def __repr__(self):
        return "LightPole Object: "+self.name
    

    #returns the intersection that contains this lightpole
    def getParent(self, intersections):
        for inter in intersections:
            for pole in inter.poles:
                if self.name == pole.name: return inter
        return None

    def draw(self):
        #draw pole
        pygame.draw.rect(self.screen, self.color, (self.x, self.y-(self.height/2), self.width, self.height), 0)
        #draw the lights
        if self.id%2 == 1:
            pygame.draw.circle(self.screen, self.lights[0].color, (int(self.x+self.lights[0].diameter),int(self.y)), int(self.lights[0].diameter))#int(self.height/2))
            pygame.draw.circle(self.screen, self.lights[1].color, (int(self.x+self.lights[1].diameter*3),int(self.y)), int(self.lights[0].diameter))#iint(self.height/2))
        elif self.id%2 == 0:
            pygame.draw.circle(self.screen, self.lights[0].color, (int(self.x+self.lights[0].diameter),int(self.y-(self.width/2))), int(self.lights[0].diameter))#iint(self.width/2))
            pygame.draw.circle(self.screen, self.lights[1].color, (int(self.x+self.lights[1].diameter),int(self.y+(self.width/2))), int(self.lights[0].diameter))#iint(self.width/2))


class Light:

    def __init__(self, name, state, diameter=5):
        self.name = name
        self.state = state
        self.diameter = diameter
        self.radius = diameter/2.0
        self.color = purple
        self.isDrawable = False


        if self.state == "go":self.color = green
        elif self.state == "stop":self.color = red
        elif self.state == "slow":self.color = yellow

    def __repr__(self):
        return "Light Object: "+self.name

    def setState(self, state):
        self.state = state

        if self.state == "go":self.color = green
        elif self.state == "stop":self.color = red
        elif self.state == "slow":self.color = yellow

class SpawnFrequencyIndex:

    def __init__(self):
        self.spawnsPerMin = {}
        self.mods = {}

    #sets the modulus values that will be used to spawn the vehicles a set number of times per minute
    def setMods(self):
        for key in self.spawnsPerMin.keys():
            self.mods[key] = int((FRAMERATE*60)/self.spawnsPerMin[key])
        
