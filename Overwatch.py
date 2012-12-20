from Config import *
from LightController import *
from Analytics import *
from Learning import *

#this class acts as a convenient container for several other classes needed by Main
class Overwatch:

    def __init__(self, rs, vehics):
        self.rs = rs
        self.vehics = vehics
        self.rects = []
        self.lc = LightController(self)
        self.analytics = Analytics()
        self.learning = Learning(self)

        
    #removes the given vehic from the vehicles list so it will be garbage collected
    def removeVehic(self, vehic):
        self.vehics.remove(vehic)
        self.analytics.vehicPassed(vehic)


    #automatically spawns vehicls at the rate defined in the road system data file
    def autoVehicSpawn(self, frameCount, screen):
        defaultSpawnInfo = self.rs.entranceExitDefaults
        for key in self.rs.spawns.mods:
            if frameCount % self.rs.spawns.mods[key] == 0:
                rand = random.randint(1,100)
                if rand%2==0:
                    self.spawnVehic(key, 1, defaultSpawnInfo[key][0], screen)
                elif rand%2==1:
                    self.spawnVehic(key, 2, defaultSpawnInfo[key][0], screen)

    #returns the last vehicle spawned on the given road in the given lane
    def getPrevVehic(self, road, lane):
        if len(self.vehics) == 0 : return None
        limit = -1*len(self.vehics)
        i = -1
        while  i >= limit:
            if self.vehics[i].road == road and self.vehics[i].lane.id == lane : return self.vehics[i]
            i -= 1
        return None

    #spawns a vehicle at the given entrance, in the given lane, headed for the given exit, and adds it to the vehicle list
    def spawnVehic(self, entrance, lane, exit, screen):
        entrance = self.rs.features[entrance]
        road = entrance.road
        exit = self.rs.features[exit]
        frontVehic = self.getPrevVehic(road, lane)
        v = Vehicle(screen, self.rs, entrance, road, road.lanes[lane-1], frontVehic, exit, self)
        road.lanes[lane-1].vehicles.append(v)    
        self.vehics.append(v)
