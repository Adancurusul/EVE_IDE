from PyQt5.QtGui import QFont, QIcon, QColor
from PyQt5.Qsci import *
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
        font.setItalic(True)
        self.setFont(font, QsciLexerCPP.Comment)  # 注释的字体用斜体。
        self.setFont(font, 5)  # 默认的字体加粗。

        font = QFont(self.parent().Font)

