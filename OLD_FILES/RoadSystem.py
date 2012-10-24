import pygame
from Config import *
from RoadFeatures import *



class RoadSystem:

    roadGap = 30

    def __init__(self, fname, screen='', width=1280, height=720, segmentSize=5):
        self.screen = screen
        self.width, self.height = width, height
        self.f = open(fname, 'r')
        self.fstr = self.f.read()
        
        self.name = self.getStringBetween(':','\n')
        
        self.roadLen = (self.getStringBetween('START:\n','\nEND:\n').split('\n')[0]).count('>')
        self.roadStrings = self.getStringBetween('START:\n','\nEND:\n').split('\n')
        self.segmentSize = (width/self.roadLen)

        self.features = {}
        self.setRoads()
        self.setEntrances()
        self.setExits()
        self.setLightPoles()
        """
        self.roads = self.setRoads()
        self.entrances = self.setEntrances()
        self.exits = self.getExits()
        self.intersections = self.getIntersections()
        """

        """
        self.features = dict(list(self.roads) +
                             list(self.entrances.items()) +
                             list(self.exits.items()) +
                             list(self.intersections.items()))
        """
        
    def setRoads(self):
        roadStringList = self.getStringBetween('START:\n','\nEND:\n').split('\n')
        id = 0
        for i, rdstr in enumerate(self.roadStrings):
            if 'v' in rdstr: id = 1
            elif '<' in rdstr: id = 2
            elif '^' in rdstr: id = 3
            elif '>'  in rdstr: id = 4
            self.features["R"+str(i+1)] = Road("Road"+str(i+1), id, self.screen, [(0,((self.height/2)+(i*RoadSystem.roadGap))) , ((0+self.roadLen)*self.segmentSize, ((self.height/2)+(i*RoadSystem.roadGap)))], Lane(1), Lane(2))
    

    def setEntrances(self):
        argList = self.getStringBetween('[ENTRANCES]\n','\n[/ENTRANCES]').split('\n')
        for argstr in argList:
            args = argstr.split(',')
            self.features[args[0]] = Entrance(args[0], self.screen)
        for i, rdstr in enumerate(self.roadStrings):
            splt = '>' if '>' in rdstr else '<'
            for j, elem in enumerate(rdstr.split(splt)):
                if 'E' in elem:
                        self.features[elem].x, self.features[elem].y = ((j*self.segmentSize)+self.segmentSize), ((self.height/2)+(i*RoadSystem.roadGap))
                        self.features[elem].width, self.features[elem].height = self.segmentSize, self.segmentSize
                        self.setPoleStack(elem, rdstr)
                        
    def setPoleStack(self, entr, str):
        print (str,'\n\n\n')
        if len(self.features[entr].poleStack) == 0:
            splt = '>' if '>' in str else '<'
            for e in str.split(splt):
                if 'P' in e: self.features[entr].poleStack.append(e)
        
    

    def setExits(self):
        argList = self.getStringBetween('[EXITS]\n','\n[/EXITS]').split('\n')
        for argstr in argList:
            args = argstr.split(',')
            self.features[args[0]] = Exit(args[0], self.screen)
        for i, rdstr in enumerate(self.roadStrings):
            splt = '>' if '>' in rdstr else '<'
            for j, elem in enumerate(rdstr.split(splt)):
                if 'X' in elem:
                        self.features[elem].x, self.features[elem].y = ((j*self.segmentSize)+self.segmentSize), ((self.height/2)+(i*RoadSystem.roadGap))
                        self.features[elem].width, self.features[elem].height = self.segmentSize, self.segmentSize


    def setLightPoles(self):
        argList = self.getStringBetween('[LIGHTPOLES]\n','\n[/LIGHTPOLES]').split('\n')
        for argstr in argList:
            args = argstr.split(',')
            self.features[args[0]] = LightPole(args[0], args[1], self.screen, Light('l1', 'stop'), Light('l2', 'stop'))
        for i, rdstr in enumerate(self.roadStrings):
            splt = '>' if '>' in rdstr else '<'
            for j, elem in enumerate(rdstr.split(splt)):
                if 'P' in elem:
                        self.features[elem].x, self.features[elem].y = ((j*self.segmentSize)+self.segmentSize), ((self.height/2)+(i*RoadSystem.roadGap))
                        self.features[elem].width, self.features[elem].height = self.segmentSize, self.segmentSize*2



    """
    def setPositions(self):
        for i in range(len(self.roads)):
            graphics['lines'].append([(0,((self.height/2)+(i*10))) , (0+len(self.roads[i])*self.segmentSize,((self.height/2)+(i*10)))])
            
            splt = '>' if '>' in self.roads[i] else '<'
            for i2, element in enumerate(self.roads[i].split(splt)):
                if not element == '':
                    graphics['rects'].append((i2*self.segmentSize, ((self.height/2)+(i*10)), 5, 5))
                    self.features[element].x, self.features[element].y = (i2*self.segmentSize), ((self.height/2)+(i*10))

    def getGraphics(self):
        graphics = {'lines':[],'rects':[]}
        for i in range(len(self.roads)):
            graphics['lines'].append([(0,((self.height/2)+(i*10))) , (0+len(self.roads[i])*self.segmentSize,((self.height/2)+(i*10)))])
            splt = '>' if '>' in self.roads[i] else '<'
            for i2, element in enumerate(self.roads[i].split(splt)):
                if not element == '':
                    graphics['rects'].append((i2*self.segmentSize, ((self.height/2)+(i*10)), 5, 5))
                    self.features[element].x, self.features[element].y = (i2*self.segmentSize), ((self.height/2)+(i*10))
        return graphics
    """
    def draw(self):
        """for road in self.roads.values():
            pygame.draw.lines(self.screen,black,False,road.line)"""
        for feature in self.features.values():
            feature.draw()
        """
        for line in self.graphics['lines']:
            pygame.draw.lines(self.screen,black,False,line)
        for rect in self.graphics['rects']:
            pygame.draw.rect(self.screen, red, rect, 0)
        """
        


    def getStringBetween(self, start='', end=''):
        return self.fstr.split(start)[1].split(end)[0]
        

r = RoadSystem('r1.txt')
print ("RoadSystem r has been created")

