# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1203, 721)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.findStrokeButton = QtWidgets.QPushButton(self.centralwidget)
        self.findStrokeButton.setGeometry(QtCore.QRect(40, 620, 281, 23))
        self.findStrokeButton.setObjectName("findStrokeButton")
        self.loadButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadButton.setGeometry(QtCore.QRect(40, 50, 151, 23))
        self.loadButton.setObjectName("loadButton")
        self.downloadButton = QtWidgets.QPushButton(self.centralwidget)
        self.downloadButton.setGeometry(QtCore.QRect(610, 620, 251, 23))
        self.downloadButton.setObjectName("downloadButton")
        self.inputImage = QtWidgets.QLabel(self.centralwidget)
        self.inputImage.setGeometry(QtCore.QRect(40, 100, 512, 512))
        self.inputImage.setObjectName("inputImage")
        self.outputImage = QtWidgets.QLabel(self.centralwidget)
        self.outputImage.setGeometry(QtCore.QRect(610, 100, 512, 512))
        self.outputImage.setObjectName("outputImage")
        self.fileName = QtWidgets.QLabel(self.centralwidget)
        self.fileName.setGeometry(QtCore.QRect(210, 50, 871, 21))
        self.fileName.setText("")
        self.fileName.setObjectName("fileName")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1203, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.findStrokeButton.setText(_translate("MainWindow", "Найти очаги"))
        self.loadButton.setText(_translate("MainWindow", "Загрузить снимок МРТ"))
        self.downloadButton.setText(_translate("MainWindow", "Скачать обработанный снимок"))
        self.inputImage.setText(_translate("MainWindow", "Input"))
        self.outputImage.setText(_translate("MainWindow", "Output"))

