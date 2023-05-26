import cv2
from Utils.distance import *

class SubTracker():
    def __init__(self, image, bounding): #Initialize tracker
        self.start = bounding
        self.prev = self.start
        self.current = self.start
        self.distance = 0
        self.displacement = 0
        self.frames = 0
        self.tracker = cv2.TrackerCSRT_create()
        self.tracker.init(image, bounding)
        self.active = 1
    def update(self, image): #Update tracker frame
        #print(self.active, self.prev, self.current)
        if not self.active: 
            return
        retval, box = self.tracker.update(image)
        self.prev = self.current
        if retval:            
            self.current = box
            if self.current[0] < 50 or self.current[0]>850 or self.current[1]<50 or self.current[1]>750:
                self.active = 0
            self.updateDistance()
            self.updateFrames()
    def draw(self, image): #Draw bounding boxes on rectangle
        cv2.rectangle(image, self.current, (0, 255, 21), 2)
        cv2.imshow('Bead Analyzer', image)
    def updateDistance(self): #Update the distance
        p1, p2 = findCntrPnt(self.prev), findCntrPnt(self.current)
        x1, y1, x2, y2 = p1[0], p1[1], p2[0], p2[1] 
        distance = sqrt((x2-x1)**2 + (y2-y1)**2)
        self.distance+=distance
    def updateDisplacement(self): #Update the displacement
        p1, p2 = findCntrPnt(self.start), findCntrPnt(self.current)
        x1, y1, x2, y2 = p1[0], p1[1], p2[0], p2[1] 
        displacement = sqrt((x2-x1)**2 + (y2-y1)**2)
        self.displacement=displacement
    def updateFrames(self):
        self.frames+=1