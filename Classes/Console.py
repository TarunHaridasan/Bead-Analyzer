from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QColor, QFont
from datetime import datetime

class Console():
    #Initialize console class
    def __init__(self, consoleWidget):
        self.widget = consoleWidget
    #Add entry into the console
    def add(self, message, colour = (255,255,255)):
        time = datetime.now().strftime("%H:%M:%S")
        item = QListWidgetItem(f'>[{time}] {message}')
        item.setForeground(QColor(colour[0], colour[1], colour[2]))
        self.widget.addItem(item)
        self.widget.scrollToItem(item)
    #Purge the console
    def clear(self): 
        self.widget.clear()