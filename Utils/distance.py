from math import sqrt

#Find the center point of a rectangle
def findCntrPnt(rect):
    x1,y1,w,h = rect[0], rect[1], rect[2], rect[3]
    x2 = x1 + w
    y2 = y1 + h
    xa = (x1+x2)/2
    ya = (y1+y2)/2
    return [xa, ya]

#Calculate the distance between 2 points
def dist(start, end):
    x1,y1 = start[0], start[1]
    x2,y2 = end[0], end[1]
    return sqrt((x2-x1)**2 + (y2-y1)**2)