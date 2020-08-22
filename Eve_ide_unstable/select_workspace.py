# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'select_workspace.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_select(object):
    def setupUi(self, select):
        select.setObjectName("select")
        select.resize(616, 244)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pic/main.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        select.setWindowIcon(icon)
        select.setAutoFillBackground(False)
        self.checkBo = QtWidgets.QCheckBox(select)
        self.checkBo.setGeometry(QtCore.QRect(13, 169, 317, 23))
        self.checkBo.setStyleSheet("font: 8pt \"Corbel\";\n"
"")
        self.checkBo.setObjectName("checkBo")
        self.buttonBox = QtWidgets.QDialogButtonBox(select)
        self.buttonBox.setGeometry(QtCore.QRect(360, 190, 233, 34))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(select)
        self.label.setEnabled(True)
        self.label.setGeometry(QtCore.QRect(13, 13, 402, 44))
        self.label.setMaximumSize(QtCore.QSize(16777215, 16777214))
        self.label.setStyleSheet("font: 18pt \"Agency FB\";\n"
"")
        self.label.setObjectName("label")
        self.layoutWidget = QtWidgets.QWidget(select)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 80, 571, 61))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(13, 20, 30, 7)
        self.horizontalLayout.setSpacing(14)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setStyleSheet("font: 11pt \"Arial Rounded MT Bold\";")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.select_directory = QtWidgets.QPushButton(self.layoutWidget)
        self.select_directory.setObjectName("select_directory")
        self.horizontalLayout.addWidget(self.select_directory)

        self.retranslateUi(select)
        #self.buttonBox.accepted.connect(select.accept)
        self.buttonBox.rejected.connect(select.close)
        self.checkBo.toggled['bool'].connect(select.hide)
        #self.select_directory.clicked.connect(select.open)
        QtCore.QMetaObject.connectSlotsByName(select)

    def retranslateUi(self, select):
        _translate = QtCore.QCoreApplication.translate
        select.setWindowTitle(_translate("select", "Eve IDE"))
        self.checkBo.setText(_translate("select", "use this as the default and do not ask again"))
        self.label.setText(_translate("select", "Select a directory as your workspace"))
        self.label_2.setText(_translate("select", "Workspace:"))
        self.select_directory.setText(_translate("select", "select"))
import icons_rc
