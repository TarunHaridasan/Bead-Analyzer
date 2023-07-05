from PyQt5.QtCore import QThreadPool, QRunnable

class Thread():
    def __init__(self, threadViewWidget):
        self.threadpool = QThreadPool()
        self.widget = threadViewWidget
        self.active = []
        self.completed = []
        self.inactived = []
    def add(self, data, tracker):
        worker = Worker(data, tracker)
        self.threadpool.start(worker)
    def updateList():
        pass
    def clearList(self): 
        self.widget.clear()

class Worker(QRunnable):
    def run(self, data, tracker):
        pass