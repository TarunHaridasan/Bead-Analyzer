from PyQt5 import QtWidgets
from frame import Ui_MainWindow
from data import Data, Tracker
import cv2
import sys

class Window():
    #Initialize
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.ui = ui
        self.app = app
        self.ui.search.clicked.connect(self.intiateData)
        self.ui.remove.clicked.connect(self.removeBox)
        self.ui.add.clicked.connect(self.addBox)
        self.ui.remove.setStyleSheet("")
        self.ui.add.setStyleSheet("")
        self.ui.proceed.setStyleSheet("")
        self.ui.boundingBoxes.currentItemChanged.connect(self.highlightBounding)
        self.removeActive = 0  
        self.addActive = 0
        self.ui.proceed.clicked.connect(self.run)
    #Display the window
    def start(self):
        self.MainWindow.show()
        sys.exit(self.app.exec_())
    #Folder search
    def intiateData(self):
        fp = QtWidgets.QFileDialog.getExistingDirectory(self.MainWindow, 'Select Folder')
        #fp = "C:\\Users\\furio\\Desktop\\Fluorescent-Bead-Analyzer\\Data"
        self.ui.folderPath.setText(fp)
        self.data = Data(fp) 
        #self.data.findBeads()
        self.data.print(self.data.get(0))
        self.updateList()
        self.ui.add.setEnabled(1)
        self.ui.remove.setEnabled(1)
        self.ui.proceed.setEnabled(1)
    #Activate/deactivate remove mode
    def removeBox(self):
        if not self.removeActive:
            cv2.setMouseCallback("Beads", self.data.removeBounding)
            self.ui.remove.setStyleSheet("background-color: rgb(171, 171, 171)")            
        else:
            cv2.setMouseCallback("Beads", lambda *args : None)
            self.ui.remove.setStyleSheet("")
            self.updateList()
        self.removeActive = not self.removeActive            
    #Activate/deactivate add mode
    def addBox(self):
        if not self.addActive:
            self.addActive = 1
            self.ui.add.setStyleSheet("background-color: rgb(171, 171, 171)") 
            self.data.addBounding()
            self.ui.add.setStyleSheet("") 
            self.addActive = 0
            self.updateList()
    #Populate the ListWidget with the bounding boxes
    def updateList(self):
        self.ui.boundingBoxes.clear()
        for i in range(len(self.data.boundingBoxes)):
            box = self.data.boundingBoxes[i]
            self.ui.boundingBoxes.addItem(f'Blob {i}: {box[0]},{box[1]},{box[0]+box[2]},{box[1]+box[3]}')
    #Highlight bounding box
    def highlightBounding(self, item):
        index = self.ui.boundingBoxes.indexFromItem(item).row()
        print(index)
        self.data.print(self.data.get(0), index)
    #Run the tracking on all the boxes
    def run(self):
        cv2.destroyWindow("Beads")
        self.ui.proceed.setStyleSheet("background-color: rgb(171, 171, 171)")

        tracker = Tracker(self.data.get(0))   

        for box in self.data.boundingBoxes:
            tracker.add(box)

        for i in range(self.data.size):
            self.ui.progressBar.setValue(int((i/self.data.size)*100))
            tracker.update(self.data.get(i))
            tracker.draw()            
            cv2.waitKey(15)

        self.ui.progressBar.setValue(100)
        self.ui.proceed.setStyleSheet("")
        tracker.updateDisplacements()
        #tracker.saveData()
        cv2.waitKey(0)
        cv2.destroyAllWindows()
window = Window()
window.start()