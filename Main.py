import sys, pygame
from RoadSystem import *
from Config import *
from Vehicle import *


#initialize pygame, the game library used for visually
#representing the simulation
pygame.init()

#initialize the screen surface onto which everything
#will be drawn
screen = pygame.display.set_mode(size)

#initialize the clock instance which allows framerate regulation
Clock = pygame.time.Clock()

#a font instance must be initialized so we can render
#text within the game loop
Font = pygame.font.Font(None, 36)

frameCount = 0
secondsPassed = 0

rs = RoadSystem('r1.txt', screen, width, height)
cars = []

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

    for car in cars:
        car.auto()
        car.draw()
    
    #handle keyboard input
    if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                if frameCount%10 == 0:
                    c = Vehicle(screen,rs.features['EA1'].x,rs.features['EA1'].y,20,10,'car.png',rs.features['R2'],rs.features['R2'].lane1,rs.features['PA3'],rs.features['PA3'].light1,'forward',rs.features['R2'].lane1.getLastVehicle())
                    rs.features['R2'].lane1.vehicles.append(c)
                    cars.append(c)
            elif event.key == pygame.K_2:
                print('asdf')

    
    #display the FPS (Frames Per Second) and info text
    screen.blit(fpsLabel, (0,0))
    screen.blit(secondsLabel, (0, 35))
    
    #update the screen
    pygame.display.flip()

