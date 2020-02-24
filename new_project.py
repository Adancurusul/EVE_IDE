# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_project.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import ( QMainWindow)


class Ui_new_project(object):
    def setupUi(self, new_project):
        new_project.setObjectName("new_project")
        new_project.resize(378, 192)
        new_project.setFixedSize(378,192)
        self.centralwidget = QtWidgets.QWidget(new_project)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(70, 60, 241, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 271, 41))
        self.label.setStyleSheet("font: 25 20pt \"Bahnschrift Light Condensed\";")
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(240, 110, 112, 34))
        self.pushButton.setObjectName("pushButton")
        new_project.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(new_project)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 378, 30))
        self.menubar.setObjectName("menubar")
        new_project.setMenuBar(self.menubar)

        self.retranslateUi(new_project)
        QtCore.QMetaObject.connectSlotsByName(new_project)

    def retranslateUi(self, new_project):
        _translate = QtCore.QCoreApplication.translate
        new_project.setWindowTitle(_translate("new_project", "New project"))
        self.label.setText(_translate("new_project", "Input project name :"))
        self.pushButton.setText(_translate("new_project", "OK"))
class new_project(QMainWindow,Ui_new_project):
    def __init__(self):
        super(new_project,self).__init__()
        self.setupUi(self)
        #self.init()