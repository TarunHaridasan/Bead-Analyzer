from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage
import GUI.main
import GUI.settings
from Classes.Data import Data
import sys
import cv2
from Classes.Console import Console
import qdarktheme


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
        self.bindButtons()
        #Console window
        self.Console = Console(self.Main.ui.console)
    #Display the window
    def start(self):
        self.Main.show()
        sys.exit(self.app.exec_())
    #Connect signal emissions to functions
    def bindButtons(self):
        self.Main.ui.newAnalysis.triggered.connect(self.Dialog.exec)
        self.Dialog.ui.inputSearch.clicked.connect(self.searchInput)
        self.Dialog.ui.outputSearch.clicked.connect(self.searchOutput)
        self.Dialog.ui.buttonBox.accepted.connect(self.saveSettings)
    #Collect input data
    def searchInput(self):
        fp = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select Folder')
        if fp!="":
            self.Dialog.ui.inputFP.setText(fp)
            self.data = Data(fp)   
            self.data.findBeads()     
        return False  
    #Collect output data
    def searchOutput(self):
        fp = QtWidgets.QFileDialog.getOpenFileName(None, 'Select File')[0]
        if fp!="":
            self.Dialog.ui.outputFP.setText(fp)      
        return False  
    #Save settings
    def saveSettings(self):
        self.inputFP = self.Dialog.ui.inputFP.text()
        self.outputFP = self.Dialog.ui.outputFP.text()
        self.fps = self.Dialog.ui.fps.value()
        self.conversion = self.Dialog.ui.conversion.value()
        self.Console.add(f'Settings Saved. Load {self.data.size} images')
        self.print(self.data.get(0))
        self.updateList()
    #Print image and bounding boxes
    def print(self, image):
        #Add boxes around the blobs
        frame = image.copy()
        print(self.data.boundingBoxes)
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
    #Update the bounding box list
    def updateList(self):
        table = self.Main.ui.bboxes
        table.clear()
        for i in range(len(self.data.boundingBoxes)):
            table.insertRow(table.rowCount())
            table.setItem(table.rowCount()-1, 0, QtWidgets.QTableWidgetItem(str(i)))
            table.setItem(table.rowCount()-1, 1, QtWidgets.QTableWidgetItem(str(self.data.boundingBoxes[i]))) 
    
    
    
    # #Activate/deactivate remove mode
    # def removeBox(self):
    #     if not self.removeActive:
    #         cv2.setMouseCallback("Beads", self.data.removeBounding)
    #         self.ui.remove.setStyleSheet("background-color: rgb(171, 171, 171)")            
    #     else:
    #         cv2.setMouseCallback("Beads", lambda *args : None)
    #         self.ui.remove.setStyleSheet("")
    #         self.updateList()
    #     self.removeActive = not self.removeActive            
    # #Activate/deactivate add mode
    # def addBox(self):
    #     if not self.addActive:
    #         self.addActive = 1
    #         self.ui.add.setStyleSheet("background-color: rgb(171, 171, 171)") 
    #         self.data.addBounding()
    #         self.ui.add.setStyleSheet("") 
    #         self.addActive = 0
    #         self.updateList()
    # #Populate the ListWidget with the bounding boxes
    # def updateList(self):
    #    
    # #Highlight bounding box
    # def highlightBounding(self, item):
    #     index = self.ui.boundingBoxes.indexFromItem(item).row()
    #     print(index)
    #     self.data.print(self.data.get(0), index)
    # #Run the tracking on all the boxes
    # def run(self):
    #     cv2.destroyWindow("Beads")
    #     self.ui.proceed.setStyleSheet("background-color: rgb(171, 171, 171)")

    #     tracker = Tracker(self.data.get(0))   

    #     for box in self.data.boundingBoxes:
    #         tracker.add(box)

    #     for i in range(self.data.size):
    #         self.ui.progressBar.setValue(int((i/self.data.size)*100))
    #         tracker.update(self.data.get(i))
    #         tracker.draw()            
    #         cv2.waitKey(15)

    #     self.ui.progressBar.setValue(100)
    #     self.ui.proceed.setStyleSheet("")
    #     tracker.updateDisplacements()
    #     #tracker.saveData()
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()