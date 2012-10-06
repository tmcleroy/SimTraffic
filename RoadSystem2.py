import pygame
from Config import *
from RoadFeatures import *

class RoadSystem2:

    roadGap = 0

    def __init__(self, fname, screen='', width=1280, height=720, segmentSize=5):
        self.screen = screen
        self.width, self.height = width, height
        self.features = {}
        self.f = open(fname, 'r')
        self.fstr = self.f.read()
        
        self.name = self.getStringBetween(self.fstr,':','\n')
        
        self.roadLen = (self.getStringBetween(self.fstr,'START:\n','\nEND:\n').split('\n')[0]).count('<')
        self.roadStrings = self.getStringBetween(self.fstr,'START:\n','\nEND:\n').split('\n')
        self.segmentSize = (width/self.roadLen)
        RoadSystem2.roadGap = self.segmentSize*3

        self.setAnchors()
        self.setRoads()
        self.setEntrances()
        self.setExits()
        self.setLightPoles()
        self.setSideRoads()
        
        
    def setRoads(self):
        roadStringList = self.getStringBetween(self.fstr,'START:\n','\nEND:\n').split('\n')
        id = 0
        for i, rdstr in enumerate(self.roadStrings):
            if not '-' in rdstr:
                if 'v' in rdstr: id = 1
                elif '<' in rdstr: id = 2
                elif '^' in rdstr: id = 3
                elif '>'  in rdstr: id = 4
                self.features["R"+str(i+1)] = Road("Road"+str(i+1), id, self.screen, [(0,((self.height/2)+(i*RoadSystem2.roadGap))) , ((0+self.roadLen)*self.segmentSize, ((self.height/2)+(i*RoadSystem2.roadGap)))], Lane(1), Lane(2))


    def setSideRoads(self):
        numRoads = 0
        sideRoadsStr = self.getStringBetween(self.fstr,'[SIDEROADS]\n','\n[/SIDEROADS]')
        for line in sideRoadsStr.split('\n'):
            if '<sideRoad' in line: numRoads+=1
        for num in range(numRoads):
            sr = self.getStringBetween(sideRoadsStr,('<sideRoad'+str(num+1)+'>\n'),('\n</sideRoad'+str(num+1)+'>'))
            loc = self.getStringBetween(sr,'<loc>','</loc>')
            sr = sr.split('</loc>\n')[-1].split('\n')
            xCoord, yCoord = self.features[loc].x, self.features[loc].y
            id = roadLen = 0
            splt = '@'
            for i, rdstr in enumerate(sr):
                if '<' in rdstr:
                    id = 3
                    roadLen = rdstr.count('<')
                    splt = '<'
                elif '>'  in rdstr:
                    id = 1
                    roadLen = rdstr.count('>')
                    splt = '>'
                for j, elem in enumerate(rdstr.split(splt)):
                    #********************************************************
                    if 'En' in elem:
                        self.features[elem].x, self.features[elem].y = ((xCoord+(i*RoadSystem2.roadGap)-(RoadSystem2.roadGap/2)-(self.features[elem].width/2)), ((self.height/2)-((roadLen/2)*self.segmentSize)+(j*self.segmentSize)+self.roadGap))
                        self.features[elem].width, self.features[elem].height = self.segmentSize, self.segmentSize
                    elif 'Ex' in elem:
                        self.features[elem].x, self.features[elem].y = ((xCoord+(i*RoadSystem2.roadGap)-(RoadSystem2.roadGap/2)-(self.features[elem].width/2)), ((self.height/2)-((roadLen/2)*self.segmentSize)+(j*self.segmentSize)+self.roadGap))
                        self.features[elem].width, self.features[elem].height = self.segmentSize, self.segmentSize
                self.features["SR"+str(num+1)+str(i)] = Road("SideRoad"+str(num+1), id, self.screen, [(xCoord+(i*RoadSystem2.roadGap)-(RoadSystem2.roadGap/2),yCoord-((roadLen/2)*self.segmentSize)) , (xCoord+(i*RoadSystem2.roadGap)-(RoadSystem2.roadGap/2), yCoord+((roadLen/2))*self.segmentSize)], Lane(1), Lane(2))


    def setAnchors(self):
        argList = self.getStringBetween(self.fstr,'[ANCHORS]\n','\n[/ANCHORS]').split('\n')
        for argstr in argList:
            args = argstr.split(',')
            self.features[args[0]] = Anchor("Anchor"+args[0], self.screen)
        for i, rdstr in enumerate(self.roadStrings):
            splt = '-' if '-' in rdstr else '@'
            for j, elem in enumerate(rdstr.split(splt)):
                if 'An' in elem:
                        self.features[elem].x, self.features[elem].y = ((j*self.segmentSize)+self.segmentSize), ((self.height/2)+(i*RoadSystem2.roadGap))
        

    def setEntrances(self):
        argList = self.getStringBetween(self.fstr,'[ENTRANCES]\n','\n[/ENTRANCES]').split('\n')
        for argstr in argList:
            args = argstr.split(',')
            self.features[args[0]] = Entrance(args[0], self.screen)
        for i, rdstr in enumerate(self.roadStrings):
            splt = '>' if '>' in rdstr else '<'
            for j, elem in enumerate(rdstr.split(splt)):
                if 'En' in elem:
                        self.features[elem].x, self.features[elem].y = ((j*self.segmentSize)+self.segmentSize), ((self.height/2)+(i*RoadSystem2.roadGap))
                        self.features[elem].width, self.features[elem].height = self.segmentSize, self.segmentSize
                        self.setPoleStack(elem, rdstr)

                
    def setPoleStack(self, entr, str):
        #print (str,'\n\n\n')
        if len(self.features[entr].poleStack) == 0:
            splt = '>' if '>' in str else '<'
            for e in str.split(splt):
                if 'Po' in e: self.features[entr].poleStack.append(e)
    
        
    

    def setExits(self):
        argList = self.getStringBetween(self.fstr,'[EXITS]\n','\n[/EXITS]').split('\n')
        for argstr in argList:
            args = argstr.split(',')
            self.features[args[0]] = Exit(args[0], self.screen)
        for i, rdstr in enumerate(self.roadStrings):
            splt = '>' if '>' in rdstr else '<'
            for j, elem in enumerate(rdstr.split(splt)):
                if 'Ex' in elem:
                        self.features[elem].x, self.features[elem].y = ((j*self.segmentSize)+self.segmentSize), ((self.height/2)+(i*RoadSystem2.roadGap))
                        self.features[elem].width, self.features[elem].height = self.segmentSize, self.segmentSize


    def setLightPoles(self):
        argList = self.getStringBetween(self.fstr,'[LIGHTPOLES]\n','\n[/LIGHTPOLES]').split('\n')
        for argstr in argList:
            args = argstr.split(',')
            self.features[args[0]] = LightPole(args[0], args[1], self.screen, Light('l1', 'stop'), Light('l2', 'stop'))
        for i, rdstr in enumerate(self.roadStrings):
            splt = '>' if '>' in rdstr else '<'
            for j, elem in enumerate(rdstr.split(splt)):
                if 'Po' in elem:
                    if splt == '<':
                        self.features[elem].x, self.features[elem].y = ((j*self.segmentSize)+self.segmentSize*2), ((self.height/2)+(i*RoadSystem2.roadGap))
                        self.features[elem].width, self.features[elem].height = self.segmentSize, self.segmentSize*2
                    elif splt == '>':
                        self.features[elem].x, self.features[elem].y = ((j*self.segmentSize)+(RoadSystem2.roadGap*2)+self.segmentSize), ((self.height/2)+(i*RoadSystem2.roadGap))
                        self.features[elem].width, self.features[elem].height = self.segmentSize, self.segmentSize*2


    def draw(self):
        for feature in self.features.values():
            if feature.isDrawable: feature.draw()
      


    def getStringBetween(self,string, start='', end=''):
        return string.split(start)[1].split(end)[0]
        

r = RoadSystem2('r2.txt')
print ("RoadSystem r has been created")

