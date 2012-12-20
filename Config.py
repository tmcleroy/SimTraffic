
#this config file allows for easy changing of system variables


#window size and positioning vars
SIZE = WIDTH, HEIGHT = 1280, 720
MIDDLE_X = int(WIDTH/2)
MIDDLE_Y = int(HEIGHT/2)

#framerate. The screen will refresh this many times per second
FRAMERATE = 120

#variables which determine which stats are printed to the window
SHOW_FPS = False#True
SHOW_SECONDS = False#True
SHOW_DATA = True

#file names
ROAD_SYSTEM_FILE_NAME = 'ROAD_SYSTEMS/road.txt'
VEHICLE_IMAGE_FILE_NAME = 'IMAGES/car.bmp'

#IDs of high traffic (HT) and normal (NM) roads
#Downward facing roads have ID 1, upward facing roads have ID 3
#Left facing roads have ID 2, right facing roads have ID 4
HT_ROADS = [2,4]
NM_ROADS = [1,3]

#must be greater than 0
#values less than 1 decrease all vehicle speeds
#values greater than 1 increase all vehicle speeds
VEHICLE_SPEED_MULTIPLIER = 1

#timing and scoring weight importance of a vehicle on a high traffic road
#vehicles on high traffic roads may be considered more important than normal ones
#Ex. 1 normal traffic vehicle = 1*HT...WEIGHT high traffic vehicle
#a weight of 1 means no additional weight is applied
HT_TIMING_WEIGHT = 5#1
HT_SCORING_WEIGHT = 5

#minutes the analytics system will wait before starting to keep track of stats
#this is necessary because the road system cannot be fully populated right away
#and must take some time to get to full capacity
WARMUP_TIME = 0.50
BASELINE_WARMUP_TIME = 0.50
BASELINE_TIME = 0.50

#light timing variables
TIMING = 'independent' 	#do not change
YELLOW_TIME = 3 		#seconds a light will stay yellow before turning red
MIN_GREEN_TIME = 5 		#minimum seconds a light will stay green
INACTIVITY_PAUSE = 2 	#seconds to pause between light switching decisions

#reinforcement learning variables
LEARNING_SAMPLE_INTERVAL =  0.75 	#minutes between statistical samples for the learning module
LEARNING_CHANGE_INTERVAL = 0.25 	#amount by which a variable is changed each tick

#colors
road_line_yellow = (255,255,50)
road_grey = (220, 220, 220)
background = (255,255,255)
black = (0, 0, 0)
white = (255,255,255)
grey = (150, 150, 150)
light_grey = (225,225,225)
dark_grey = (90, 95, 90)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,244)
yellow = (255,255,0)
purple = (255,0,255)

