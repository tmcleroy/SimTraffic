"""
This config file allows for easy changing of system variables
"""

#imports
from pprint import pprint

#dimensions of the simulation window
size = width, height = 1280, 720

#file name of the RoadSystem
roadSystemFileName = 'roadSystems/r2.txt'

#type of light timing
TIMING = 'independent'

#positioning variables
middleX = int(width/2)
middleY = int(height/2)

#framerate of the simulation. The screen will refresh this
#many times per second
framerate = 120

#colors
black = 0, 0, 0
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,244)
yellow = (255,255,0)
purple = (255,0,255)
light_grey = (225,225,225)
grey = (150, 150, 150)
dark_grey = (90, 95, 90)
