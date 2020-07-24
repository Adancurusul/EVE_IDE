from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5 import QtCore
from PyQt5 import QtWidgets

if __name__ == '__main__':

    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication([])
    view =QWebEngineView()
    view.load(QUrl('http://192.168.137.217/'))
    view.show()
    app.exec_()
