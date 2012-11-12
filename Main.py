import sys, pygame, threading, random
from Config import *
from Overwatch import *
from RoadSystem import *
from RoadFeatures import * 
from Vehicle import *


#initialize pygame, the graphics library used for visually representing the simulation
pygame.init()

#initialize the screen surface onto which everything will be drawn
screen = pygame.display.set_mode(size)
vehics=[]
ow = Overwatch(RoadSystem(roadSystemFileName, screen, width, height), vehics)
rs = ow.rs
defaultSpawnInfo = {'EnA1':['ExA1'],
                    'EnB1':['ExB1'],
                    'EnC1':['ExC1'],
                    'EnC2':['ExC2'],
                    'EnD1':['ExD1'],
                    'EnD2':['ExD2'],
                    'EnE1':['ExE1'],
                    'EnE2':['ExE2']}


def autoVehicSpawn(frameCount):
    for key in rs.spawns.mods:
        if frameCount % rs.spawns.mods[key] == 0:
            rand = random.randint(1,100)
            if rand%2==0:
                spawnVehic(key, 1, defaultSpawnInfo[key][0])
            elif rand%2==1:
                spawnVehic(key, 2, defaultSpawnInfo[key][0])
    

#returns the last vehicle spawned on the given road
def getPrevVehic(road):
    if len(ow.vehics) == 0 : return None
    limit = -1*len(ow.vehics)
    i = -1
    while  i >= limit:
        if ow.vehics[i].road == road : return ow.vehics[i]
        i -= 1
    return None
        

#spawns a vehicle and adds it to the car list
def spawnVehic(entrance, lane, exit):
    entrance = ow.rs.features[entrance]
    road = entrance.road
    exit = ow.rs.features[exit]
    frontVehic = getPrevVehic(road)
    
    v = Vehicle(screen, ow.rs, entrance, road, road.lanes[lane-1], frontVehic, exit)
    
    road.lanes[lane-1].vehicles.append(v)    
    ow.vehics.append(v)




#initialize the clock instance which allows framerate regulation
Clock = pygame.time.Clock()

#a font instance must be initialized so we can render text within the game loop
Font = pygame.font.Font(None, 36)

frameCount = 0
secondsPassed = 0

#t = threading.Thread(target=ow.lc.auto)
ow.lc.start()

#GAME LOOP. This will run every frame (120 times per second) until the program is closed
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit();

    #the screen must be erased every frame, the additional
    #elements are then redrawn over the white surface after their
    #positions are recalculated. This creates the illusion of motion
    screen.fill(white)

    #limit framerate
    ms = Clock.tick(framerate)

    #increment frame count and track seconds passed
    frameCount += 1
    if frameCount % framerate == 0 : secondsPassed += 1
    #reset frameCount each minute
    if frameCount >= 7200 : frameCount = 0

    #generates the info text labels. These must be in multiple labels because
    #the font renderer cannot handle newline characters
    fpsText = ("FPS: "+str(int(Clock.get_fps())))
    fpsLabel = Font.render(fpsText, 1, black)
    secondsText = ("Seconds Passed: "+str(secondsPassed))
    secondsLabel = Font.render(secondsText, 1, black)

    ow.rs.draw()

    #auto spawn vehicles
    autoVehicSpawn(frameCount)

    
    for vehic in ow.vehics:
        vehic.auto()
        vehic.draw()

    #automatically control lights
    
    """
    if not t.is_alive():
        print("not alive")
        t = threading.Thread(target=ow.lc.auto)
        t.start()
    """
    
    #ow.lc.auto()
    
    
    #handle keyboard input
    if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                if frameCount%10 == 0:
                    spawnVehic(entrance='EnC1', lane=1, exit='ExC1')
            elif event.key == pygame.K_2:
                if frameCount%10 == 0:
                    spawnVehic(entrance='EnB1', lane=1, exit='ExB1')
            elif event.key == pygame.K_3:
                if frameCount%10 == 0:
                    spawnVehic(entrance='EnD2', lane=1, exit='ExD2')
            elif event.key == pygame.K_4:
                if frameCount%10 == 0:
                    spawnVehic(entrance='EnA1', lane=1, exit='ExA1')
            elif event.key == pygame.K_0:
                ow.lc.setAll([0,1,2,3], "go")
            elif event.key == pygame.K_9:
                ow.lc.setAll([0,1,2,3], "stop")
            elif event.key == pygame.K_8:
                ow.lc.transAllToState([0,1,2,3], "go")
            elif event.key == pygame.K_7:
                ow.lc.transAllToState([0,1,2,3], "stop")
            elif event.key == pygame.K_l:
                for intersection in ow.lc.intersections:
                    for pole in intersection.poles:
                        if len(pole.vehics) > 0:
                            print(pole," has: ",pole.vehics)
    
    #display the FPS (Frames Per Second) and info text
    screen.blit(fpsLabel, (0,0))
    screen.blit(secondsLabel, (0, 35))
    
    #update the screen
    pygame.display.flip()

