import time

class Stopwatch():
    def __init__(self):
        self.StartTime = 0
        self.EndTime = 0
        self.TimePassed = 0
        self.TempStart = 0
        self.TempEnd = 0
        self.TimePaused = 0
        self.started = False

    def start(self):
        self.StartTime = time.time()
        self.started = True

    def secondsPassed(self):
        if self.started:
            self.EndTime = time.time()
            self.TimePassed = self.EndTime - self.StartTime - self.TimePaused
            return self.TimePassed
        else:
            return 0

    def Pause(self):
        self.TempStart = time.time()
        return self.TempStart - self.StartTime

    def Unpause(self):
        self.TempEnd = time.time()
        self.TimePaused = self.TempEnd - self.TempStart
    
    def reset(self):
        self.StartTime = 0
        self.EndTime = 0
        self.TimePassed = 0
        self.TempStart = 0
        self.TempEnd = 0
        self.TimePaused = 0
        self.started = False
