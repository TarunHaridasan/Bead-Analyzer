from PyQt5.QtGui import QPixmap, QImage
import cv2

class Frame():
    def __init__(self, frameWidget, beadsWidget, lcd):
        self.widget = frameWidget
        self.beadsWidget = beadsWidget
        self.lcd = lcd
    #Print the image and beads in appropriate window
    def show(self, image, bounding = []):
        self.clear()
        frame = image.copy()
        for box in bounding:
            x,y,w,h = box[0], box[1], box[2], box[3]
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255, 0, 21),2)  
        height, width, channel = frame.shape
        bytesPerLine = 3 * width
        qImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap(qImg)
        self.widget.setPixmap(pixmap)   
        for i in range(len(bounding)):
            self.beadsWidget.addItem(f'Bead {i}: {str(bounding[i])}') 
        self.lcd.display(len(bounding))
    #Clear the image and beads from the window
    def clear(self):
        self.widget.clear()
        self.beadsWidget.clear()
    