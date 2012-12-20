import time
from threading import Thread
from Config import *

#this class controls the lights in one particular intersection
#it essentially sets the states of its lights governing its odd or even
#roads depending on which type of road has the greatest vehicle weight
#(not physical weight but scoring weight)
class IntersectionController(Thread):

    def __init__(self, intersection, mode):
        self.intersection = intersection
        self.poles = self.intersection.poles
        self.mode = mode
        self.curr_flow = None
        self.yt = YELLOW_TIME
        self.gt = MIN_GREEN_TIME
        self.ip = INACTIVITY_PAUSE
        Thread.__init__(self)

	#this method runs automatically when start() is called on an instance of this class (becuase it's a Thread)
    #it essentially allows odd roads or even roads to flow depending on which has more vehicle weight
    def run(self):
        	        
        run = True
        while run == True:
            numOdd = self.getWeightedNums([0,2])
            numEven = self.getWeightedNums([1,3])

            if self.mode == 'independent':
                if numOdd > (numEven) and self.curr_flow == 'even':
                    self.flow('odd')
                    #print ('waiting for green time: ', self.gt)
                    time.sleep(self.gt)
                elif (numEven) > numOdd and (self.curr_flow == 'odd' or self.curr_flow == None):
                    self.flow('even')
                    #print ('waiting for green time: ', self.gt)
                    time.sleep(self.gt)
                elif (numEven) == numOdd and not self.curr_flow == 'even':
                    self.flow('even')
                    #print ('waiting for green time: ', self.gt)
                    time.sleep(self.gt)
                else:
                    #print ('pausing for inactivity pause: ', self.ip) 
                    time.sleep(self.ip)
    


    #returns the weighted equivalent of the number of vehicles on the roads defined by the given indices
    def getWeightedNums(self, indices):
        ret = 0
        for i in indices:
            for vehic in self.poles[i].vehics:
                ret += vehic.importance
        return ret


    #adds the given amount of importance to the vehicles on the roads defined by the given indices
    def setNewImportances(self, indices, amount):
        for i in indices:
            for vehic in self.poles[i].vehics:
                vehic.importance += amount
                if vehic.importance <= 0 : vehic.importance = 1


    #sets the state of all lights in the intersection
    def setAllLights(self, state):
        for pole in self.poles:
            for light in pole.lights:
                light.setState(state)

        
    #sets the states of given states
    #lights is a list containing the indices of the lights that will be set
    def setLights(self, lights, state):
        for i in range(len(self.poles)):
            if i in lights:
                for light in self.poles[i].lights:
                    light.setState(state)



    #used for updating light timing variables as dictated by the learning module
    def setTimingVars(self, yellowTime, minGreenTime, inactivityPause):
        self.yt = yellowTime
        self.gt = minGreenTime
        self.ip = inactivityPause

                    

    #flows either even or odd lanes safely by properly adjusting light states to avoid collisions
    def flow(self, dir='none'):
        if dir == 'even':
            self.setNewImportances([1,3],2)
            self.setLights([0,2], 'slow')
            #print ('waiting for yellow time: ', self.yt)
            time.sleep(self.yt)
            self.setLights([0,2], 'stop')
            time.sleep(1)
            self.setLights([1,3], 'go')
            self.curr_flow = 'even'

        elif dir == 'odd':
            self.setLights([1,3], 'slow')
            #print ('waiting for yellow time: ', self.yt)
            time.sleep(self.yt)
            self.setLights([1,3], 'stop')
            time.sleep(1)
            self.setLights([0,2], 'go')
            self.curr_flow = 'odd'         

