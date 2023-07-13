from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QDialog
import GUI.main
import GUI.settings
from Classes.Data import Data
import sys
import cv2
from Classes.Console import Console
from Classes.Queue import Queue
from Classes.Frame import Frame
import qdarktheme
import time
from Classes.Tracker import Tracker
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QThreadPool, QRunnable
import os
import copy
import numpy

class Window():
    #Instantiate the main and settings window
    def __init__(self):
        #Main window
        self.app = QtWidgets.QApplication(sys.argv)
        qdarktheme.setup_theme(custom_colors={"primary": "#FFFFFF"})
        self.Main = QtWidgets.QMainWindow()
        self.Main.ui = GUI.main.Ui_MainWindow()
        self.Main.ui.setupUi(self.Main)
        #Dialog window
        self.Dialog = QtWidgets.QDialog()
        self.Dialog.ui = GUI.settings.Ui_Dialog()
        self.Dialog.ui.setupUi(self.Dialog)
        self.Main.ui.newAnalysis.triggered.connect(self.Dialog.exec)
        #self.Main.ui.actionNext.triggered.connect(self.runNext)
        self.Main.ui.stop.clicked.connect(self.runNext)
        self.Dialog.ui.inputSearch.clicked.connect(self.searchInput)
        self.Dialog.ui.outputSearch.clicked.connect(self.searchOutput)
        self.Dialog.ui.buttonBox.accepted.connect(self.saveSettings)
        self.Main.ui.reset.clicked.connect(self.resetBoxes)        
        self.addActive = 0
        self.addBoxStart=1
        self.newBoxCoordinates = []
        self.Main.ui.add.clicked.connect(self.addMode) 
        self.removeActive = 0    
        self.Main.ui.remove.clicked.connect(self.removeMode)  
        self.Main.ui.start.clicked.connect(self.run)        
        self.worker = 0
        #Additional widget windows
        self.console = Console(self.Main.ui.console)    
        self.queue = Queue(self.Main.ui.threadView) 
        self.frame = Frame(self.Main.ui.frame, self.Main.ui.bboxes, self.Main.ui.beadCount)     

    #Display the window
    def start(self):
        self.Main.show()
        sys.exit(self.app.exec_())

    #Collect input data
    def searchInput(self):
        fp = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select Folder')
        self.Dialog.ui.inputFP.setText(fp)            

    #Collect output data
    def searchOutput(self):
        fp = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select Folder')
        self.Dialog.ui.outputFP.setText(fp)

    #Save settings
    def saveSettings(self):        
        self.inputFP = self.Dialog.ui.inputFP.text()        
        self.outputFP = self.Dialog.ui.outputFP.text()
        self.fps = self.Dialog.ui.fps.value()
        self.conversion = self.Dialog.ui.conversion.value()
        self.outputFP = ".//Output"
        if self.inputFP == "" or self.outputFP == "" or self.fps == "" or self.conversion == "":
            return        
        for i in os.listdir(self.inputFP):
            fp = f'{self.inputFP}\{i}'
            self.queue.add(i, fp)
        self.console.add(f'Settings Saved. Loaded {self.queue.size()} videos into queue.')
        self.runNext()

    #Activate/deactivate add mode
    def addMode(self):
        if not self.addActive:
            self.console.add("Add Mode Activated")
            self.Main.ui.add.setStyleSheet("background-color:black;")
            self.Main.ui.frame.mousePressEvent = self.addBox           
        else:
            self.console.add("Add Mode Deactivated")
            self.Main.ui.add.setStyleSheet("background-color: transparent;")
            self.Main.ui.frame.mousePressEvent = lambda *args: None      
        self.addActive = not self.addActive   

    #Add a bounding box
    def addBox(self, event):
        if self.addBoxStart:
            self.newBoxCoordinates = [event.x(), event.y()]            
        else:
            bounding = self.data.addBounding(self.newBoxCoordinates[0], self.newBoxCoordinates[1], event.x(), event.y())
            self.frame.show(self.data.get(0), bounding)
        self.addBoxStart = not self.addBoxStart

    #Activate/deactivate remove mode
    def removeMode(self):
        if not self.removeActive:
            self.console.add("Remove Mode Activated")
            self.Main.ui.add.setStyleSheet("background-color:black;")
            self.Main.ui.frame.mousePressEvent = self.removeBox                      
        else:
            self.console.add("Remove Mode Deactivated")
            self.Main.ui.add.setStyleSheet("background-color: transparent;")
            self.Main.ui.frame.mousePressEvent = lambda *args: None    
        self.removeActive = not self.removeActive     

    #Remove a bounding box
    def removeBox(self, event):
        x, y = event.x(), event.y()
        bounding = self.data.removeBounding(x, y)
        self.frame.show(self.data.get(0), bounding) 

    #Reset Bounding Boxes
    def resetBoxes(self):
        bounding = self.data.findBeads()   
        self.frame.show(self.data.get(0), bounding)     
        self.console.add("Reset bounding boxes to default")

    #Open up the next video
    def runNext(self):
        name, fp = self.queue.next()
        data = Data(fp)
        bounding = data.findBeads()   
        self.frame.show(data.get(0), bounding)
        self.console.add(f'Loaded {name}. {self.queue.cur+1}/{self.queue.size()} in queue')
        self.data = data
        if self.worker!=0:
            self.worker.signals.progress.disconnect()

    #Run the tracking on all the boxes
    def run(self):
        data = copy.deepcopy(self.data)
        del self.data
        output = f'{self.outputFP}/{self.queue.current()}.xlsx'
        tracker = Tracker(data.get(0), output, self.conversion, self.fps)           
        for box in data.boundingBoxes:
            tracker.add(box)
        worker = Worker(data, tracker, self.queue.getQId())
        worker.signals.progress.connect(self.updateProgress)
        worker.signals.finished.connect(self.analysisFinished)
        worker.signals.queueProgress.connect(self.queue.setProgress)
        self.queue.run(worker)
        self.worker = worker
        self.console.add("Analysis Started")

    #Update each frame
    def updateProgress(self, progress, image, bounding, qid):
        self.frame.show(image, bounding)

    #Update when completed
    def analysisFinished(self, qid):        
        self.queue.completed(qid)
        self.console.add(f'Analysis For "{self.queue.getName(qid)}" Completed')

#Worker and signals
class Signals(QObject):
    finished = pyqtSignal(int)
    progress = pyqtSignal(int, numpy.ndarray, list, int)
    queueProgress = pyqtSignal(int, int)

class Worker(QRunnable):
    def __init__(self, data, tracker, qid):
        super().__init__()
        self.data = data
        self.tracker = tracker
        self.qid = qid
        self.signals = Signals()
    def run(self):
        for i in range(self.data.size):
            img = self.data.get(i)
            self.tracker.update(img)
            self.data.boundingBoxes = self.tracker.newBoxes()
            progress = int((i/self.data.size)*100)
            self.signals.progress.emit(progress, img, self.data.boundingBoxes, self.qid)
            self.signals.queueProgress.emit(self.qid, progress)
        self.signals.progress.emit(100, self.data.get(self.data.size-1), self.data.boundingBoxes, self.qid)
        self.tracker.updateDisplacements()
        self.tracker.saveData()
        self.signals.finished.emit(self.qid)