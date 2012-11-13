import pygame, math, random
from Config import *
from RoadFeatures import *
pygame.init()


roadWidth = 4
laneWidth = 2
poleWidth = 5
poleHeight = 10

#should be 39 according to the equation describing 
#how fast a vehicle stops...pixels to stop = 39 * speed
eq = 39

#degrees in radians that define car movement direction
up = 0
down = math.pi
left = math.pi/2
right = (3*math.pi)/2

baseSpeed = 0.001
greenSpeed = 0.5
yellowSpeed = 0.3
vehicStop = None
killDistance = 100

class Vehicle:

    #CONSTRUCTOR
    def __init__(self, screen, roadSystem, entrance, road, lane, nextVehic, exit, ow):
        self.screen = screen
        self.entrance = entrance
        self.road = road
        self.lane = lane
        self.roadSystem = roadSystem
        self.path = self.roadSystem.getPath(entrance,exit)
        self.direction = "forward"
        self.image = 'car.bmp'
        self.ow = ow
        self.setNextDestAndLight()

        
        #randomize speeds
        greenSpeed = random.uniform(0.2, 1.2)
        yellowSpeed = random.uniform(0.1, 0.5)
        

        #these parameters control the physics of the car
        self.speed = 0.00
        self.mass = 1
        self.massOfAir = 0.15
        self.acceleration = 1
        self.drag = self.mass/(self.mass + self.massOfAir)
        self.maxSpeed = 10

        #This is the vehicle in front of the current one, for collision avoidance
        self.nextVehic = nextVehic

        #road specific assignments
        if self.road.id==1:
            self.length,self.width = int(self.roadSystem.segmentSize/2),int(self.roadSystem.segmentSize)
            self.vehicSpace = self.width
            self.angle = down
            self.poleStop = self.pole.y-(self.roadSystem.roadGap*2)-(2*self.width)
            rawImg = pygame.image.load(self.image)
            self.image = pygame.transform.smoothscale(rawImg,(self.length,self.width))
            self.rect = self.image.get_rect()
            if self.lane.id == 1: self.x,self.y = entrance.x-roadSystem.segmentSize,entrance.y
            if self.lane.id == 2: self.x,self.y = entrance.x+roadSystem.segmentSize,entrance.y
        elif self.road.id==2:
            self.length,self.width = int(self.roadSystem.segmentSize),int(self.roadSystem.segmentSize/2)
            self.vehicSpace = self.length/2
            self.angle = left
            self.poleStop = self.pole.x+(self.roadSystem.roadGap*1.2)+self.length
            rawImg = pygame.transform.rotate(pygame.image.load(self.image),270)
            self.image = pygame.transform.smoothscale(rawImg,(self.length,self.width))
            self.rect = self.image.get_rect()
            if self.lane.id == 1: self.x,self.y = entrance.x,entrance.y-roadSystem.segmentSize
            if self.lane.id == 2: self.x,self.y = entrance.x,entrance.y+roadSystem.segmentSize
        elif self.road.id==3:
            self.length,self.width = int(self.roadSystem.segmentSize/2),int(self.roadSystem.segmentSize)
            self.vehicSpace = self.width
            self.angle = up
            self.poleStop = self.pole.y+(self.roadSystem.roadGap*2)+(self.width)
            rawImg = pygame.transform.flip(pygame.image.load(self.image), False, True)
            self.image = pygame.transform.smoothscale(rawImg,(self.length,self.width))
            self.rect = self.image.get_rect()
            if self.lane.id == 1: self.x,self.y = entrance.x-roadSystem.segmentSize,entrance.y
            if self.lane.id == 2: self.x,self.y = entrance.x+roadSystem.segmentSize,entrance.y
        elif self.road.id==4:
            self.length,self.width = int(self.roadSystem.segmentSize),int(self.roadSystem.segmentSize/2)
            self.vehicSpace = self.length
            self.angle = right
            self.poleStop = self.pole.x-(self.roadSystem.roadGap*1.2)-self.length
            rawImg = pygame.transform.rotate(pygame.image.load(self.image),90)
            self.image = pygame.transform.smoothscale(rawImg,(self.length,self.width))
            self.rect = self.image.get_rect()
            if self.lane.id == 1: self.x,self.y = entrance.x,entrance.y-roadSystem.segmentSize
            if self.lane.id == 2: self.x,self.y = entrance.x,entrance.y+roadSystem.segmentSize
        

        
    #this is the decision making method that asks questions of the other methods
    #and decides to move forward, brake, or remove itself from the vehicle list
    def auto(self):
        #get a new pole and light if we pass the current one
        if self.isPastLine() and len(self.path) >= 2:
            #remove the vehicle from the current poles list because it has passed it
            if isinstance(self.path[0], Intersection) and self in self.pole.vehics: self.pole.vehics.remove(self)
            #remove the pole that we just passed from the path, assigning it to x is a language restraint
            x = self.path.pop(0)
            #set the vehicles next destination
            self.setNextDestAndLight(andPoleStop=True)
        elif self.isPastLine() and len(self.path) <= 1:
            #delete this instance of vehicle so that it will be garbage collected
            self.ow.removeVehic(self)
            
        #remove a vehicle from the nextVehic slot if it has been garbage collected
        if self.nextVehic and not self.nextVehic in self.ow.vehics : self.nextVehic = None
            
        #accelerate if possible
        if self.canGo():
            self.move("forward")
        elif not self.canGo():
            self.move("brake")



    #this method draws the vehicle to the screen
    def draw(self):
        #pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.length))
        self.rect.x, self.rect.y = self.x, self.y
        self.screen.blit(self.image, self.rect)

        

    #this method calculates the next position of the vehicle based on the physics parameters
    def move(self, direction):
        if direction == "forward":
            if self.speed < baseSpeed: self.speed = baseSpeed
            self.acceleration += .1
            #higher value, higher acceleration
            if self.acceleration >= self.massOfAir+1+.05: self.acceleration = self.massOfAir+1+.05
            self.speed = (self.speed * self.drag * self.acceleration)
            if self.speed >= self.maxSpeed: self.speed = self.maxSpeed
            if self.road.id%2 == 1 and self.speed>baseSpeed:
                self.y -= math.cos(self.angle) * self.speed
            elif self.road.id % 2 == 0 and self.speed>baseSpeed:
                self.x -= math.sin(self.angle) * self.speed
                
        elif direction == "brake":
            self.acceleration -= .1
            #higher value, lower braking power
            if self.acceleration <= self.massOfAir+1-.04: self.acceleration = self.massOfAir+1-.04
            self.speed = (self.speed * self.drag * self.acceleration)
            if self.speed <= baseSpeed: self.speed = baseSpeed
            if self.road.id%2 == 1 and self.speed>baseSpeed:
                self.y -= math.cos(self.angle) * self.speed
            elif self.road.id%2 == 0 and self.speed>baseSpeed:
                self.x -= math.sin(self.angle) * self.speed



    #this method determines whether or not the vehicle has passed the stop line
    def isPastLine(self):
        if   self.road.id==1:return self.y > self.poleStop
        elif self.road.id==2:return self.x < self.poleStop
        elif self.road.id==3:return self.y < self.poleStop
        elif self.road.id==4:return self.x > self.poleStop



    #this method determines whether or not a vehicle can accelerate
    #it is only so long because it must contain 4 slightly different
    #versions of basically the same code
    def canGo(self):
        #if the vehicle in front has been garbage collected, we can go
        if not self.nextVehic and isinstance(self.pole, Exit) : return True
        if self.road.id == 1:
            if self.light.state == "stop":
                self.maxSpeed = greenSpeed
                #the car may go if it has already passed the line
                #this avoids collisions in the middle of the intersection
                if self.isPastLine(): return True
                #if there is a vehicle in front of me
                if self.nextVehic:
                    vehicStop = self.nextVehic.y-self.length-self.vehicSpace
                    #check if I have enough room to stop if I need to
                    if (self.poleStop-self.y) >= (eq*self.speed) and (vehicStop-self.y) >= (eq*self.speed):
                        return True
                #if there is no car in front of me
                elif not self.nextVehic:
                    #same check but without the vehicle
                    if (self.poleStop-self.y) >= (eq*self.speed):
                        return True
                return False
            elif self.light.state == "go":
                self.maxSpeed = greenSpeed
                if self.isPastLine(): return True
                if self.nextVehic:
                    vehicStop = self.nextVehic.y-self.length-self.vehicSpace
                    #check if I have enough room to stop if I need to
                    if (vehicStop-self.y) >= (eq*self.speed):
                        return True
                #if there is no car in front of me
                elif not self.nextVehic:
                    return True
                return False
            elif self.light.state == "slow":
                if self.isPastLine(): self.maxSpeed = greenSpeed
                else: self.maxSpeed = yellowSpeed
                if self.isPastLine(): return True
                if self.nextVehic:
                    vehicStop = self.nextVehic.y-self.length-self.vehicSpace
                    #check if I have enough room to stop if I need to
                    if (vehicStop-self.y) >= (eq*self.speed):
                        return True
                #if there is no car in front of me
                elif not self.nextVehic:
                    return True
                return False
            
        elif self.road.id == 2:
            if self.light.state == "stop":
                self.maxSpeed = greenSpeed
                #the car may go if it has already passed the line
                #this avoids collisions in the middle of the intersection
                if self.isPastLine(): return True
                #if there is a vehicle in front of me
                if self.nextVehic:
                    vehicStop = self.nextVehic.x+self.length+self.vehicSpace
                    #check if I have enough room to stop if I need to
                    if (abs(self.poleStop-self.x)) >= (eq*self.speed) and (abs(vehicStop-self.x)) >= (eq*self.speed):
                        return True
                #if there is no car in front of me
                elif not self.nextVehic:
                    #same check but without the vehicle
                    if (abs(self.poleStop-self.x)) >= (eq*self.speed):
                        return True
            elif self.light.state == "go":
                self.maxSpeed = greenSpeed
                if self.isPastLine(): return True
                if self.nextVehic:
                    vehicStop = self.nextVehic.x+self.width+self.vehicSpace
                    #check if I have enough room to stop if I need to
                    if (abs(vehicStop-self.x)) >= (eq*self.speed):
                        return True
                #if there is no car in front of me
                elif not self.nextVehic:
                    return True
            elif self.light.state == "slow":
                if self.isPastLine(): self.maxSpeed = greenSpeed
                else: self.maxSpeed = yellowSpeed
                if self.isPastLine(): return True
                if self.nextVehic:
                    vehicStop = self.nextVehic.x+self.width+self.vehicSpace
                    #check if I have enough room to stop if I need to
                    if (abs(vehicStop-self.x)) >= (eq*self.speed):
                        return True
                #if there is no car in front of me
                elif not self.nextVehic:
                    return True
                
        elif self.road.id == 3:
            if self.light.state == "stop":
                self.maxSpeed = greenSpeed
                #the car may go if it has already passed the line
                #this avoids collisions in the middle of the intersection
                if self.isPastLine(): return True
                #if there is a vehicle in front of me
                if self.nextVehic:
                    vehicStop = self.nextVehic.y+self.length+self.vehicSpace
                    #check if I have enough room to stop if I need to
                    if (abs(self.poleStop-self.y)) >= (eq*self.speed) and (abs(vehicStop-self.y)) >= (eq*self.speed):
                        return True
                #if there is no car in front of me
                elif not self.nextVehic:
                    #same check but without the vehicle
                    if (abs(self.poleStop-self.y)) >= (eq*self.speed):
                        return True
            elif self.light.state == "go":
                self.maxSpeed = greenSpeed
                if self.isPastLine(): return True
                if self.nextVehic:
                    vehicStop = self.nextVehic.y+self.length+self.vehicSpace
                    #check if I have enough room to stop if I need to
                    if (abs(vehicStop-self.y)) >= (eq*self.speed):
                        return True
                #if there is no car in front of me
                elif not self.nextVehic:
                    return True
            elif self.light.state == "slow":
                if self.isPastLine(): self.maxSpeed = greenSpeed
                else: self.maxSpeed = yellowSpeed
                if self.isPastLine(): return True
                if self.nextVehic:
                    vehicStop = self.nextVehic.y+self.length+self.vehicSpace
                    #check if I have enough room to stop if I need to
                    if (abs(vehicStop-self.y)) >= (eq*self.speed):
                        return True
                #if there is no car in front of me
                elif not self.nextVehic:
                    return True
                
        elif self.road.id == 4:
            if self.light.state == "stop":
                self.maxSpeed = greenSpeed
                #the car may go if it has already passed the line
                #this avoids collisions in the middle of the intersection
                if self.isPastLine(): return True
                #if there is a vehicle in front of me
                if self.nextVehic:
                    vehicStop = self.nextVehic.x-self.width-self.vehicSpace
                    #check if I have enough room to stop if I need to
                    if (abs(self.poleStop-self.x)) >= (eq*self.speed) and (abs(vehicStop-self.x)) >= (eq*self.speed):
                        return True
                #if there is no car in front of me
                elif not self.nextVehic:
                    #same check but without the vehicle
                    if (abs(self.poleStop-self.x)) >= (eq*self.speed):
                        return True
            elif self.light.state == "go":
                self.maxSpeed = greenSpeed
                if self.isPastLine(): return True
                if self.nextVehic:
                    vehicStop = self.nextVehic.x-self.width-self.vehicSpace
                    #check if I have enough room to stop if I need to
                    if (abs(vehicStop-self.x)) >= (eq*self.speed):
                        return True
                #if there is no car in front of me
                elif not self.nextVehic:
                    return True
            elif self.light.state == "slow":
                if self.isPastLine(): self.maxSpeed = greenSpeed
                else: self.maxSpeed = yellowSpeed
                if self.isPastLine(): return True
                if self.nextVehic:
                    vehicStop = self.nextVehic.x-self.width-self.vehicSpace
                    #check if I have enough room to stop if I need to
                    if (abs(vehicStop-self.x)) >= (eq*self.speed):
                        return True
                #if there is no car in front of me
                elif not self.nextVehic:
                    return True
        return False

    def setNextDestAndLight(self, andPoleStop=False):
        for elem in self.path:
            if isinstance(elem, Intersection):
                #set new pole and light
                self.pole = elem.poles[self.road.id-1]
                self.light = self.pole.lights[self.lane.id-1]
                #add the vehicle to the new poles list
                if not self in self.pole.vehics: self.pole.vehics.append(self)
                if andPoleStop:
                    if self.road.id==1 : self.poleStop = self.pole.y-(self.roadSystem.roadGap*2)-(2*self.width)
                    elif self.road.id==2 : self.poleStop = self.pole.x+(self.roadSystem.roadGap*1.2)+self.length
                    elif self.road.id==3 : self.poleStop = self.pole.y+(self.roadSystem.roadGap*2)+(self.width)
                    elif self.road.id==4 : self.poleStop = self.pole.x-(self.roadSystem.roadGap*1.2)-self.length
                break
                
            elif isinstance(elem, Exit):
                self.pole = elem
                if andPoleStop:
                    if self.road.id==1 : self.poleStop = self.pole.y
                    elif self.road.id==2 : self.poleStop = self.pole.x
                    elif self.road.id==3 : self.poleStop = self.pole.y
                    elif self.road.id==4 : self.poleStop = self.pole.x
                break
            
            

    def turn(self, id):
        #road specific assignments
        if id==1:
            self.length,self.width = int(self.roadSystem.segmentSize/2),int(self.roadSystem.segmentSize)
            self.vehicSpace = self.width
            self.angle = down
            self.setNextDestAndLight()
            rawImg = pygame.image.load(self.image)
            self.image = pygame.transform.smoothscale(rawImg,(self.length,self.width))
            self.rect = self.image.get_rect()
        elif id==2:
            self.length,self.width = int(self.roadSystem.segmentSize),int(self.roadSystem.segmentSize/2)
            self.vehicSpace = self.length/2
            self.angle = left
            self.setNextDestAndLight()
            rawImg = pygame.transform.rotate(pygame.image.load(self.image),270)
            self.image = pygame.transform.smoothscale(rawImg,(self.length,self.width))
            self.rect = self.image.get_rect()
        elif id==3:
            self.length,self.width = int(self.roadSystem.segmentSize/2),int(self.roadSystem.segmentSize)
            self.vehicSpace = self.width
            self.angle = up
            self.setNextDestAndLight()
            rawImg = pygame.transform.flip(pygame.image.load(self.image), False, True)
            self.image = pygame.transform.smoothscale(rawImg,(self.length,self.width))
            self.rect = self.image.get_rect()
        elif id==4:
            self.length,self.width = int(self.roadSystem.segmentSize),int(self.roadSystem.segmentSize/2)
            self.vehicSpace = self.length
            self.angle = right
            self.setNextDestAndLight()
            rawImg = pygame.transform.rotate(pygame.image.load(self.image),90)
            self.image = pygame.transform.smoothscale(rawImg,(self.length,self.width))
            self.rect = self.image.get_rect()


