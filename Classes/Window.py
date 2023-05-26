from PyQt5 import QtWidgets
import GUI.main
import GUI.settings
from Classes.Data import Data
import sys


class Window():
    #Instantiate the main and settings window
    def __init__(self):
        #Main window
        self.app = QtWidgets.QApplication(sys.argv)
        self.Main = QtWidgets.QMainWindow()
        self.Main.ui = GUI.main.Ui_MainWindow()
        self.Main.ui.setupUi(self.Main)
        #Dialog window
        self.Dialog = QtWidgets.QDialog()
        self.Dialog.ui = GUI.settings.Ui_Dialog()
        self.Dialog.ui.setupUi(self.Dialog)
        self.bindButtons()
    #Display the window
    def start(self):
        self.Main.show()
        sys.exit(self.app.exec_())
    #Connect signal emissions to functions
    def bindButtons(self):
        self.Main.ui.newAnalysis.triggered.connect(self.Dialog.exec)
        self.Dialog.ui.inputSearch.clicked.connect(self.inputData)
    #Collect input data
    def inputData(self):
        fp = self.folderSearch()
        self.Dialog.ui.inputFP.setText(fp)
        self.data = Data(fp) 
        # self.data.findBeads()
        # self.data.print(self.data.get(0))
        # #self.updateList()
    
    #Folder search
    def folderSearch(self):
        fp = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select Folder')
        if fp!="":
            return fp
        return False   
    
    
    
    
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
    #     self.ui.boundingBoxes.clear()
    #     for i in range(len(self.data.boundingBoxes)):
    #         box = self.data.boundingBoxes[i]
    #         self.ui.boundingBoxes.addItem(f'Blob {i}: {box[0]},{box[1]},{box[0]+box[2]},{box[1]+box[3]}')
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