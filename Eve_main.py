import sys
import os
from select_workspace import Ui_select
from first_test import Ui_MainWindow
#from sele import Ui_s
from PyQt5.QtCore import (QEvent, QFile, QFileInfo, QIODevice, QRegExp,
                          QTextStream,Qt,QSize)
from PyQt5.QtWidgets import (QAction, QApplication,  QFileDialog,QLayout,QSplitter,QStyleFactory,QAbstractItemView,
                             QMainWindow, QMessageBox, QTextEdit,QToolBar,QMdiArea,QDockWidget,
                             QTreeWidgetItem,QFileIconProvider)
from PyQt5.QtGui import QFont, QIcon,QColor,QKeySequence,QSyntaxHighlighter,QTextCharFormat,QTextCursor

from PyQt5.QtCore import  pyqtSignal
from PyQt5 import QtCore
import lupa
import time
from functools import partial
import qdarkstyle
from window import main_win,select_work
configure_file = "configure.txt"


def file_name(path):
    return os.listdir(path)

def read_line(name,li):
    with open(name,"r") as in_file:
        num = 0
        for line in in_file:
            num+=1
            if num ==li:
                return line

def write_line(name,li,sentence):
    with open(configure_file, 'r') as re_file:
        lines = re_file.readlines()

        with open(configure_file, 'w+')as wr_file:
            lines[li-1] = sentence+'\n'
            wr_file.writelines(lines)


class logic_main(main_win):
    def __init__(self):
        super(logic_main, self).__init__()

        self.trigger_connection()  # 信号与槽连接
        self.view_dock_closeEvent()  # 重写dock关闭函数

    def view_dock_closeEvent(self):  # 当dock关闭时触发
        self.dockWidget_tree.closeEvent = self.dock_tree_close
        self.dockBuilt.closeEvent = self.dockBuilt_close

    def set_tree(self):

        path = read_line(configure_file, 1)[:-1]
        print(path)
        dirs = file_name(path)
        print(dirs)
        fileInfo = QFileInfo(path)
        fileIcon = QFileIconProvider()
        icon = QIcon(fileIcon.icon(fileInfo))
        root = QTreeWidgetItem(self.tree)
        root.setText(0, path.split('/')[-1])
        root.setIcon(0, QIcon(icon))
        self.CreateTree(dirs, root, path)
        # self.setCentralWidget(self.tree)
        QApplication.processEvents()

    def CreateTree(self, dirs, root, path):
        for i in dirs:
            path_new = path + '/' + i
            if os.path.isdir(path_new):
                fileInfo = QFileInfo(path_new)
                fileIcon = QFileIconProvider()
                icon = QIcon(fileIcon.icon(fileInfo))
                child = QTreeWidgetItem(root)
                child.setText(0, i)
                child.setIcon(0, QIcon(icon))
                dirs_new = file_name(path_new)
                self.CreateTree(dirs_new, child, path_new)
            else:
                fileInfo = QFileInfo(path_new)
                fileIcon = QFileIconProvider()
                icon = QIcon(fileIcon.icon(fileInfo))
                child = QTreeWidgetItem(root)
                child.setText(0, i)
                child.setIcon(0, QIcon(icon))

    def trigger_connection(self):
        self.menuEdit.triggered[QAction].connect(self.do_edit_menu)
        # self.actionHeaven.clicked.connect(lambda : self.change_style(1))
        # self.actionHell.clicked.connect(lambda: self.change_style(0))
        self.menuFile.triggered[QAction].connect(self.do_file_menu)
        self.action_project_files.triggered.connect(partial(self.view_triggered, "project_files"))
        self.actionBuild_output.triggered.connect(partial(self.view_triggered, "Build_output"))
        self.actionWindows.triggered.connect(app.slot_setStyle)
        self.actionWindowsXP.triggered.connect(app.slot_setStyle)
        self.actionWindowsVista.triggered.connect(app.slot_setStyle)
        self.actionFusion.triggered.connect(app.slot_setStyle)
        self.actionDark.triggered.connect(app.slot_setStyle)

    '''
    def toggle_build_output(self,state):
        if state:
            self.dockBuilt.show()
        else:
            self.dockBuilt.hide()

    def change_style(self,style):
        if style:
            write_line(configure_file,3,1)
    '''

    def view_triggered(self, name, state):  # 当view下按键状态改变时触发
        if name == "Build_output":
            if state:
                self.dockBuilt.show()
            else:
                self.dockBuilt.hide()
        if name == "project_files":
            if state:
                self.dockWidget_tree.show()
            else:
                self.dockWidget_tree.hide()

    def do_file_menu(self, action_of_file):
        print(action_of_file.text() + "is triggered")

    def do_edit_menu(selfself, action_of_edit):
        print(action_of_edit.text() + "is triggered")

    # def actionOpen(self):
    #   print("open_ok")
    def update_enable(self):
        pass

    def dockBuilt_close(self, p):
        print(p)
        self.actionBuild_output.setChecked(0)

    def dock_tree_close(self, p):
        print(p)
        print("dock_closed")
        self.action_project_files.setChecked(0)


# def fn(): print('something'); dock.closeEvent = fn


def open_main_window():  # 选择完workspace之后执行打开主窗口
    # ap = QApplication(sys.argv)
    # mainwin = main_win()
    mainwin.show()
    print("openit")
    # sys.exit(app.exec_())


def decide_if_open_selection():
    line = int(read_line(configure_file, 2))
    if line:
        return 1


class Application(QApplication):
    def __init__(self, argv):
        QApplication.__init__(self, argv)

    def slot_setStyle(self):
        app.setStyleSheet('')
        tmp = self.sender().objectName()[6:]
        print(tmp)
        if tmp in QStyleFactory.keys():
            app.setStyle(tmp)
            write_line(configure_file, 3, tmp)

        elif tmp == 'Dark':
            app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        write_line(configure_file, 3, tmp)


if __name__ == "__main__":
    style = read_line(configure_file, 3)[:-1]

    # print(style)
    show_it = decide_if_open_selection()
    # def open_select_window():

    app = Application(sys.argv)
    win = select_work()
    # mainwin = main_win()
    mainwin = logic_main()

    if style == "Dark":
        print("okk")
        # setup stylesheet
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    else:
        if style in QStyleFactory.keys():
            app.setStyleSheet('')
            app.setStyle(style)
            # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
            print("okkkk")

    if not show_it:

        win.show()
    else:
        mainwin.show()
    # win.buttonBox.accepted.connect(open_main_window)

    sys.exit(app.exec_())

# open_select_window()


