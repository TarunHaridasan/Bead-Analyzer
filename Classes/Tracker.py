from openpyxl import Workbook
from Classes.SubTracker import SubTracker
from openpyxl.styles.fonts import Font
from datetime import datetime

class Tracker:
    def __init__(self, image, output, conversion, fps):
        self.trackers = []
        self.image = image
        self.size = 0
        self.start = datetime.now()
        self.output = output
        self.conversion = conversion
        self.fps = fps
    def add(self, box):
        tracker = SubTracker(self.image, box)
        self.trackers.append(tracker)
        self.size=+1
    def remove(self, tracker):
        self.trackers.remove(tracker)
    def update(self, image):
        self.image = image
        for tracker in self.trackers:
            tracker.update(image)
    def updateDistances(self):
        for tracker in self.trackers:
            tracker.updateDistance()
    def updateDisplacements(self):
        for tracker in self.trackers:
            tracker.updateDisplacement()
    def newBoxes(self):
        boxes = []
        for tracker in self.trackers:
            boxes.append(tracker.current)
        return boxes
    def saveData(self):
        wb = Workbook()
        ws = wb.active
        now = datetime.now()
        elapsed = (now-self.start).total_seconds()
        ws.append(["Time Started", "End Time", "Elapsed Time (mins)"])
        ws.append([self.start.strftime("%H:%M:%S"), now.strftime("%H:%M:%S"), '{:.2f}'.format(round(elapsed/60, 2))])
        ws.append(["Blob", "Distance (um)", "Displacement (um)", "Frames", "Speed (um/s)", "Velocity (um/s)"])
        bold = Font(bold=True)
        for i in ["A1", "B1", "C1", "A3", "B3", "C3", "D3", "E3", "F3", "G3", "H3"]:
            ws[i].font = bold      
        for i in range(len(self.trackers)):
            blob = f'Blob {i}' 
            tracker = self.trackers[i]           
            distance = tracker.distance * self.conversion
            displacement = tracker.displacement * self.conversion
            frames = tracker.frames
            if frames == 0:
                continue
            speed = distance / (frames/self.fps)
            velocity = displacement / (frames/self.fps)
            initial = tracker.start
            final = tracker.current
            ws.append([blob, distance, displacement, frames, speed, velocity])
        
        wb.save(self.output)

        