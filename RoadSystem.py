import pygame
from Config import *
from RoadFeatures import *

class RoadSystem:

    roadGap = 0

    def __init__(self, fname, screen='', width=1280, height=720, segmentSize=5):
        self.screen = screen
        self.width, self.height = width, height
        self.features = {}
        self.features['None'] = None
        self.spawns = SpawnFrequencyIndex()
        self.navGraph = {}
        self.f = open(fname, 'r')
        self.fstr = self.f.read()
        self.f.close()
        
        self.name = self.getStringBetween(self.fstr,':','\n')
        
        self.roadLen = (self.getStringBetween(self.fstr,'START:\n','\nEND:\n').split('\n')[0]).count('<')
        self.roadStrings = self.getStringBetween(self.fstr,'START:\n','\nEND:\n').split('\n')
        #set this to a constant for unscaled graphics
        self.segmentSize = (width/self.roadLen)
        RoadSystem.roadGap = self.segmentSize*3

        #must be in this order
        self.setAnchors()
        self.setEntrances()
        self.setRoads()
        self.setExits()
        self.setSpawnFrequencies()
        self.setLightPoles()
        self.setSideRoads()
        self.setIntersections()
        self.setNavGraph()



    def setEntrances(self):
        argList = self.getStringBetween(self.fstr,'[ENTRANCES]\n','\n[/ENTRANCES]').split('\n')
        for argstr in argList:
            args = argstr.split(',')
            self.features[args[0]] = Entrance(args[0], self.screen)
        for i, rdstr in enumerate(self.roadStrings):
            splt = '>' if '>' in rdstr else '<'
            for j, elem in enumerate(rdstr.split(splt)):
                if 'En' in elem:
                        self.features[elem].x, self.features[elem].y = ((j*self.segmentSize)+self.segmentSize), ((self.height/2)+(i*RoadSystem.roadGap))
                        self.features[elem].width, self.features[elem].height = self.segmentSize, self.segmentSize
                        self.features[elem].id = 2 if splt == '<' else 4


        
        
    def setRoads(self):
        #roadStringList = self.getStringBetween(self.fstr,'START:\n','\nEND:\n').split('\n')
        id = 0
        for i, rdstr in enumerate(self.roadStrings):
            if not '-' in rdstr:
                entrance = self.getEntranceInString(rdstr)
                if '<' in rdstr: id = 2
                elif '>'  in rdstr: id = 4
                self.features["R"+str(i+1)] = Road("Road"+str(i+1), id, self.screen, [(0,((self.height/2)+(i*RoadSystem.roadGap))) , ((0+self.roadLen)*self.segmentSize, ((self.height/2)+(i*RoadSystem.roadGap)))], Lane(1), Lane(2))
                self.features[entrance].road = self.features["R"+str(i+1)]



    def getEntranceInString(self, string):
        splt = '>' if '>' in string else '<'
        for j, elem in enumerate(string.split(splt)):
            if 'En' in elem : return elem



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
                #add the sideroad to the master road string list
                self.roadStrings.append(rdstr)
                
                entrance = self.getEntranceInString(rdstr)

                if '<' in rdstr:
                    id = 3
                    roadLen = rdstr.count('<')
                    splt = '<'
                elif '>'  in rdstr:
                    id = 1
                    roadLen = rdstr.count('>')
                    splt = '>'
                for j, elem in enumerate(rdstr.split(splt)):
                    if 'En' in elem:
                        self.features[elem].x, self.features[elem].y = ((xCoord+(i*RoadSystem.roadGap)-(RoadSystem.roadGap/2)), ((self.height/2)-((roadLen/2)*self.segmentSize)+(j*self.segmentSize)+self.roadGap))
                        self.features[elem].width, self.features[elem].height = self.segmentSize, self.segmentSize
                        self.features[elem].id = id
                    elif 'Ex' in elem:
                        self.features[elem].x, self.features[elem].y = ((xCoord+(i*RoadSystem.roadGap)-(RoadSystem.roadGap/2)), ((self.height/2)-((roadLen/2)*self.segmentSize)+(j*self.segmentSize)+self.roadGap))
                        self.features[elem].width, self.features[elem].height = self.segmentSize, self.segmentSize
                        self.features[elem].id = id
                    #********************************************************
                    elif 'Po' in elem:
                        if splt == '<':
                            self.features[elem].x, self.features[elem].y = ((xCoord+(self.segmentSize/2)), ((self.height/2)-((i*RoadSystem.roadGap)*2)+self.roadGap*2)-self.segmentSize)
                            self.features[elem].width, self.features[elem].height = self.segmentSize*2, self.segmentSize
                        elif splt == '>':
                            self.features[elem].x, self.features[elem].y = ((xCoord+(self.segmentSize/2)-RoadSystem.roadGap), ((self.height/2)-((i*RoadSystem.roadGap)*2)+self.roadGap*2)+self.segmentSize)
                            self.features[elem].width, self.features[elem].height = self.segmentSize*2, self.segmentSize
                self.features["SR"+str(num+1)+str(i)] = Road("SideRoad"+str(num+1)+str(i), id, self.screen, [(xCoord+(i*RoadSystem.roadGap)-(RoadSystem.roadGap/2),yCoord-((roadLen/2)*self.segmentSize)) , (xCoord+(i*RoadSystem.roadGap)-(RoadSystem.roadGap/2), yCoord+((roadLen/2))*self.segmentSize)], Lane(1), Lane(2))
                self.features[entrance].road = self.features["SR"+str(num+1)+str(i)]

    def setAnchors(self):
        argList = self.getStringBetween(self.fstr,'[ANCHORS]\n','\n[/ANCHORS]').split('\n')
        for argstr in argList:
            args = argstr.split(',')
            self.features[args[0]] = Anchor("Anchor"+args[0], self.screen)
        for i, rdstr in enumerate(self.roadStrings):
            splt = '-' if '-' in rdstr else '@'
            for j, elem in enumerate(rdstr.split(splt)):
                if 'An' in elem:
                        self.features[elem].x, self.features[elem].y = ((j*self.segmentSize)+self.segmentSize), ((self.height/2)+(i*RoadSystem.roadGap))
        

 
    def setExits(self):
        argList = self.getStringBetween(self.fstr,'[EXITS]\n','\n[/EXITS]').split('\n')
        for argstr in argList:
            args = argstr.split(',')
            self.features[args[0]] = Exit(args[0], self.screen)
        for i, rdstr in enumerate(self.roadStrings):
            splt = '>' if '>' in rdstr else '<'
            for j, elem in enumerate(rdstr.split(splt)):
                if 'Ex' in elem:
                        self.features[elem].x, self.features[elem].y = ((j*self.segmentSize)+self.segmentSize), ((self.height/2)+(i*RoadSystem.roadGap))
                        self.features[elem].width, self.features[elem].height = self.segmentSize, self.segmentSize
                        self.features[elem].id = 2 if splt == '<' else 4

    def setSpawnFrequencies(self):
        argList = self.getStringBetween(self.fstr,'[SPAWN_FREQUENCIES]\n','\n[/SPAWN_FREQUENCIES]').split('\n')
        for argstr in argList:
            args = argstr.split(',')
            self.spawns.spawnsPerMin[args[0]] = int(args[1])
        self.spawns.setMods()
       

    def setLightPoles(self):
        argList = self.getStringBetween(self.fstr,'[LIGHTPOLES]\n','\n[/LIGHTPOLES]').split('\n')
        for argstr in argList:
            args = argstr.split(',')
            self.features[args[0]] = LightPole(args[0], args[1], self.screen, Light('l1', 'stop'), Light('l2', 'stop'))
        for i, rdstr in enumerate(self.roadStrings):
            splt = '>' if '>' in rdstr else '<'
            for j, elem in enumerate(rdstr.split(splt)):
                if 'Po' in elem:
                    if self.features[elem].id == 2:
                        self.features[elem].x, self.features[elem].y = ((j*self.segmentSize)+(RoadSystem.roadGap*2)+self.segmentSize), ((self.height/2)+(i*RoadSystem.roadGap))
                        self.features[elem].width, self.features[elem].height = self.segmentSize, self.segmentSize*2
                    elif self.features[elem].id == 4:
                        self.features[elem].x, self.features[elem].y = ((j*self.segmentSize)+self.segmentSize*2), ((self.height/2)+(i*RoadSystem.roadGap))
                        self.features[elem].width, self.features[elem].height = self.segmentSize, self.segmentSize*2

    def setIntersections(self):
        argList = self.getStringBetween(self.fstr,'[INTERSECTIONS]\n','\n[/INTERSECTIONS]').split('\n')
        for argstr in argList:
            args = argstr.split(',')
            self.features[args[0]] = Intersection(args[0], self.features[args[1]], [self.features[args[2]],self.features[args[3]],self.features[args[4]],self.features[args[5]]])


    #constructs the navigation graph that a car will use to find its way from
    #its entrance to its exit. It is a directed graph represented by a dictionary
    def setNavGraph(self):
        #initialize with entrances and intersections
        intersectionList = [] #this is needed for the getParent method of LightPole
        for i in self.features:
            if 'En' in i or 'In' in i:
                self.navGraph[self.features[i]] = []
            if 'In' in i: intersectionList.append(self.features[i])
        #populate the values for the entrance keys
        for rdstr in self.roadStrings:
            splt = '>' if '>' in rdstr else '<'
            charList = rdstr.split(splt)
            if splt == '<': charList.reverse()
            key, pole = None, None
            for elem in charList:
                if 'En' in elem: key = elem
                if 'Po' in elem:
                    pole = self.features[elem]
                    break
            #we now have the pole connected to the entrance, we need the intersection
            if key: self.navGraph[self.features[key]].append(pole.getParent(intersectionList))
        #populate the values for the intersection keys
        poleDest = {} #this is needed to map a pole to its next destination
        for feature in self.features:
            if 'Po' in feature: poleDest[feature] = None
        for po in poleDest:
            for rdstr in self.roadStrings:
                if po in rdstr:
                    splt = '>' if '>' in rdstr else '<'
                    charList = rdstr.split(splt)
                    if splt == '<' : charList.reverse()
                    dest = None
                    brkNext = False
                    for elem in charList:
                        if brkNext and ('Po' in elem or 'Ex' in elem):
                            dest = elem
                            break
                        if elem == po: brkNext = True
            poleDest[po] = dest
        for elem in self.navGraph:
            if 'In' in elem.name:
                for i in range(4):
                    dest = self.features[poleDest[self.features[elem.name].poles[i].name]]
                    if isinstance(dest, LightPole) : dest = dest.getParent(intersectionList)
                    self.navGraph[elem].append(dest)
                

    
    def draw(self):
        for feature in self.features.values():
            if feature and feature.isDrawable: feature.draw()


    #returns the shortest path from an entrance to an exit or intersection
    def getPath(self, start, end, graph=None, path=[]):
        graph = self.navGraph
        path = path + [start]
        if start == end:
            return path
        if not start in graph:
            return None
        shortest = None
        for node in graph[start]:
            if node not in path:
                newpath = self.getPath(node, end, graph, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest
      


    def getStringBetween(self,string, start='', end=''):
        return string.split(start)[1].split(end)[0]
        
"""
r = RoadSystem('roadSystems/r2.txt')
print ("RoadSystem r has been created")
"""
