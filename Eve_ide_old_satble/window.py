import sys
import os
from select_workspace import Ui_select
from first_test import Ui_MainWindow
# from sele import Ui_s
from PyQt5.QtCore import (QEvent, QFile, QFileInfo, QIODevice, QRegExp,
                          QTextStream, Qt, QSize)
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QLayout, QSplitter, QStyleFactory, QAbstractItemView,
                             QMainWindow, QMessageBox, QTextEdit, QToolBar, QMdiArea, QDockWidget, QMenu,
                             QTreeWidgetItem, QFileIconProvider)
from PyQt5.QtGui import QFont, QIcon, QColor, QKeySequence, QSyntaxHighlighter, QTextCharFormat, QTextCursor, QCursor, \
    QPixmap
from PyQt5.Qsci import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore
import lupa
import time
from functools import partial
import qdarkstyle
import keyword

configure_file = "configure.txt"
open_by_main = 0


def file_name(path):
    return os.listdir(path)


def read_line(name, li):  # 读取指定文件指定行
    with open(name, "r") as in_file:
        num = 0
        for line in in_file:
            num += 1
            if num == li:
                return line


def write_line(name, li, sentence):  # 写入到指定文件指定行
    with open(configure_file, 'r') as re_file:
        lines = re_file.readlines()

        with open(configure_file, 'w+')as wr_file:
            lines[li - 1] = sentence + '\n'
            wr_file.writelines(lines)


class MyLexerCPP(QsciLexerCPP):
    def __init__(self, parent):
        QsciLexerCPP.__init__(self, parent)
        self.setFont(self.parent().Font)
        self.setColor(QColor(0, 0, 0))  # 设置默认的字体颜色
        self.setPaper(QColor(255, 255, 255))  # 设置底色
        self.setColor(QColor("#B0171F"), QsciLexerCPP.Keyword)

        self.setColor(QColor("#008000"), QsciLexerCPP.CommentDoc)  # 文档注释 /**开头的颜色
        self.setColor(QColor("#008000"), QsciLexerCPP.Comment)  # 块注释 的颜色
        self.setColor(QColor("#008000"), QsciLexerCPP.CommentLine)  # 行注释的颜色
        self.setColor(QColor("#007f7f"), QsciLexerCPP.Number)  # 数字 的颜色
        self.setColor(QColor("#ff00ff"), QsciLexerCPP.DoubleQuotedString)  # 双引号字符串的颜色
        self.setColor(QColor("#ff00ff"), QsciLexerCPP.SingleQuotedString)  # 单引号字符的颜色
        self.setColor(QColor("#be07ff"), QsciLexerCPP.PreProcessor)  # 预编译语句的颜色
        self.setColor(QColor("#191970"), QsciLexerCPP.Operator)
        # self.setColor(QColor("#000000"), QsciLexerCPP.Identifier)  #可识别字符的颜色，这个范围很广，包含了关键词，函数名；所以要取消这句
        self.setColor(QColor("#0000FF"), QsciLexerCPP.UnclosedString)  # 未完成输入的字符串的颜色

        font = QFont(self.parent().Font)
        font.setBold(True)
        self.setFont(font, 5)  # 默认的字体加粗。

        font = QFont(self.parent().Font)
        font.setItalic(True)
        self.setFont(font, QsciLexerCPP.Comment)  # 注释的字体用斜体。


class SciTextEdit(QsciScintilla):
    NextId = 1

    def __init__(self, filename='', wins=None, parent=None):
        global g_allFuncList
        super(QsciScintilla, self).__init__(parent)
        self.win = wins
        self.jumpName = ''
        self.list_line = []
        self.Font = QFont()
        # self.Font = self.win.EditFont  # 采用主窗口传入的字体
        self.Font.setFixedPitch(True)
        #self.loadFile(self.filename)
        self.setFont(self.Font)
        # 1.设置文档的编码格式为 “utf8” ，换行符为 windows   【可选linux，Mac】
        self.setUtf8(True)
        self.setEolMode(QsciScintilla.SC_EOL_CRLF)  # 文件中的每一行都以EOL字符结尾（换行符为 \r \n）
        # 2.设置括号匹配模式
        self.setBraceMatching(QsciScintilla.StrictBraceMatch)  #
        # 3.设置 Tab 键功能
        self.setIndentationsUseTabs(True)  # 行首缩进采用Tab键，反向缩进是Shift +Tab
        self.setIndentationWidth(4)  # 行首缩进宽度为4个空格




        self.setIndentationGuides(True)  # 显示虚线垂直线的方式来指示缩进
        self.setTabIndents(True)  # 编辑器将行首第一个非空格字符推送到下一个缩进级别
        self.setAutoIndent(True)  # 插入新行时，自动缩进将光标推送到与前一个相同的缩进级别
        self.setBackspaceUnindents(True)
        self.setTabWidth(4)  # Tab 等于 4 个空格
        # 4.设置光标
        self.setCaretWidth(2)  # 光标宽度（以像素为单位），0表示不显示光标
        self.setCaretForegroundColor(QColor("darkCyan"))  # 光标颜色
        self.setCaretLineVisible(True)  # 是否高亮显示光标所在行
        self.setCaretLineBackgroundColor(QColor('#FFCFCF'))  # 光标所在行的底色
        # 5.设置页边特性。        这里有3种Margin：[0]行号    [1]改动标识   [2]代码折叠
        # 5.1 设置行号
        self.setMarginsFont(self.Font)  # 行号字体
        self.setMarginLineNumbers(0, True)  # 设置标号为0的页边显示行号
        self.setMarginWidth(0, '00000')  # 行号宽度
        self.setMarkerForegroundColor(QColor("#FFFFFF"), 0)
        # 5.2 设置改动标记
        self.setMarginType(1, QsciScintilla.SymbolMargin)  # 设置标号为1的页边用于显示改动标记
        self.setMarginWidth(1, "0000")  # 改动标记占用的宽度
        img = QPixmap("test1.png")  # 改动标记图标，大小是48 x 48
        sym_1 = img.scaled(QSize(16, 16))  # 图标缩小为 16 x 16
        self.markerDefine(sym_1, 0)
        self.setMarginMarkerMask(1, 0b1111)
        self.setMarkerForegroundColor(QColor("#ee1111"), 1)  # 00ff00
        # 5.3  设置代码自动折叠区域
        self.setFolding(QsciScintilla.PlainFoldStyle)
        self.setMarginWidth(2, 12)
        # 5.3.1 设置代码折叠和展开时的页边标记 - +
        self.markerDefine(QsciScintilla.Minus, QsciScintilla.SC_MARKNUM_FOLDEROPEN)
        self.markerDefine(QsciScintilla.Plus, QsciScintilla.SC_MARKNUM_FOLDER)
        self.markerDefine(QsciScintilla.Minus, QsciScintilla.SC_MARKNUM_FOLDEROPENMID)
        self.markerDefine(QsciScintilla.Plus, QsciScintilla.SC_MARKNUM_FOLDEREND)
        # 5.3.2 设置代码折叠后，+ 的颜色FFFFFF
        self.setMarkerBackgroundColor(QColor("#FFBCBC"), QsciScintilla.SC_MARKNUM_FOLDEREND)
        self.setMarkerForegroundColor(QColor("red"), QsciScintilla.SC_MARKNUM_FOLDEREND)

        # 6.语法高亮显示
        # 6.1语法高亮的设置见 MyLexerCPP类 源码
        self.lexer = MyLexerCPP(self)
        self.setLexer(self.lexer)
        # 6.2设置自动补全
        self.mod = False
        self.__api = QsciAPIs(self.lexer)
        # SDCC编译器的关键字 列表
        sdcc_kwlist = ['__data', '__idata', '__pdata', '__xdata', '__code', '__bit', '__sbit',
                       '__sfr', 'u8', 'u16', 'WORD', 'BYTE', 'define', 'include', '__interrupt',
                       'auto', 'double', 'int', 'struct', 'break', 'else', 'long',
                       'switch', 'case', 'enum', 'register', 'typedef', 'default',
                       'char', 'extern', 'return', 'union', 'const', 'float',
                       'short', 'unsigned', 'continue', 'for', 'signed', 'void',
                       'goto', 'sizeof', 'volatile', 'do', 'while', 'static', 'if']
        autocompletions = keyword.kwlist + sdcc_kwlist
        # autocompletions = sdcc_kwlist
        print("sciisodk")

        for ac in autocompletions:
            self.__api.add(ac)
        self.__api.prepare()
        self.autoCompleteFromAll()
        self.setAutoCompletionSource(QsciScintilla.AcsAll)  # 自动补全所以地方出现的
        self.setAutoCompletionCaseSensitivity(True)  # 设置自动补全大小写敏感
        self.setAutoCompletionThreshold(1)  # 输入1个字符，就出现自动补全 提示
        self.setAutoCompletionReplaceWord(False)
        self.setAutoCompletionUseSingle(QsciScintilla.AcusExplicit)
        self.setAttribute(Qt.WA_DeleteOnClose)
        # 设置函数名为关键字2    KeyWord = sdcc_kwlistcc  ;KeywordSet2 = 函数名
        self.SendScintilla(QsciScintilla.SCI_SETKEYWORDS, 0, " ".join(sdcc_kwlist).encode(encoding='utf-8'))
        self.SendScintilla(QsciScintilla.SCI_STYLESETFORE, QsciLexerCPP.KeywordSet2, 0x7f0000)
        # self.SendScintilla(QsciScintilla.SCI_SETKEYWORDS, 1, " ".join(g_allFuncList).encode(encoding='utf-8'))

        self.filename = filename
        if self.filename == '':
            self.filename = str("未命名-{0}".format(SciTextEdit.NextId))
            SciTextEdit.NextId += 1
        self.setModified(False)
        # 设置文档窗口的标题
        self.setWindowTitle(QFileInfo(self.filename).fileName())
        # 将槽函数链接到文本改动的信号
        self.textChanged.connect(self.textChangedAction)
        # 给文档窗口添加右键菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)  #
        self.customContextMenuRequested.connect(self.RightMenu)
        # self.win.setWidget(self)

    def RightMenu(self):
        print("右键")

    def textChangedAction(self):
        line, index = self.getCursorPosition()  # 获取当前光标所在行
        #self.win.from_sci(self.win,1)
        self.win.dis_enable(self.win,1)
        if not line ==0:
            handle_01 = self.markerAdd(line, 0)  # 添加改动标记
            print(handle_01)
            self.list_line.append(handle_01)


class select_work(QMainWindow, Ui_select):
    def __init__(self):
        global open_by_main
        super(select_work, self).__init__()

        self.setupUi(self)

        self.setWindowIcon(QIcon("main.ico"))
        self.show_next_time = True
        self.hide_0 = 0
        self.get_old_workspace()
        self.change_state = 0
        # self.open_by_main= 0

    def get_old_workspace(self):  # 获取原来的工作位置
        self.old_space = read_line(configure_file, 1)
        self.lineEdit.setText(self.old_space)
        print(self.old_space)

    @QtCore.pyqtSlot()
    def on_select_directory_clicked(self):
        self.new_space = QFileDialog.getExistingDirectory(self,
                                                          "选取文件夹",
                                                          "./")  # 起始路径
        self.lineEdit.setText(self.new_space)
        print(self.new_space)
        self.change_state = 1
        # write_line(configure_file,1,self.new_space)
        self.lineEdit.selectAll()

    '''
    def ope(self):#单击select的操作

        self.new_space = QFileDialog.getExistingDirectory(self,
                                                      "选取文件夹",
                                                      "./")  #起始路径
        self.lineEdit.setText(self.new_space)
        print(self.new_space)
        self.change_state = 1
        #write_line(configure_file,1,self.new_space)

        self.lineEdit.selectAll()
    '''

    def hide(self):  #

        self.hide_0 += 1
        if not self.hide_0 % 2 == 0:
            self.show_next_time = False
        else:
            self.show_next_time = True
        print(self.show_next_time)

    # def accept(self):
    @QtCore.pyqtSlot()
    def on_buttonBox_accepted(self):
        if not self.show_next_time:
            write_line(configure_file, 2, "1")
            print("notshow")

        if self.change_state == 1:
            write_line(configure_file, 1, self.new_space)

        self.close()

        open_main_window()


class main_win(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(main_win, self).__init__()
        self.setupUi(self)
        self.my_setupUi()  # 优化界面

        # self.trigger_connection()#信号与槽连接
        # self.view_dock_closeEvent()#重写dock关闭函数

    def my_setupUi(self):
        self.tree.setColumnCount(1)  # 设置列数
        self.tree.header().hide()
        self.mdi = QMdiArea()

        self.tabWidget = QTabWidget()
        self.tabWidget.setTabsClosable(True)
        #self.mdi.setViewMode(QMdiArea.TabbedView)  # 设置为Tab多页显示模式
        #self.mdi.setTabsClosable(1)
        self.text_browser = QTextEdit(self)  # QtextEditClick继承自QTextEdit，内置于信息输出视图
        self.text_browser.setReadOnly(True)  # 仅作为信息输出，设置“只读”属性
        self.serial_info = QTextEdit(self)  # QtextEditClick继承自QTextEdit，内置于信息输出视图
        self.serial_info.setReadOnly(True)
        #self.loadFile(self.filename)
        # 1.3创建信息输出视图
        self.dock_serial = QDockWidget('Serial monitor', self)
        # self.dock_connection.setText("connnnn")
        # self.dock_serial.setMinimumSize(600, 150)
        self.dock_serial.setWidget(self.serial_info)
        self.dockBuilt = QDockWidget('Built output', self)
        # self.dockBuilt.setFearures(DockWidgetClosable)
        self.dockBuilt.setFeatures(
            QDockWidget.DockWidgetClosable | QDockWidget.DockWidgetMovable)
        self.dockBuilt.setMinimumSize(600, 150)  # 宽=600，高=   150
        self.dockBuilt.setWidget(self.text_browser)
        self.tabifyDockWidget(self.dockBuilt, self.dock_serial)
        splitter1 = QSplitter(Qt.Vertical)
        splitter1.addWidget(self.mdi)  # 多文档视图占布局右上
        splitter1.addWidget(self.dockBuilt)  # 信息输出视图占布局右下
        # self.addDockWidget(Qt.LeftDockWidgetArea, self.dockProject)  # 工程视图占布局左边
        self.setCentralWidget(splitter1)
        self.tabifyDockWidget(self.dock_connection, self.dock_serial)

        self.tree.setIconSize(QSize(25, 25))
        self.tree.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.sub =QMdiSubWindow()
        self.sub.setWidget(self.tabWidget)
        self.mdi.addSubWindow(self.sub)
        self.sub.showMaximized()
        self.sub.setWindowFlags(Qt.FramelessWindowHint)
        self.set_tree()


class logic_main(main_win):
    def __init__(self):
        super(logic_main, self).__init__()
        self.project_path = read_line(configure_file, 1)[:-1]
        self.list_of_files_with_path = []  # 完整名称
        self.list_of_files = []  # 无路径
        self.file_path_dict = {}
        #self.dis_enable(0)
        self.file_list(self.project_path, self.list_of_files_with_path, self.list_of_files)  # 得到list 包含了完整路径和仅有名字

        self.trigger_connection()  # 信号与槽连接
        self.view_dock_closeEvent()  # 重写dock关闭函数
        # SciTextEdit()

    def dis_enable(self,state):
        print(str(state)+"this is state")
        self.action_save.setEnabled(state)
        self.action_saveas.setEnabled(state)
        self.actionChange_into_COE.setEnabled(state)
        self.actionChange_into_MIF.setEnabled(state)
        self.actionChange_into_Binary.setEnabled(state)
        self.actionChange_into_Hex.setEnabled(state)
        self.actionView_the_Eluminate.setEnabled(state)
        self.actioncut.setEnabled(state)
        self.actionpaste.setEnabled(state)
        self.actionindent.setEnabled(state)
        self.actionunindent.setEnabled(state)
        self.actioncopy.setEnabled(state)
        self.actionDownload_2.setEnabled(state)

        #self.action_save.setEabled(state)

    # self.file_list(self.project_path,self.list_of_files)
    def file_list(self, path, list_name, li):  # 传入存储的list
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isdir(file_path):
                self.file_list(file_path, list_name, li)
            else:
                list_name.append(file_path)
                li.append(file)
                self.file_path_dict.setdefault(file, file_path)
        # return list_name

    def view_dock_closeEvent(self):  # 当dock关闭时触发
        self.dockWidget_tree.closeEvent = self.dock_tree_close
        self.dockBuilt.closeEvent = self.dockBuilt_close

    def set_tree(self):
        self.tree.clear()
        path = read_line(configure_file, 1)[:-1]
        print("+" * 10 + path)
        dirs = file_name(path)
        print(dirs)
        fileInfo = QFileInfo(path)
        fileIcon = QFileIconProvider()
        icon = QIcon(fileIcon.icon(fileInfo))
        root = QTreeWidgetItem(self.tree)
        root.setText(0, path.split('/')[-1])
        root.setIcon(0, QIcon(icon))
        self.CreateTree(dirs, root, path)
        self.tree.expandAll()
        # self.setCentralWidget(self.tree)
        # self.tree.clicked.connect(self.onTreeClicked)
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
        self.tree.itemDoubleClicked.connect(self.onTreeClicked)  # 双击树某个child
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)  # 开放右键策略
        self.tree.customContextMenuRequested.connect(self.OnTreeRightMenuShow)  # 树的右键菜单
        self.actionchoose_workspace.triggered.connect(self.choose_workspace)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
    def closeTab(self):
        i = self.tabWidget.currentIndex()
        self.tabWidget.removeTab(i)

    def choose_workspace(self):
        global open_by_main
        # write_line(configure_file,4,"1")
        open_by_main = 1
        reply = QMessageBox.question(self, '警告', '更换工作区域将重启Eve IDE\n请确保换工作区前所有文件已经保存',
                                     QMessageBox.Ok, QMessageBox.Cancel)
        if reply == QMessageBox.Ok:
            # select = select_work()
            select.checkBo.setEnabled(False)
            select.checkBo.setText('')

            '''
            #@QtCore.pyqtSlot()
            def on_buttonBox_accept():

                if not self.show_next_time:
                    write_line(configure_file, 2, "1")
                    print("notshow")


                if select.change_state:
                    write_line(configure_file, 1, select.new_space)
                    print("sssssssssssssss")
                select.close()

            select.buttonBox.accepted.connect(on_buttonBox_accept)
            '''
            select.show()
        else:
            pass
        # write_line(configure_file, 4, "0")
        # open_by_main = 0

    def OnTreeRightMenuShow(self):
        print("右键")
        item = self.tree.currentItem()  # 获取鼠标所在的树状列表的项
        print(item.text(0))
        self.tree.popMenu = QMenu()
        if '.' in item.text(0) and '.cbp' not in item.text(0):  # 该项是文件名，添加右键[删除菜单]
            delectFile4Proj = QAction('Delect file from project', self)
            open_file_in_project = QAction('Open the file', self)
            self.refresh_tree = QAction('Refresh', self)
            self.tree.popMenu.addAction(delectFile4Proj)
            self.tree.popMenu.addAction(open_file_in_project)
            self.tree.popMenu.addAction(self.refresh_tree)
            delectFile4Proj.triggered.connect(self.do_delectFile4Proj)
            open_file_in_project.triggered.connect(self.onTreeClicked)
            self.refresh_tree.triggered.connect(self.refresh_treearea)
        else:  # 该项非文件名，添加右键[添加菜单]

            addFile2Proj = QAction("Refresh", self)

            self.tree.popMenu.addAction(addFile2Proj)
            addFile2Proj.triggered.connect(self.refresh_treearea)
        self.tree.popMenu.exec_(QCursor.pos())  # 在鼠标位置显示

    def refresh_treearea(self):
        self.set_tree()

    def do_delectFile4Proj(self):
        reply = QMessageBox.question(self, '警告', '你将彻底删除该文件\n你确认要删除吗？',
                                     QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:

            item = self.tree.currentItem()

            # 2.从文件列表中删除
            w_d = self.file_path_dict[item]
            self.file_path_dict.pop(item)
            os.remove(w_d)
            self.list_of_files.remove(item)
            self.list_of_files_with_path.remove((w_d))

            '''
            for i in range(len(self.list_of_files)):
                if item.text(0) in self.list_of_files[i] :
                    w_d = self.list_of_files_with_path[i]
                    os.remove(w_d)

                    del self.list_of_files_with_path[i]
                    del self.list_of_files[i]
                    break
            '''

            # 3.从窗口中删除
            if item.parent() is not None:
                item.parent().removeChild(item)

            # print("file")
        else:  #
            pass

    def do_open_file(self):
        print("ok")

    def onTreeClicked(self, which):
        item = self.tree.currentItem()
        if '.' in item.text(0):
            #self.sub = QMdiSubWindow()
            #self.mdi.addSubWindow(self.sub)
            # item = self.tree.currentItem()
            it = item.text(0)
            filepath = self.file_path_dict[it]
            self.open_qsci(filepath)

            #self.editor = SciTextEdit(filepath)
            #filepath = self.file_path_dict[it]
            #self.tabWidget.addTab(self.editor, it)
            #print(self.editor)
            #obj = open(filepath, 'r+', encoding='utf-8')
            #self.editor.setText(obj.read())
            #q = SciTextEdit(filepath, wins=self.sub)
            #self.sub.setWidget(q)

            print("key=%s " % (item.text(0)))

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
    def open_qsci(self,fname):
        filename, extension = os.path.split(fname)
        if filename:
            print(filename+'aaaaaa'+extension)
            self.editor = SciTextEdit(fname,wins=logic_main,parent=self.tabWidget)
            # filepath = self.file_path_dict[it]
            self.tabWidget.addTab(self.editor, extension)
            print(self.editor)
            obj = open(fname, 'r+', encoding='utf-8')
            self.editor.setText(obj.read())
            # q = SciTextEdit(filepath, wins=self.sub)
            # self.sub.setWidget(q)

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
        if action_of_file.text() == 'Open':
            self.openaction(False)

    def do_edit_menu(self, action_of_edit):
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



    def openaction(self,name):
        if name:
            pass
        else:
            filename, _buff = QFileDialog.getOpenFileName(self, '另存为', './', 'All (*.*)')
            self.open_qsci(filename)



def open_main_window():  # 选择完workspace之后执行打开主窗口
    # print(read_line(configure_file,4)[:-1]+str(select.change_state))
    print(open_by_main)
    print(select.change_state)
    if open_by_main and not select.change_state:
        # ap = QApplication(sys.argv)
        # mainwin = main_win()
        # mainwin = logic_main()
        print("not need")
        pass
    else:
        mainwin.show()
        mainwin.set_tree()  # 重新设置一次workspace
        select.change_state = 0
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
    select = select_work()
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

        select.show()
    else:
        mainwin.show()
    # win.buttonBox.accepted.connect(open_main_window)

    sys.exit(app.exec_())

# open_select_window()



