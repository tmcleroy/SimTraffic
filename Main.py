import sys, pygame, threading, random
from pprint import pprint
from Config import *
from Overwatch import *
from RoadSystem import *
from RoadFeatures import * 
from Vehicle import *

#initialize pygame, the graphics library used for visually representing the simulation
pygame.init()
#initialize the screen surface onto which everything will be drawn
screen = pygame.display.set_mode(SIZE)
#overwatch aggregates many of the essential system components
ow = Overwatch(RoadSystem(ROAD_SYSTEM_FILE_NAME, screen, WIDTH, HEIGHT), [])


#initialize the clock and timing variables
Clock = pygame.time.Clock()
frameCount = 0
secondsPassed = 0

#font for rendering text
Font = pygame.font.Font(None, 36)

#set all lights to green for baseline stat gathering
ow.lc.setAll([0,1,2,3], "go")

#these variables must be initialized here
fpsLabel = None
secondsLabel = None
dataLabels = None
started = False
draw = False
showFPS = SHOW_FPS
showData = SHOW_DATA
showSeconds = SHOW_SECONDS


#*******************************************************************
#*******************************************************************
#************************* MAIN LOOP *******************************
#*******************************************************************
#*******************************************************************
#GAME LOOP. This will run every frame (FRAMERATE times per second) until the program is closed
while True:
    #close window if x is clicked
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #limit framerate
    ms = Clock.tick(FRAMERATE)

    #increment frame count and track seconds passed
    frameCount += 1
    if frameCount % FRAMERATE == 0 : secondsPassed += 1
    #reset frameCount each minute
    if frameCount >= (FRAMERATE*60) : 
        frameCount = 0
        
    #only draw every other frame, 60 draws per second is sufficient for fluid motion
    if frameCount % 2 == 0: draw = True

    #generates the info text labels each second. These must be in multiple labels because
    #the pygame font renderer cannot handle newline characters
    if frameCount % FRAMERATE == 0:
        fpsText = ("FPS: "+str(int(Clock.get_fps())))
        fpsLabel = Font.render(fpsText, 1, black)
        secondsText = ("Seconds Passed: "+str(secondsPassed))
        secondsLabel = Font.render(secondsText, 1, black)
        dataLabels = []
        for key,value in ow.analytics.getData().items():
            if isinstance(value, float):
                dataText = (key+": "+str("%.2f" % round(value,2)))
            elif isinstance(value, str) or isinstance(value, int):
                dataText = (key+": "+str(value))
            color = light_grey
            if 'Metric' in key or 'Status' in key : color = black
            dataLabels.append(Font.render(dataText, 1, color))

    #keep up to date with statistics each frame
    ow.analytics.auto()

    #run the learning module
    ow.learning.auto()

    #baseline has been gathered, start actual light controller
    if ow.analytics.getTimePassed() >= BASELINE_TIME + BASELINE_WARMUP_TIME and not started:
        ow.lc.start(mode='independent')
        started = True

    #auto spawn vehicles
    ow.autoVehicSpawn(frameCount, screen)

    #the screen must be erased (filled white) every frame, the additional
    #elements are then redrawn over the white surface after their
    #positions are recalculated. This creates the illusion of motion
    if draw :screen.fill(background)

    #draw the road system
    if draw : ow.rs.draw()

    #allow vehicles to act, then redraw them
    for vehic in ow.vehics:
        vehic.auto()
        if draw : vehic.draw()
    
    #handle keyboard input
    #presently, keyboard input is only used for testing purposes
    if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                if frameCount%10 == 0:
                    showData = not showData
            elif event.key == pygame.K_2:
                if frameCount%10 == 0:
                    showFPS = not showFPS
         
    #display the FPS (Frames Per Second) and statistical text each second
    if fpsLabel and showFPS: screen.blit(fpsLabel, (0,0))
    if secondsLabel and showSeconds: screen.blit(secondsLabel, (0, 35))
    if dataLabels and showData:
        for i in range(len(dataLabels)):
            screen.blit(dataLabels[i], (600,0+(35*i)))
    redraw = False
    
    #update the screen
    pygame.display.flip()

