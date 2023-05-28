from openpyxl import Workbook
from openpyxl.styles import Font
from Classes.SubTracker import SubTracker

class Tracker:
    def __init__(self, image):
        self.trackers = []
        self.image = image
        self.size = 0
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
    def saveData(self, output, conversion, fps):
        wb = Workbook()
        ws = wb.active
        ws.append(["Blob", "Distance (um)", "Displacement (um)", "Frames", "Speed (um/s)", "Velocity (um/s)", "Start Coordinates", "End Coordinates"])
        ws["A1"].font, ws["B1"].font, ws["C1"].font, ws["D1"].font, ws["E1"].font, ws["F1"].font = Font(bold=True), Font(bold=True), Font(bold=True), Font(bold=True), Font(bold=True), Font(bold=True)
        for i in range(len(self.trackers)):
            blob = f'Blob {i}' 
            tracker = self.trackers[i]           
            distance = tracker.distance * conversion
            displacement = tracker.displacement * conversion
            frames = tracker.frames
            speed = distance / (frames/fps)
            velocity = displacement / (frames/fps)
            initial = tracker.start
            final = tracker.current
            ws.append([blob, distance, displacement, frames, speed, velocity, str(initial), str(final)])
        wb.save(output)

        