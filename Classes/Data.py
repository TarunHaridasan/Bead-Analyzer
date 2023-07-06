import cv2
import os
import numpy as np

class Data:
    #Load the images from the video
    def __init__(self, fp):
        self.fp = fp
        self.images = []
        self.boundingBoxes = []  
        files = os.listdir(self.fp)
        for i in range(0,len(files)):
            item = files[i]
            fp = f'{self.fp}//{item}'
            image = cv2.imread(fp)
            self.images.append(image)
        self.size = len(self.images)
    #Get an image
    def get(self, index):
        return self.images[index]
    #Initially detect fluorescent beads off an image
    def findBeads(self):
        self.boundingBoxes = []
        image = self.get(0).copy()
        cropped = image[30:870, 30:770]
        gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        blob = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 5)
        #Opening (remove noise)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))
        blob = cv2.morphologyEx(blob, cv2.MORPH_OPEN, kernel)
        #Closing
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))
        blob = cv2.morphologyEx(blob, cv2.MORPH_CLOSE, kernel)
        #Find contours
        blob = 255 - blob
        contours, hier = cv2.findContours(blob, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = [c + 30 for c in contours]
        if len(contours)==0:
            return []
        #Find 50th percentile area
        areas = []
        for cnt in contours:
            areas.append(cv2.contourArea(cnt))
        areas.sort()
        a = areas[int(len(areas)*0.25)]
        #Remove bounding boxes with area too small
        boundingBoxes = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area>a:
                x,y,w,h = cv2.boundingRect(cnt)
                boundingBoxes.append([x,y,w,h])
        self.boundingBoxes = boundingBoxes
        return boundingBoxes
    #Return the bounding box the x,y coordinates are inside
    def findBox(self,x,y):
        for box in self.boundingBoxes:
            x1,y1,w,h = box[0], box[1], box[2], box[3]
            x2,y2 = x1+w, y1+h
            if x>x1 and x<x2 and y>y1 and y<y2: #Inside
                return [x1, y1, w, h]
        return 0    
    #Remove bounding box
    def removeBounding(self, x, y):
        box = self.findBox(x,y)
        if box!=0:
            self.boundingBoxes.remove(box)  
        return self.boundingBoxes
    #Add bounding box
    def addBounding(self, x, y, x2,y2):
        w = x2-x
        h = y2-y
        self.boundingBoxes.append([x,y,w,h])
        return self.boundingBoxes
            