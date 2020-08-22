
import sys
from PyQt5.QtWidgets import QMainWindow , QApplication

app = QApplication(sys.argv)
win = QMainWindow()
win.setWindowTitle("界面背景图片设置")
win.resize(350,  250)
win.setObjectName("MainWindow")
win.setStyleSheet("#MainWindow{image:url(./icos/background.png);}")
#win.setStyleSheet("#MainWindow{background-color: yellow}")
win.show()
sys.exit(app.exec_())