from PyQt5.QtCore import QThreadPool, QRunnable
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QColor

class Queue():
    def __init__(self, threadViewWidget):
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(10)
        self.widget = threadViewWidget
        self.queue = []
        self.cur = -1
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
    #Add item to the queue
    def add(self, name, fp):
        self.queue.append([name, fp, 0, 0]) #name, fp, status, progress
        self.updateList() 
    #Queue the worker to be run when thread available           
    def run(self, worker):
        self.threadpool.start(worker)
    #Update the queue window
    def updateList(self):
        self.clearList()
        for i in self.queue:
            item = QListWidgetItem(f'{i[0]} - {i[3]}%')
            if i[2]==0:                
                item.setForeground(QColor(255, 0, 0))
            elif i[2]==1:
                item.setForeground(QColor(255,255,0))
            else:
                item.setForeground(QColor(0, 255, 0))
            self.widget.addItem(item)        
    #Clear the list
    def clearList(self): 
        self.widget.clear()
    #Return the size of the quuee
    def size(self):
        return len(self.queue)
    #Go to the next item in the queue
    def next(self):
        self.cur+=1
        self.queue[self.cur][2]=1
        item = self.queue[self.cur]
        self.updateList()
        return item[0], item[1]
    #Get current QID
    def getQId(self):
        return self.cur
    #Get name form QID
    def getName(self, qid):
        return self.queue[qid][0]
    #Completed and change to green
    def completed(self, qid):
        self.queue[qid][2]=2
        self.updateList()
    #Set progress for a qid
    def setProgress(self, qid, progress):
        self.queue[qid][3] = progress
        self.updateList()
    #Return the current item in the queue
    def current(self):
        return self.queue[self.cur][0]