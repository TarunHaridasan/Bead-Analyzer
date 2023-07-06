from PyQt5.QtCore import QThreadPool, QRunnable
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QColor

class Queue():
    def __init__(self, threadViewWidget):
        self.threadpool = QThreadPool()
        self.widget = threadViewWidget
        self.queue = []
        self.cur = -1
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
    def add(self, name, fp):
        self.queue.append([name, fp, 0])    
        self.updateList()            
    def run(self, worker):
        self.threadpool.start(worker)
    def updateList(self):
        self.clearList()
        for i in self.queue:
            item = QListWidgetItem(i[0])
            if i[2]==0:                
                item.setForeground(QColor(255, 0, 0))
            elif i[2]==1:
                item.setForeground(QColor(255,255,0))
            else:
                item.setForeground(QColor(0, 255, 0))
            self.widget.addItem(item)        
    def clearList(self): 
        self.widget.clear()
    def size(self):
        return len(self.queue)
    def getNext(self):
        self.cur+=1
        self.queue[self.cur][2]=1
        item = self.queue[self.cur]
        return item[0], item[1]