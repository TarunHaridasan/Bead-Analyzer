# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 980)
        MainWindow.setMinimumSize(QtCore.QSize(1300, 980))
        MainWindow.setMaximumSize(QtCore.QSize(1300, 980))
        MainWindow.setStyleSheet("font-family: Calibri;\n"
"font-size: 17px;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayout = QtWidgets.QFormLayout(self.centralwidget)
        self.formLayout.setObjectName("formLayout")
        self.Left = QtWidgets.QGridLayout()
        self.Left.setObjectName("Left")
        self.frame = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(900, 800))
        self.frame.setMaximumSize(QtCore.QSize(900, 800))
        self.frame.setMouseTracking(True)
        self.frame.setAutoFillBackground(False)
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setText("")
        self.frame.setScaledContents(False)
        self.frame.setObjectName("frame")
        self.Left.addWidget(self.frame, 0, 0, 1, 1)
        self.console = QtWidgets.QListWidget(self.centralwidget)
        self.console.setObjectName("console")
        self.Left.addWidget(self.console, 1, 0, 1, 1)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.Left)
        self.Right = QtWidgets.QGridLayout()
        self.Right.setObjectName("Right")
        self.threadView = QtWidgets.QListWidget(self.centralwidget)
        self.threadView.setObjectName("threadView")
        self.Right.addWidget(self.threadView, 4, 0, 1, 4)
        self.bboxes = QtWidgets.QListWidget(self.centralwidget)
        self.bboxes.setObjectName("bboxes")
        self.Right.addWidget(self.bboxes, 1, 0, 1, 4)
        self.start = QtWidgets.QPushButton(self.centralwidget)
        self.start.setEnabled(False)
        self.start.setObjectName("start")
        self.Right.addWidget(self.start, 5, 0, 1, 2)
        self.next = QtWidgets.QPushButton(self.centralwidget)
        self.next.setEnabled(False)
        self.next.setObjectName("next")
        self.Right.addWidget(self.next, 5, 2, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("font-family: Calibri;\n"
"font-size: 20px;")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.Right.addWidget(self.label_2, 3, 0, 1, 4)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("font-family: Calibri;\n"
"font-size: 20px;\n"
"")
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.Right.addWidget(self.label, 0, 0, 1, 4)
        self.add = QtWidgets.QPushButton(self.centralwidget)
        self.add.setEnabled(False)
        self.add.setObjectName("add")
        self.Right.addWidget(self.add, 2, 0, 1, 1)
        self.remove = QtWidgets.QPushButton(self.centralwidget)
        self.remove.setEnabled(False)
        self.remove.setObjectName("remove")
        self.Right.addWidget(self.remove, 2, 1, 1, 1)
        self.reset = QtWidgets.QPushButton(self.centralwidget)
        self.reset.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.reset.setFont(font)
        self.reset.setObjectName("reset")
        self.Right.addWidget(self.reset, 2, 2, 1, 1)
        self.beadCount = QtWidgets.QLCDNumber(self.centralwidget)
        self.beadCount.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.beadCount.setFrameShadow(QtWidgets.QFrame.Raised)
        self.beadCount.setSmallDecimalPoint(False)
        self.beadCount.setDigitCount(3)
        self.beadCount.setMode(QtWidgets.QLCDNumber.Dec)
        self.beadCount.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.beadCount.setProperty("intValue", 0)
        self.beadCount.setObjectName("beadCount")
        self.Right.addWidget(self.beadCount, 2, 3, 1, 1)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.Right)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1300, 27))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.newAnalysis = QtWidgets.QAction(MainWindow)
        self.newAnalysis.setObjectName("newAnalysis")
        self.actionNext = QtWidgets.QAction(MainWindow)
        self.actionNext.setObjectName("actionNext")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.newAnalysis)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Fluorescent Bead Analyzer"))
        self.start.setText(_translate("MainWindow", "Start"))
        self.next.setText(_translate("MainWindow", "Next"))
        self.label_2.setText(_translate("MainWindow", "Queue"))
        self.label.setText(_translate("MainWindow", "Beads"))
        self.add.setText(_translate("MainWindow", "Add"))
        self.remove.setText(_translate("MainWindow", "Remove"))
        self.reset.setText(_translate("MainWindow", "Reset"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.newAnalysis.setText(_translate("MainWindow", "New"))
        self.actionNext.setText(_translate("MainWindow", "Next"))
        self.actionAbout.setText(_translate("MainWindow", "About"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
