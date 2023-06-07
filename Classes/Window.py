from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QDialog
import GUI.main
import GUI.settings
from Classes.Data import Data
import sys
import cv2
from Classes.Console import Console
import qdarktheme
import time
from Classes.Tracker import Tracker
from PyQt5.QtCore import QObject, QThread, pyqtSignal


class Window():
    #Instantiate the main and settings window
    def __init__(self):
        #Main window
        self.app = QtWidgets.QApplication(sys.argv)
        qdarktheme.setup_theme(custom_colors={"primary": "#fa05c1"})
        self.Main = QtWidgets.QMainWindow()
        self.Main.ui = GUI.main.Ui_MainWindow()
        self.Main.ui.setupUi(self.Main)
        #Dialog window
        self.Dialog = QtWidgets.QDialog()
        self.Dialog.ui = GUI.settings.Ui_Dialog()
        self.Dialog.ui.setupUi(self.Dialog)
        self.Main.ui.newAnalysis.triggered.connect(self.Dialog.exec)
        self.Dialog.ui.inputSearch.clicked.connect(self.searchInput)
        self.Dialog.ui.outputSearch.clicked.connect(self.searchOutput)
        self.Dialog.ui.buttonBox.accepted.connect(self.saveSettings)
        self.Main.ui.reset.clicked.connect(self.resetBoxes)
        self.Main.ui.remove.clicked.connect(self.removeMode)
        self.removeActive = 0
        self.Main.ui.add.clicked.connect(self.addMode)
        self.addActive = 0
        self.addBoxStart=1
        self.newBoxCoordinates = []
        self.Main.ui.start.clicked.connect(self.run)
        #Console window
        self.console = Console(self.Main.ui.console)
    
    #Display the window
    def start(self):
        self.Main.show()
        #REMOVE AFTER
        #self.saveSettings()
        sys.exit(self.app.exec_())
    
    #Collect input data
    def searchInput(self):
        fp = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select Folder')
        self.Dialog.ui.inputFP.setText(fp)            

    #Collect output data
    def searchOutput(self):
        fp = QtWidgets.QFileDialog.getOpenFileName(None, 'Select File')[0]
        self.Dialog.ui.outputFP.setText(fp)

    #Save settings
    def saveSettings(self):        
        self.inputFP = self.Dialog.ui.inputFP.text()
        self.folderName = self.inputFP.split("/")[-1]
        self.outputFP = self.Dialog.ui.outputFP.text()
        self.fps = self.Dialog.ui.fps.value()
        self.conversion = self.Dialog.ui.conversion.value()
        self.outputFP = "./Output" #Default output path
        self.data = Data(self.inputFP)
        self.data.findBeads()   
        self.print(self.data.get(0))     
        self.updateList()
        self.console.add(f'Settings Saved. Load {self.data.size} images')

    #Print image and bounding boxes
    def print(self, image):
        #Add boxes around the blobs
        frame = image.copy()
        for i in range(len(self.data.boundingBoxes)):
            box = self.data.boundingBoxes[i]
            x,y,w,h = box[0], box[1], box[2], box[3]
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255, 0, 21),2)  
        #Convert to Pixmap for PyQT5
        height, width, channel = frame.shape
        bytesPerLine = 3 * width
        qImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap(qImg)
        self.Main.ui.frame.setPixmap(pixmap)     
    
    #Update the bounding box list with current boxes
    def updateList(self):
        list = self.Main.ui.bboxes
        list.clear()
        boxes = self.data.boundingBoxes
        for i in range(len(boxes)):
            list.addItem(f'Bead {i}: {str(boxes[i])}')    
    
    #Activate/deactivate remove mode
    def removeMode(self):
        if not self.removeActive:
            self.console.add("Remove mode activated")
            self.Main.ui.frame.mousePressEvent = self.removeBox                      
        else:
            self.console.add("Remove mode deactivated")
            self.Main.ui.frame.mousePressEvent = lambda *args: None    
        self.removeActive = not self.removeActive     
    
    #Activate/deactivate add mode
    def addMode(self):
        if not self.addActive:
            self.console.add("Add mode activated")
            self.Main.ui.frame.mousePressEvent = self.addBox           
        else:
            self.console.add("Add mode deactivated")
            self.Main.ui.frame.mousePressEvent = lambda *args: None      
        self.addActive = not self.addActive   

    #Remove a bounding box
    def removeBox(self, event):
        x, y = event.x(), event.y()
        print(x,y)
        self.data.removeBounding(x, y)
        self.print(self.data.get(0))
        self.updateList()

    #Add a bounding box
    def addBox(self, event):
        if self.addBoxStart:
            self.newBoxCoordinates = [event.x(), event.y()]            
        else:
            self.data.addBounding(self.newBoxCoordinates[0], self.newBoxCoordinates[1], event.x(), event.y())
            self.print(self.data.get(0))
            self.updateList()
        self.addBoxStart = not self.addBoxStart
    
    #Reset Bounding Boxes
    def resetBoxes(self):
        self.data.findBeads()   
        self.print(self.data.get(0))     
        self.updateList()
        self.console.add(f'Reset bounding boxes to default')

    #Highlight bounding box
    def highlightBounding(self, item):
        index = self.ui.boundingBoxes.indexFromItem(item).row()
        print(index)
        self.data.print(self.data.get(0), index)

    #Run the tracking on all the boxes
    def run(self):
        self.console.add("Analysis started")
        self.tracker = Tracker(self.data.get(0))   
        for box in self.data.boundingBoxes:
            self.tracker.add(box)

        self.thread = QThread()
        self.worker = Worker(self.data, self.tracker)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.reportAnalysisProgress)
        self.worker.finished.connect(self.analysisFinished)
        self.worker.finished.connect(self.thread.quit)

        self.thread.start()

    def reportAnalysisProgress(self, i):
        progress = int((i/self.data.size)*100)
        print(progress)
        self.Main.ui.progressBar.setValue(progress)
        self.print(self.data.get(i))
        self.updateList()   
    
    def analysisFinished(self):        
        self.Main.ui.progressBar.setValue(100)
        self.tracker.updateDisplacements()
        output = f'{self.outputFP}/{self.folderName}.xlsx'
        self.tracker.saveData(output, self.conversion, self.fps) #Also send fps and conversion
        self.console.add(f'Analysis completed. Data saved into {output}')



#Analysis thread
class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self, data, tracker):
        super().__init__()
        self.data = data
        self.tracker = tracker

    def run(self):
        for i in range(self.data.size):
            img = self.data.get(i)
            self.tracker.update(img)
            self.data.boundingBoxes = self.tracker.newBoxes()
            self.progress.emit(i)
        self.finished.emit()