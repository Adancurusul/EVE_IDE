import sys
import os
from select_workspace import Ui_select
from new_project import new_project
from create_sourcefile import move_source
from first_test import Ui_MainWindow
import subprocess
# from sele import Ui_s
from PyQt5.QtCore import (QEvent, QFile, QFileInfo, QIODevice, QRegExp,
                          QTextStream, Qt, QSize,pyqtSignal,QObject)
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QLayout, QSplitter, QStyleFactory, QAbstractItemView,
                             QMainWindow, QMessageBox, QTextEdit, QToolBar, QMdiArea, QDockWidget, QMenu,
                             QTreeWidgetItem, QFileIconProvider)
from PyQt5.QtGui import QFont, QIcon, QColor, QKeySequence, QSyntaxHighlighter, QTextCharFormat, QTextCursor, QCursor, \
    QPixmap,QBrush
from PyQt5.Qsci import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore
import lupa
import time
from functools import partial
import qdarkstyle
import keyword
from serial_show import Pyqt5_Serial
from make_project import do_make

import threading

surpport_chips = ['empty','gd32vg103','prv332']
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

class EmittingStream(QObject):
    textWritten = pyqtSignal(str)  # 定义一个发送str的信号

    def write(self, text):
        self.textWritten.emit(str(text))

KEYWORD_LIST_FUNC = ['if', 'while', 'for', 'switch']
g_allFuncList = []


class lexer_c_getfunc:
    def __init__(self, fileFullName):
        self.current_row = -1
        self.current_line = 0
        self.fullName = fileFullName
        if not os.path.exists(fileFullName):
            return None  # 文件名为空  或者 文件不存在
        try:
            fin = open(self.fullName, "r", encoding='utf-8', errors="ignore")
            input_file = fin.read()
            fin.close()
        except:
            fin.close()
            return None  # 打开文件失败
        self.input_str = input_file.splitlines(False)
        self.max_line = len(self.input_str) - 1

    def getchar(self):  # 从整个文档中取出一个 char
        self.current_row += 1
        if self.current_row == len(self.input_str[self.current_line]):
            self.current_line += 1
            self.current_row = 0
            while True:
                #print(self.input_str)
                #print("*")
                if len(self.input_str[self.current_line]) != 0:
                    break
                self.current_line += 1
        if self.current_line == self.max_line:
            return 'SCANEOF'
        return self.input_str[self.current_line][self.current_row]

    def ungetchar(self):  # 往文档存回一个 char
        self.current_row = self.current_row - 1
        if self.current_row < 0:
            self.current_line = self.current_line - 1
            self.current_row = len(self.input_str[self.current_line]) - 1
        return self.input_str[self.current_line][self.current_row]

    def getFunctionNameInLine(self, strline):
        for i in range(0, len(strline)):
            if strline[i] == '(':
                break
        else:
            return None
        j = i - 1
        for i in range(j, -1, -1):
            if ord(strline[i]) > 127:  # 非 ASCII 码
                return None
            if strline[i].isalnum() == False and strline[i] != '_':  # 含有非函数名字符则停止
                str1 = strline[i + 1: j + 1]
                if str1 in KEYWORD_LIST_FUNC:  # 不是关键字
                    break
                else:  # 函数名
                    return str1
        return None

    def scanFunction(self):
        global g_allFuncList
        if self.current_line == self.max_line:
            return ('SCANEOF', self.max_line)

        str1 = self.input_str[self.current_line].strip()
        if len(str1) == 0:  # 空行
            self.current_line += 1
            self.current_row = -1
            return None
        if '(' not in str1:  # 没有 左括号
            self.current_line += 1
            self.current_row = -1
            return None
        # 本行出现(,记录行号
        lineOfLeft = self.current_line
        while (True):
            # 查找‘)’  -->  {
            current_char = self.getchar()
            if current_char == ')':  # 后面可能有注释 /**/  或者  //    跳过   ;还有=跳过
                while (True):
                    current_char = self.getchar()
                    if current_char == '{':  # 当前行中包含函数名，记录行号和获取函数名
                        str1 = self.getFunctionNameInLine(self.input_str[lineOfLeft])
                        if str1:
                            g_allFuncList.append(str1)
                            return (str1, lineOfLeft)
                        return None
                    elif current_char == '(':
                        lineOfLeft = self.current_line
                        continue
                    elif current_char == ';' or current_char == '=':  # 分号表示此处为函数调用，并非函数体跳过  =可能是函数指针数组
                        self.current_line += 1
                        self.current_row = -1
                        return None
                    elif current_char == '/':
                        next_char = self.getchar()
                        if next_char == '/':  # 单行注释跳过当前行，下面已经是下一行
                            self.current_line += 1
                            self.current_row = -1
                            next_char = self.getchar()  # 换行的第一个是 ｛ 认为是函数所在行
                            if next_char == '{':  # 行首是 { ,将字符存回去 ，回到当前的while开始处
                                self.ungetchar()
                                continue
                            elif next_char == 'SCANEOF':
                                return ('SCANEOF', 0)
                            else:
                                return None
                        elif current_char == '*':  # 块注释  /**/
                            next_char = self.getchar()
                            while True:
                                if next_char == '*':
                                    end_char = self.getchar()
                                    if end_char == '/':
                                        break
                                    if end_char == 'SCANEOF':
                                        return ('SCANEOF', 0)
                                elif next_char == 'SCANEOF':
                                    return ('SCANEOF', 0)
                                next_char = self.getchar()

    def lexer_analysis(self):
        [dirname, filename] = os.path.split(self.fullName)
        #print(self.fullName)
        funcDict = {}  # 本字典 属于 子自典，key = 函数名,value = 行号
        # 分析c文件，一直到文档结束
        while True:
            r = self.scanFunction()
            if r is not None:
                if r[0] == 'SCANEOF':  # 文档结尾，结束查找
                    break
                funcDict.setdefault(r[0], r[1])  # 查找到函数名，记录所在行号
        return (filename, funcDict)














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
        self.setColor(QColor("#191970"), QsciLexerCPP.PreProcessor)  # 预编译语句的颜色
        self.setColor(QColor("#be07ff"), QsciLexerCPP.Operator)
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

    def __init__(self, filename='', wins=None, parent=None,tree =None):
        global g_allFuncList
        super(QsciScintilla, self).__init__(parent)
        self.tree = tree
        #print(tree)
        self.win = wins
        self.jumpName = ''
        self.list_line = []
        self.Font = QFont()
        self.filename = filename
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
        #print("sciisodk")

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

        #self.filename = filename
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
        #self.customContextMenuRequested.connect(self.RightMenu)
        # self.win.setWidget(self)


    def RightMenu(self):
        line_num, index = self.getCursorPosition()
        text = self.text()
        # 0.获取光标所在行的全部字符
        str1 = text.splitlines(False)[line_num]
        if len(str1) != 0:
            # 0.1 如果字符串有 ‘#in’ ，那么应该包含文件名
            if '#in' in str1:
                self.jumpName = self.win.getIncludeFile(str1)
            # 0.2 如果含有 字符 (  ,那么应该有函数名
            elif '(' in str1:
                self.jumpName = self.win.getFuncNameInLine(str1)
        # 1.Jump to
        self.popMenu = QMenu()
        Jump2Function = QAction('Jump to ' + self.jumpName, self)
        self.popMenu.addAction(Jump2Function)
        Jump2Function.triggered.connect(self.do_Jump2Function)
        # setEnabled   isRedoAvailable  isUndoAvailable
        # 2.undo
        undoAction = QAction('Undo', self)
        undoAction.triggered.connect(self.undo)
        undoAction.setEnabled(self.isUndoAvailable())
        self.popMenu.addAction(undoAction)
        # 3.redo
        redoAction = QAction('Redo', self)
        redoAction.triggered.connect(self.redo)
        redoAction.setEnabled(self.isRedoAvailable())
        self.popMenu.addAction(redoAction)
        # 4.copy
        copyAction = QAction('Copy', self)
        copyAction.triggered.connect(self.copy)
        self.popMenu.addAction(copyAction)
        # 5.cut
        cutAction = QAction('Cut', self)
        cutAction.triggered.connect(self.cut)
        self.popMenu.addAction(cutAction)
        # 6.paste
        pasteAction = QAction('Paste', self)
        pasteAction.triggered.connect(self.paste)
        self.popMenu.addAction(pasteAction)
        # 7.在鼠标位置显示右菜单
        self.popMenu.exec_(QCursor.pos())


    def textChangedAction(self):
        line, index = self.getCursorPosition()  # 获取当前光标所在行
        #self.win.from_sci(self.win,1)


        if not line ==0:
            self.win.dis_enable(1)
            handle_01 = self.markerAdd(line, 0)  # 添加改动标记
            #print(handle_01)
            self.list_line.append(handle_01)
            #print(self.list_line)

    def saveas(self):
        filename, _buff = QFileDialog.getSaveFileName(self, '另存为', './', 'All (*.*)')
        if filename:
            self.filename = filename
            i = self.win.tabWidget.currentIndex()
            #得到当前的index
            self.win.tabWidget.setTabText(i,QFileInfo(self.filename).fileName())

            #bText(i,QFileInfo(self.filename).fileName())#存完改变名字
            return self.save()


    def save(self):
        if self.filename == None:
            self.saveas()
        else:
            #write_text = self.text()

            #save_name = self.win.file_path_dict[self.filename]
            try:
                #print(save_name)
                with open(self.filename,"w+",encoding='utf-8') as w_file:
                    w_file.write(self.text())
                #清除改动标记
                for line in self.list_line:
                    self.markerDeleteHandle(line)
                self.list_line.clear()
            except:
                QMessageBox.warning(self, "EVE IDE -- SAVE Error",
                                    "Failed to save {0}".format(QFileInfo(self.filename).fileName()))

    def save_when_close_tab(self):
        if self.filename == None:
            reply = QMessageBox.question(self,
                                         "Eve IDE",
                                         "未命名文件无法自动保存，是否保存？",
                                         QMessageBox.Yes | QMessageBox.No
                                         )
            if reply == QMessageBox.No:
                pass
            elif reply == QMessageBox.Yes:
                self.saveas()



        else:
            # write_text = self.text()

            # save_name = self.win.file_path_dict[self.filename]
            try:
                # print(save_name)
                with open(self.filename, "w+", encoding='utf-8') as w_file:
                    w_file.write(self.text())
                # 清除改动标记
                for line in self.list_line:
                    self.markerDeleteHandle(line)
                self.list_line.clear()
            except:
                QMessageBox.warning(self, "EVE IDE -- SAVE Error",
                                    "Failed to save {0}".format(QFileInfo(self.filename).fileName()))


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
        # self.dock_serial.setMinimumSize
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
        #self.set_tree()
        time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        st_first = 'Open at ' + time_now + " --Eve ide"
        self.text_browser.setPlainText(st_first)
        #self.text_browser.clear()
        #self.text_browser.setPlainText(st_first)
        #self.text_browser.append("hello")

class logic_main(main_win):
    Jump2Func_Signal = pyqtSignal(str)
    Jump2IncludeFile_Signal = pyqtSignal(str)
    def __init__(self):
        super(logic_main, self).__init__()
        self.st_process=0
        self.project_path = read_line(configure_file, 4)[:-1]
        #print(self.project_path)
        self.project_path = self.project_path.split(';')#propath
        print(self.project_path)
        l = []
        for path in self.project_path:#判断路径是否存在

            if os.path.exists(path):
                l.append(path)

                #print(path + "not")


            else:
                #print(path+"not")
                self.project_path.remove(path)
            '''
                QMessageBox.warning(self, "EVE IDE -- OPEN Error",
                                    "Failed to open {0}".format(path))
            '''
        #print("8"*8)
        #print(self.project_path)
        self.project_path = l
        self.path_name_list = []#propath名字
        self.project_path_dict = {}
        self.file_fuction_dict = {}#完整路径
        self.function_list  = []#方便分辨是否为function
        self.opened_file_list = []#store the opened files已经打开的
        self.tree_tab_connection_dict = {}#用于每次刷新tree的时候连接到相应的
        self.all_index =0


        for i_p in range(len(self.project_path)):
            full_path = self.project_path[i_p]
            path_name = self.project_path[i_p].split('/')[-1]
            self.path_name_list.append(path_name)

            self.project_path_dict.setdefault(path_name,full_path)

        #print(self.project_path_dict)
        #print("this is project path")

        self.list_of_files_with_path = []  # 完整名称
        self.list_of_files = []  # 无路径
        self.file_path_dict = {}
        #self.list_of_projects = []
        self.project_file_path_dict = {}

        #self.dis_enable(1)
        self.file_list(self.project_path, self.list_of_files_with_path, self.list_of_files,0)  # 得到list 包含了完整路径和仅有名字
        #最后一个参数表示将放入list
        self.set_tree()
        self.trigger_connection()  # 信号与槽连接
        self.view_dock_closeEvent()  # 重写dock关闭函数
        # SciTextEdit()

    def dis_enable(self,state):
        #print(self)
        #print(str(state)+"this is state")
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
        QApplication.processEvents()

        #self.action_save.setEabled(state)

    # self.file_list(self.project_path,self.list_of_files)
    def file_list(self, paths, list_name, li,state ):  # 传入存储的list

        if state == 0:
            i = 0
            for path in paths:
                print(i)
                i+=1
                #print(i)
                #print(path[i])
                #print(path)
                try:
                    for file in os.listdir(path):


                        file_path = os.path.join(path, file)

                        if os.path.isdir(file_path):
                            self.file_list(file_path, list_name, li,1)
                        else:
                            list_name.append(file_path)
                            li.append(file)
                            self.file_path_dict.setdefault(file, file_path)
                except:
                    paths.remove(path)
                    QMessageBox.warning(self, "EVE IDE -- OPEN Error",
                                        "Failed to open {0}".format(path))

                    continue
                #print(self.file_path_dict)
                # return list_name
                path = path.split('/')[-1]
                self.project_file_path_dict.setdefault(path,self.file_path_dict)

                self.file_path_dict = {}
            #print(self.project_file_path_dict)
            #print("this+reagasdg")
        else:
            for file in os.listdir(paths):
                file_path = os.path.join(paths, file)
                if os.path.isdir(file_path):#如果发现又是文件夹

                    #这个地方阔以加入成pro
                    self.file_list(file_path, list_name, li, 1)
                else:
                    list_name.append(file_path)
                    li.append(file)
                    self.file_path_dict.setdefault(file, file_path)

                    #print(self.file_path_dict)

    def view_dock_closeEvent(self):  # 当dock关闭时触发
        self.dockWidget_tree.closeEvent = self.dock_tree_close
        self.dockBuilt.closeEvent = self.dockBuilt_close

    def set_tree(self):
        self.tree.clear()
        #path = read_line(configure_file, 1)[:-1]
        for path in self.project_path:
            #print("+" * 10 + path)
            dirs = file_name(path)
            #print(dirs)
            fileInfo = QFileInfo(path)
            fileIcon = QFileIconProvider()
            icon = QIcon(fileIcon.icon(fileInfo))
            root = QTreeWidgetItem(self.tree)
            root.setText(0, path.split('/')[-1])
            root.setIcon(0, QIcon(icon))
            self.CreateTree(dirs, root, path)
            #self.tree.expandAll()#全部展开
            # self.setCentralWidget(self.tree)
            # self.tree.clicked.connect(self.onTreeClicked)
            QApplication.processEvents()

    def CreateTree(self, dirs, root, path):

        for i in dirs:
            path_new = path + '/' + i

            if os.path.isdir(path_new):
                #print('this is path'+i+'ok:'+path_new)

                fileInfo = QFileInfo(path_new)
                fileIcon = QFileIconProvider()
                icon = QIcon(fileIcon.icon(fileInfo))
                child = QTreeWidgetItem(root)
                child.setText(0, i)
                child.setIcon(0, QIcon(icon))
                dirs_new = file_name(path_new)
                self.CreateTree(dirs_new, child, path_new)
            else:
                #print(path_new+"okkkk")

                fileInfo = QFileInfo(path_new)


                fileIcon = QFileIconProvider()
                icon = QIcon(fileIcon.icon(fileInfo))
                child = QTreeWidgetItem(root)
                child.setExpanded(True)
                child.setText(0, i)
                child.setIcon(0, QIcon(icon))
                #print(self.tree_tab_connection_dict)
                if path_new in self.tree_tab_connection_dict:
                    textEdit = self.tree_tab_connection_dict[path_new]
                    textEdit.tree = child
                    print("connected")
                #print(new_project)
                try:
                    c_getfunc = lexer_c_getfunc(path_new)
                    _fname, _dict = c_getfunc.lexer_analysis()
                    _path = path.split('/')[-1]
                    #fname = self.project_file_path_dict[_path][_fname]
                    #print(fname)
                    #print("*")
                    self.file_fuction_dict.setdefault(path_new, _dict)
                    funcs = list(_dict.keys())
                    #print(self.file_fuction_dict)
                    for func in funcs:
                        self.function_list.append(func)
                        #print(self.function_list)
                        subsubchild = QTreeWidgetItem(child)
                        subsubchild.setText(0, func)
                        subsubchild.setIcon(0, QIcon("./fuc.ico"))

                except:
                    pass


    '''
                    c_getfunc = lexer_c_getfunc(path_new)
                    _fname, _dict = c_getfunc.lexer_analysis()
                    _path = path.split('/')[-1]
                    _fname = self.project_file_path_dict[_path][_fname]
                    self.file_fuction_dict.setdefault(_fname, _dict)


                    funcs = list(_dict.keys())
                    for di in funcs:
                        self.function_list.append(di)
                    print(self.function_list)
                    #print(self.file_fuction_dict)
                    for func in funcs:
                        subsubchild = QTreeWidgetItem(child)
                        subsubchild.setText(0, func)
                        subsubchild.setIcon(0, QIcon("./fuc.ico"))
    '''




    def trigger_connection(self):#设置触发
        self.menuEdit.triggered[QAction].connect(self.do_edit_menu)
        # self.actionHeaven.clicked.connect(lambda : self.change_style(1))
        # self.actionHell.clicked.connect(lambda: self.change_style(0))
        self.menuFile.triggered[QAction].connect(self.do_file_menu)
        self.menuActions.triggered[QAction].connect(self.do_action_menu)
        self.action_project_files.triggered.connect(partial(self.view_triggered, "project_files"))
        self.actionBuild_output.triggered.connect(partial(self.view_triggered, "Build_output"))
        self.actionWindows.triggered.connect(app.slot_setStyle)
        self.actionWindowsXP.triggered.connect(app.slot_setStyle)
        self.actionWindowsVista.triggered.connect(app.slot_setStyle)
        self.actionFusion.triggered.connect(app.slot_setStyle)#style选择
        self.actionDark.triggered.connect(app.slot_setStyle)#style选择
        self.tree.itemDoubleClicked.connect(self.onTreeClicked)  # 双击树某个child
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)  # 开放右键策略
        self.tree.customContextMenuRequested.connect(self.OnTreeRightMenuShow)  # 树的右键菜单
        self.actionchoose_workspace.triggered.connect(self.choose_workspace)#选择工作区域
        self.tabWidget.tabCloseRequested.connect(self.closeTab)#重写关闭tab
        self.actionserial_monitor.triggered.connect(self.open_serial_monitor)
        self.actionOpen_Project.triggered.connect(self.add_project)
        self.actionnew_empty_project.triggered.connect(lambda : self.new_project("empty"))
        self.actionnew_gd32vf103_project.triggered.connect(lambda : self.new_project("gd32vf103"))
        self.actionnew_prv332_project.triggered.connect(lambda:self.new_project("prv332"))
        #print("triggerok")
        self.Jump2Func_Signal[str].connect(self.do_Jump2Function)  # 右键跳转到函数
        self.Jump2IncludeFile_Signal[str].connect(self.do_Jump2IncludeFile)  # 右键跳转到包含文件
        self.tabWidget.currentChanged.connect(self.change_tab)
        #sys.stdout = EmittingStream(textWritten=self.outputWritten)
        #sys.stderr = EmittingStream(textWritten=self.outputWritten)

    def outputWritten(self):
        cursor = self.text_browser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.text_browser.setTextCursor(cursor)
        self.text_browser.ensureCursorVisible()







    def change_tab(self,t):
        textEdit = self.tabWidget.currentWidget()  # 获取当前的类
        if textEdit and textEdit.tree:
            if textEdit.tree.text(0) in self.function_list:
                textEdit.tree = textEdit.tree.parent()
            #brush_red = QBrush(Qt.red)
            #brush = QBrush(Qt.color0)
            #textEdit.tree.setBackground(0, brush)
            self.tree.setCurrentItem(textEdit.tree)
            #self.treeWidget.setCurrentItem(item)



    def do_Jump2Function(self,str1):
        pass

    def do_Jump2IncludeFile(self,str1):
        pass

    def new_project(self,which):

        new_pro.show()  # 打开选择窗口
        new_pro.pushButton.clicked.connect(lambda: self.create_new_project(which))


    def create_new_project(self,which):

        new_pro_name = read_line(configure_file,1)[:-1]+"/"+new_pro.lineEdit.text()
        project_main_path = new_pro_name+'/main.c'
        project_source_path = new_pro_name+'/source'
        project_include_path = new_pro_name +'/include'

        #取得路径

        #try:
        create_act = move_source(new_pro_name)
        #os.mkdir(new_pro_name)
        full_path = new_pro_name
        path_name = new_pro.lineEdit.text()
        if full_path not in self.project_path:
            self.path_name_list.append(path_name)

            self.project_path_dict.setdefault(path_name, full_path)
            self.project_path.append(full_path)

            if which == 'empty':
                if not os.path.exists(new_pro_name):
                    os.mkdir(new_pro_name)
                    create_act.create_empty()




            if which == 'gd32vf103':
                create_act.create_with_source()


            if which == 'prv332':
                if not os.path.exists(new_pro_name):
                    os.mkdir(new_pro_name)
                    create_act.create_with_main()

            #print(self.project_path)
            self.file_list(self.project_path, self.list_of_files_with_path, self.list_of_files,
                           0)  # 得到list 包含了完整路径和仅有名字
            self.set_tree()

            '''
            except:
                QMessageBox.warning(self, "EVE IDE ",
                                    "Failed to create {0}".format(new_pro.lineEdit.text()))
    
    
            '''
        new_pro.close()


    def add_project(self):
        directory1 = QFileDialog.getExistingDirectory(self,
                                                      "选取文件夹",
                                                      "./")
        if directory1:
            full_path =directory1
            path_name = directory1.split('/')[-1]
            self.path_name_list.append(path_name)

            self.project_path_dict.setdefault(path_name, full_path)
            self.project_path.append(directory1)
            self.file_list(self.project_path, self.list_of_files_with_path, self.list_of_files,0)  # 得到list 包含了完整路径和仅有名字


            #print(self.project_path)
            self.set_tree()


    def open_serial_monitor(self):

        #print("oprn_serial_monitor")
        serial_monitor.show()



    def closeTab(self,tab_index):
        #print(t)
        #self.file_save()
        self.tabWidget.setCurrentIndex(tab_index)#获取关闭的标签的index
        current_tab = self.tabWidget.currentWidget()
        fname = current_tab.filename
        self.tree_tab_connection_dict.pop(fname)
        #print(name.filename)
        self.save_when_close_tab()
        self.tabWidget.removeTab(tab_index)
        self.all_index-=1
        #self.opened_file_list.remove(name.filename)
        '''
        i = self.tabWidget.currentIndex()
        self.file_save()
        self.tabWidget.removeTab(i)
        '''
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
        try:
            #print("右键")
            item = self.tree.currentItem()  # 获取鼠标所在的树状列表的项
            #print(item.text(0))
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
                if item.text(0) in self.path_name_list:
                    delete_project = QAction("Delete the project",self)
                    self.tree.popMenu.addAction(delete_project)
                    delete_project.triggered.connect(lambda :self.delete_project(item.text(0)))
                addFile2Proj = QAction("Refresh", self)

                self.tree.popMenu.addAction(addFile2Proj)
                addFile2Proj.triggered.connect(self.refresh_treearea)
            self.tree.popMenu.exec_(QCursor.pos())  # 在鼠标位置显示
        except:
            pass

    def delete_project(self,name_str):
        reply = QMessageBox.question(self, '警告', '你将从工程中移除该工程\n你确认要删除吗？',
                                     QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            #print(self.path_name_list[0])
            #print(name_str)

            self.path_name_list.remove(name_str)
            #print(self.path_name_list[name_str])
            self.project_path.remove(self.project_path_dict[name_str])
            del self.project_path_dict[name_str]
            self.set_tree()



    def refresh_treearea(self):
        self.set_tree()

    def do_delectFile4Proj(self):
        reply = QMessageBox.question(self, '警告', '你将彻底删除该文件\n你确认要删除吗？',
                                     QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:

            item = self.tree.currentItem()
            it = item.text(0)
            pa = item.parent()
            while (1):
                if pa.text(0):
                    if pa.text(0) in self.project_file_path_dict.keys():
                        filepath = self.project_file_path_dict[pa.text(0)][it]
                        break
                    else:
                        pa = pa.parent()
                else:
                    break

            # 2.从文件列表中删除
            self.project_file_path_dict[pa.text(0)].pop(it)
            self.list_of_files_with_path.remove(filepath)
            os.remove(filepath)
            '''
            w_d = self.file_path_dict[item]
            self.file_path_dict.pop(item)
            os.remove(w_d)
            self.list_of_files.remove(item)
            self.list_of_files_with_path.remove((w_d))
            '''

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

    def onTreeClicked(self, which):#树列表被双击
        #if which:
        #    which.setExpanded(False)#双击后不折叠
        #print(which)
        #q = item.parent()
        #print(q.text(0))
        item = self.tree.currentItem()
        #在这里which和item是同一个子类


        #item.setExpanded(True)

        #print(str(item)+"is t")
        if '.' in item.text(0):
            item.setExpanded(False)
            it = item.text(0)
            pa = item.parent()
            while(1):
                if pa.text(0):
                    if pa.text(0) in self.project_file_path_dict.keys():
                        filepath = self.project_file_path_dict[pa.text(0)][it]
                        break
                    else:
                        pa = pa.parent()
                else:
                    break
            self.open_qsci(filepath,item)
            #print("key=%s " % (item.text(0)))
        elif item.text(0) in self.function_list :
            #print("yes")
            p = item.parent()
            if p:
                p.text(0)
                pa = p.parent()
                while (1):
                    if pa.text(0):
                        if pa.text(0) in self.project_file_path_dict.keys():
                            filepath = self.project_file_path_dict[pa.text(0)][p.text(0)]
                            break
                        else:
                            pa = pa.parent()
                    else:
                        break
                self.open_qsci(filepath,item)
                textEdit = self.tabWidget.currentWidget()
                filepath=filepath.replace('\\','/')
                textEdit.setCursorPosition(self.file_fuction_dict[filepath][item.text(0)],0)
                textEdit.setCaretLineBackgroundColor(Qt.lightGray)  # 光标所在行显示灰色
                textEdit.setFocus()







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
    def open_qsci(self,fname,which_tree=None):
        #打开文件工作区

        if fname =='':
            lm = self
            self.editor = SciTextEdit(filename = None,wins = lm,parent=self.tabWidget,tree = which_tree)
            self.tabWidget.addTab(self.editor,"Unnamed")
            self.editor.setText("")
            self.tabWidget.setCurrentWidget(self.editor)
            self.all_index+=1



        else:
            fname=fname.replace('\\','/')
            #self.opened_file_list.append(fname)
            filename, extension = os.path.split(fname)
            if filename:

                q = 1
                now = self.tabWidget.currentWidget()
                if now == None:#如果当前编辑区无tab
                    try:

                        lm = self
                        self.editor = SciTextEdit(filename=fname, wins=lm, parent=self.tabWidget, tree=which_tree)

                        self.tabWidget.addTab(self.editor, extension)
                        # print(self.editor)
                        obj = open(fname, 'r+', encoding='utf-8')
                        self.editor.setText(obj.read())
                        self.tabWidget.setCurrentWidget(self.editor)
                        self.tree_tab_connection_dict.setdefault(fname,self.editor)
                        self.all_index+=1

                    except:
                        i = self.tabWidget.currentIndex()
                        self.tabWidget.removeTab(i)
                        QMessageBox.warning(self, "EVE IDE -- OPEN Error",
                                            "Failed to open {0}".format(extension))
                else:        #有tab、
                    #print("into tab")
                    nowindex = self.tabWidget.currentIndex()
                    print(nowindex)
                    #line, index = now.getCursorPosition()  # 获取当前光标所在行
                    i = 0

                    while (i <=self.all_index):#进入循环判断是否出现

                        self.tabWidget.setCurrentIndex(i)

                        winnow = self.tabWidget.currentWidget()
                        #print(winnow.filename)
                        #print(winnow.filename)
                        #print(fname)
                        if winnow.filename == fname:


                            q = 0
                            break
                        i+=1
                        #print(i)
                    if q:
                        try:

                            lm = self
                            self.editor = SciTextEdit(filename=fname,wins=lm,parent=self.tabWidget,tree =which_tree)

                            self.tabWidget.addTab(self.editor, extension)
                            #print(self.editor)
                            obj = open(fname, 'r+', encoding='utf-8')
                            self.editor.setText(obj.read())
                            self.tabWidget.setCurrentWidget(self.editor)
                            self.tree_tab_connection_dict.setdefault(fname, self.editor)

                            self.all_index+=1
                        except:
                            i = self.tabWidget.currentIndex()
                            self.tabWidget.removeTab(i)
                            QMessageBox.warning(self, "EVE IDE -- OPEN Error",
                                                "Failed to open {0}".format(extension))




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
    '''
    
    def build_output(self):
        while(1):
            if self.st_process:
                self.show_output(self.st_process)
                break
    def show_output(self,st):
        while 1:
            st_now = self.st_process
            if not st == st_now:
                self.text_browser.append(st)
                self.show_output(st)
                break

    '''

    def do_action_menu(self,which_action):
        print(which_action.text())
        text = which_action.text()
        textEdit = self.tabWidget.currentWidget()
        textEdit.save()
        current_tree = textEdit.tree

        pa = current_tree

        #pa = item.parent()
        i = 0
        while (1):
            if pa:
                if pa.text(0):
                    if pa.text(0) in self.path_name_list:
                        pro_p  = self.project_path_dict[pa.text(0)]
                        break
                    else:
                        pa = pa.parent()
                else:
                    break
        print(pro_p)



        try:
            auto_make = do_make(pro_p, 'nuclei', 'gd')
            auto_make.create_path_gd()
            if auto_make.state:
                auto_make.create_makefile_obj_source_gd()
                auto_make.create_sub_makefile_gd()
                #auto_make.do_make_gd()

            else:
                auto_make.create_sub_makefile_gd()
                #auto_make.do_make_gd()
            path = auto_make.path
            gcc_path = read_line(configure_file, 6)[:-1]
            # (gcc_path)
            cmd = "make all -C " + path
            # obj = subprocess.Popen("mkdir t3", shell=True, cwd='/tmp/')
            pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, cwd=gcc_path,
                                    stderr=subprocess.PIPE)
            #li_re = pipe.readlines()
            self.text_browser.clear()
            time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

            st_first = 'build at ' +time_now+" by Eve ide\n"
            self.text_browser.setPlainText(st_first)

            #th1 = threading.Thread(target=self.build_output)
            #th1.start()
            for i in iter(pipe.stdout.readline, 'b'):
                #i = str(i, encoding='utf-8')

                self.st_process = str(i, encoding='utf-8')
                self.text_browser.append(self.st_process)
                print(i)
                if not subprocess.Popen.poll(pipe) is None:
                    if i == b'':
                        break

            pipe.stdout.close()
            if pipe.stderr:
                for i in iter(pipe.stdout.readline, 'b'):
                    # i = str(i, encoding='utf-8')

                    self.st_process = str(i, encoding='utf-8')
                    self.text_browser.append(self.st_process)
                    print(i)
                    if not subprocess.Popen.poll(pipe) is None:
                        if i == b'':
                            break


        except:
            pass
        if text =='Simulate online':
            pass
        elif text =='Download':
            pass
        elif text =='Change into Hex':
            pass
        elif text == 'Change into COE':
            pass
        elif text == 'Change into Binary':
            pass
        elif text == 'Change into MIF':
            pass
        self.set_tree()



    def do_file_menu(self, action_of_file):
        #print(action_of_file.text() + "is triggered")
        if action_of_file.text() == 'Open':
            self.file_open(False)
            self.statusBar().showMessage("file opened", 5000)
        elif action_of_file.text() =='Save':
            print("do save")
            self.file_save()
        elif action_of_file.text() =='SaveAs':
            self.file_saveas()

        elif action_of_file.text() =="New":
            print("create new file")

            self.open_qsci('')
            self.statusBar().showMessage("new file created", 5000)
        elif action_of_file.text() == "SaveAll":
            print("save all")
            self.file_saveall()
    def file_saveall(self):
        pass
    def file_save(self):
        i = self.tabWidget.currentIndex()
        textEdit = self.tabWidget.currentWidget()#获取当前的类/即获得编辑区的类
        #print(textEdit)
        textEdit.save()
        #self.tabWidget.removeTab(i)

    def save_when_close_tab(self):
        i = self.tabWidget.currentIndex()
        textEdit = self.tabWidget.currentWidget()  # 获取当前的类/即获得编辑区的类
        # print(textEdit)
        textEdit.save_when_close_tab()



    def file_saveas(self):
        i = self.tabWidget.currentIndex()
        textEdit = self.tabWidget.currentWidget()  # 获取当前的类
        #print("txtx")
        #print(textEdit)
        textEdit.saveas()




    def do_edit_menu(self, action_of_edit):
        print(action_of_edit.text() + "is triggered")

    # def actionOpen(self):
    #   print("open_ok")

    def update_enable(self):
        pass

    def dockBuilt_close(self, p):
        #print(p)
        self.actionBuild_output.setChecked(0)

    def dock_tree_close(self, p):
        #print(p)
        print("dock_closed")
        self.action_project_files.setChecked(0)



    def file_open(self,name):
        if name:
            pass
        else:
            filename, _buff = QFileDialog.getOpenFileName(self, '另存为', './', 'All (*.*)')
            self.open_qsci(filename)


    def closeEvent(self, event):
        if not self.okToContinue():
            event.ignore()


    def okToContinue(self):

        reply = QMessageBox.question(self,
                        "Eve IDE",
                        "确定退出?\n确保已经保存你的文件",
                        QMessageBox.Yes|QMessageBox.No
                        )
        if reply == QMessageBox.No:
            return False
        elif reply == QMessageBox.Yes:
            pro_str =(';').join( self.project_path)
            #print(pro_str)
            write_line(configure_file,4,pro_str)
        return True




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
        #print(tmp)
        if tmp =="WindowsVista":
            tmp = 'windowsvista'
        if tmp in QStyleFactory.keys():#换主题
            #print(QStyleFactory.keys())
            #print('changed')
            app.setStyle(tmp)#用qt自带主题
            write_line(configure_file, 3, tmp)


        elif tmp == 'Dark':
            app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        write_line(configure_file, 3, tmp)



if __name__ == "__main__":
    style = read_line(configure_file, 3)[:-1]#读取配置中的style选择

    # print(style)
    show_it = decide_if_open_selection()
    # def open_select_window():


    app = Application(sys.argv)
    new_pro = new_project()
    select = select_work()
    # mainwin = main_win()
    mainwin = logic_main()

    serial_monitor = Pyqt5_Serial()
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



