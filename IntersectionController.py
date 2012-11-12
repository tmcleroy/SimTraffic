import time
from threading import Thread

class IntersectionController(Thread):

    def __init__(self, intersection):
        self.intersection = intersection
        self.poles = self.intersection.poles
        self.curr_flow = None
        Thread.__init__(self)


    def run(self):
        #print("in run ", self.intersection)

        numOdd = len(self.poles[0].vehics)+len(self.poles[2].vehics)
        numEven = len(self.poles[1].vehics)+len(self.poles[3].vehics)


        if numOdd > numEven and self.curr_flow == 'even':
            self.flow('odd')
            time.sleep(5)
        elif numEven > numOdd and self.curr_flow == 'odd':
            self.flow('even')
            time.sleep(5)
        elif numEven == numOdd and not self.curr_flow == 'even':
            self.flow('even')
            time.sleep(5)
        else: 
            time.sleep(5)
            
        self.run()


        

    def wait(self, seconds):
        time.sleep(seconds)
        """
        t = threading.Thread(target=self.auto)
        t.start()
        """

    #sets the state of all lights in the intersection after a set amount of time
    #sleep is the number of seconds to wait before setting the lights
    def setAllLights(self, state, sleep=0):
        if sleep: self.wait(sleep)
        for pole in self.poles:
            for light in pole.lights:
                light.setState(state)

        
    #sets the states of specific lights in the intersection after a set amount of time
    #lights is a list containing the indices of the lights that will be set
    #sleep is the number of seconds to wait before setting the lights
    def setLights(self, lights, state, sleep=0):
        if sleep: time.sleep(sleep)
        for i in range(len(self.poles)):
            if i in lights:
                for light in self.poles[i].lights:
                    light.setState(state)

                    

    def transToState(self, lights, state):
        if state == 'go':
            self.setLights(lights, 'go')
            return
        elif state == 'stop':
            t = Thread(target=self.setLights, args=(lights, state, 3))
            t.start()
            self.setLights(lights, 'slow')


    def flow(self, dir='none'):
        if dir == 'even':
            self.setLights([0,2], 'slow')
            time.sleep(3)
            self.setLights([0,2], 'stop')
            time.sleep(1)
            self.setLights([1,3], 'go')
            self.curr_flow = 'even'
            
            """
            self.transToState([0,2], 'stop')
            self.transToState([1,3], 'go')
            self.curr_flow = 'even'
            #time.sleep(3)
            #self.run()
            """
        if dir == 'odd':
            self.setLights([1,3], 'slow')
            time.sleep(3)
            self.setLights([1,3], 'stop')
            time.sleep(1)
            self.setLights([0,2], 'go')
            self.curr_flow = 'odd'         
            
            """
            self.transToState([0,2], 'go')
            self.transToState([1,3], 'stop')
            self.curr_flow = 'odd'
            #time.sleep(3)
            #self.run()
            """
