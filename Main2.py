import sys, pygame
from RoadSystem2 import *
from RoadFeatures import *
from Config import *
from Vehicle2 import *


#initialize pygame, the game library used for visually
#representing the simulation
pygame.init()

#initialize the screen surface onto which everything
#will be drawn
screen = pygame.display.set_mode(size)
vehics=[]
roadSystemFname = 'roadSystems/r2short.txt'
rs = RoadSystem2(roadSystemFname, screen, width, height)


#returns the last vehicle spawned on the given road
def getPrevVehic(road):
    if len(vehics) == 0 : return None
    limit = -1*len(vehics)
    i = -1
    while  i >= limit:
        if vehics[i].road.id == road.id: return vehics[i]
        i -= 1
    return None
        

#spawns a vehicle and adds it to the car list
def spawnVehic(entrance, road, lane, exit):
    entrance = rs.features[entrance]
    road = rs.features[road]
    exit = rs.features[exit]
    frontVehic = getPrevVehic(road)
    
    v = Vehicle2(screen, rs, entrance, road, road.lanes[lane-1], frontVehic, exit)
    
    road.lanes[lane-1].vehicles.append(v)    
    vehics.append(v)




#initialize the clock instance which allows framerate regulation
Clock = pygame.time.Clock()

#a font instance must be initialized so we can render
#text within the game loop
Font = pygame.font.Font(None, 36)

frameCount = 0
secondsPassed = 0



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
    if frameCount % framerate == 0: secondsPassed += 1

    #generates the info text labels. These must be
    #in multiple labels because the font renderer
    #cannot handle newline characters
    fpsText = ("FPS: "+str(int(Clock.get_fps())))
    fpsLabel = Font.render(fpsText, 1, black)
    secondsText = ("Seconds Passed: "+str(secondsPassed))
    secondsLabel = Font.render(secondsText, 1, black)

    rs.draw()

    
    for vehic in vehics:
        vehic.auto()
        vehic.draw()
    

    #pprint (cars)
    
    #handle keyboard input
    if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                if frameCount%10 == 0:
                    spawnVehic(entrance='EnC1', road='SR10', lane=1, exit='ExC1')
            elif event.key == pygame.K_2:
                if frameCount%10 == 0:
                    spawnVehic(entrance='EnB1', road='R1', lane=1, exit='ExB1')
            elif event.key == pygame.K_3:
                if frameCount%10 == 0:
                    spawnVehic(entrance='EnD2', road='SR21', lane=1, exit='ExD2')
            elif event.key == pygame.K_4:
                if frameCount%10 == 0:
                    spawnVehic(entrance='EnA1', road='R3', lane=1, exit='ExA1')
            elif event.key == pygame.K_0:
                rs.setAllLights("go")
            elif event.key == pygame.K_9:
                rs.setAllLights("stop")

    
    
    #display the FPS (Frames Per Second) and info text
    screen.blit(fpsLabel, (0,0))
    screen.blit(secondsLabel, (0, 35))
    
    #update the screen
    pygame.display.flip()

