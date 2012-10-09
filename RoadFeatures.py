import pygame
from Config import *

class Road:
    def __init__(self, name, id, screen, line, lane1, lane2, color=black):
        self.name = name
        self.id = id
        self.screen = screen
        self.color = color
        self.line = line
        self.lane1 = lane1
        self.lane2 = lane2
        self.isDrawable = True

    def getNumVehicles(self):
        return len(self.lane1.vehicles+self.lane2.vehicles)

    def isOdd(self):
        return self.id%2

    def isEven(self):
        return not self.isOdd()

    def draw(self):
        pygame.draw.lines(self.screen, self.color, False, self.line)


class Lane:

    def __init__(self, id, rules=''):
        self.id = id
        self.vehicles = []
		
        self.rules = rules
        self.allowsStraight = "straight" in rules
        self.allowsRight =  "right" in rules
        self.allowsLeft = "left" in rules

    def getLastVehicle(self):
        if len(self.vehicles)>0: return self.vehicles[-1]
        else: return False
        
class Anchor:
    def __init__(self, name, screen, x=0, y=0, color=purple, width=2, height=2):
        self.name = name
        self.x = x
        self.y = y
        self.screen = screen
        self.color = color
        self.width = width
        self.height = height
        self.isDrawable = True

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x-(self.width/2), self.y-(self.height/2), self.width, self.height), 0)



class Entrance:
    def __init__(self, name, screen, poleStack=[], x=0, y=0, width=5, height=5, color=green):
        self.name = name
        self.screen = screen
        self.poleStack = poleStack
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.isDrawable = True

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x-(self.height/2), self.y-(self.width/2), self.width, self.height), 0)

class Exit:
    def __init__(self, name, screen, x=0, y=0, width=5, height=5, color=red):
        self.name = name
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.isDrawable = True

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x-(self.height/2), self.y-(self.width/2), self.width, self.height), 0)



class LightPole:

    def __init__(self, name, id, screen, light1, light2, x=0, y=0, width=5, height=5, color=black):
        self.name = name
        self.id = int(id)
        self.screen = screen
        self.light1 = light1
        self.light2 = light2
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.isDrawable = True


    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y-(self.height/2), self.width, self.height), 0)

        #draw the pole
        #pygame.draw.rect(self.screen, self.color, (self.x,self.y,self.width,self.height))
        #draw the lights
        if self.id%2 == 1:
            pygame.draw.circle(self.screen, self.light1.color, (int(self.x+self.light1.diameter+(self.height/4)+2),int(self.y)), int(self.height/2))
            pygame.draw.circle(self.screen, self.light2.color, (int(self.x+self.light1.diameter+(self.height)+6),int(self.y)), int(self.height/2))
        elif self.id%2 == 0:
            pygame.draw.circle(self.screen, self.light1.color, (int(self.x+self.light1.diameter+(self.width/4)+2),int(self.y-(self.width/2))), int(self.width/2))
            pygame.draw.circle(self.screen, self.light2.color, (int(self.x+self.light2.diameter+(self.width/4)+2),int(self.y+(self.width/2))), int(self.width/2))


class Light:

    def __init__(self, name, state, diameter=3):
        self.name = name
        self.state = state
        self.diameter = diameter
        self.radius = diameter/2
        self.color = purple
        self.isDrawable = True

        if self.state == "go":self.color = green
        elif self.state == "stop":self.color = red
        elif self.state == "slow":self.color = yellow


    def setState(self, state):
        self.state = state

        if self.state == "go":self.color = green
        elif self.state == "stop":self.color = red
        elif self.state == "slow":self.color = yellow
