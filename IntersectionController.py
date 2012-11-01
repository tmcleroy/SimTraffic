import time
import threading

class IntersectionController:

    def __init__(self, intersection):
        self.intersection = intersection
        self.poles = self.intersection.poles


    def setAllLights(self, state, sleep=0):
        if sleep: time.sleep(sleep)
        for pole in self.poles:
            for light in pole.lights:
                light.setState(state)

    def transAllToState(self, state):
        if state == "go":
            self.setAllLights("go")
            return
        t = threading.Thread(target=self.setAllLights, args=(state, 3))
        t.start()
        self.setAllLights("slow")
