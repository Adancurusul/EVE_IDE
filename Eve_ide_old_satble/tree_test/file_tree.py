import sys
from PyQt5.QtWidgets import *
from PyQt5 import Qt, QtGui
from filename import file_name
from fileopen import Ui_MainWindow
from PyQt5 import QtWidgets
import threading
import os
#actionfileopen

class Tree(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Tree, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("File_Tree")
        #self.actionfileopen.triggered.connect(self.Open_Folder)
        self.Open_Folder()
    def Open_Folder(self):
        #path = read_line(configure_file,1)
        #path = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")
        path = 'D:/codes/python/Eve_ide'
        self.tree = QTreeWidget()
        self.tree.setColumnCount(1)
        self.tree.setColumnWidth(0, 50)
        #self.tree.setHeaderLabels(["EXPLORER"])
        self.tree.setIconSize(Qt.QSize(25, 25))
        self.tree.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.actionfileopen.triggered.connect(self.Open_Folder)



        dirs = file_name(path)

        fileInfo = Qt.QFileInfo(path)
        fileIcon = Qt.QFileIconProvider()
        icon = QtGui.QIcon(fileIcon.icon(fileInfo))
        root = QTreeWidgetItem(self.tree)
        root.setText(0, path.split('/')[-1])
        root.setIcon(0, QtGui.QIcon(icon))
        self.CreateTree(dirs, root, path)
        self.setCentralWidget(self.tree)
        QApplication.processEvents()

    def CreateTree(self, dirs, root, path):
        for i in dirs:
            path_new = path + '/' + i
            if os.path.isdir(path_new):
                fileInfo = Qt.QFileInfo(path_new)
                fileIcon = Qt.QFileIconProvider()
                icon = QtGui.QIcon(fileIcon.icon(fileInfo))
                child = QTreeWidgetItem(root)
                child.setText(0, i)
                child.setIcon(0, QtGui.QIcon(icon))
                dirs_new = file_name(path_new)
                self.CreateTree(dirs_new, child, path_new)
            else:
                fileInfo = Qt.QFileInfo(path_new)
                fileIcon = Qt.QFileIconProvider()
                icon = QtGui.QIcon(fileIcon.icon(fileInfo))
                child = QTreeWidgetItem(root)
                child.setText(0, i)
                child.setIcon(0, QtGui.QIcon(icon))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Tree()
    win.show()
    sys.exit(app.exec_())
