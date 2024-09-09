# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'errorlist.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QPushButton,
    QSizePolicy, QTextBrowser, QWidget)

class Ui_ErrorList(object):
    def setupUi(self, ErrorList):
        if not ErrorList.objectName():
            ErrorList.setObjectName(u"ErrorList")
        ErrorList.resize(400, 330)
        self.Errorlabel = QLabel(ErrorList)
        self.Errorlabel.setObjectName(u"Errorlabel")
        self.Errorlabel.setGeometry(QRect(30, 20, 171, 31))
        self.Errorlabel.setStyleSheet(u"color: rgb(255, 0, 0);\n"
"font: 12pt \"\u9ed1\u4f53\";")
        self.textBrowser = QTextBrowser(ErrorList)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(30, 50, 351, 231))
        self.pushButton = QPushButton(ErrorList)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(150, 290, 121, 31))

        self.retranslateUi(ErrorList)

        QMetaObject.connectSlotsByName(ErrorList)
    # setupUi

    def retranslateUi(self, ErrorList):
        ErrorList.setWindowTitle(QCoreApplication.translate("ErrorList", u"ErrorList", None))
        self.Errorlabel.setText(QCoreApplication.translate("ErrorList", u"\u672a\u88ab\u68c0\u6d4b\u6210\u529f\u7684\u53d1\u7968\uff1a", None))
        self.pushButton.setText(QCoreApplication.translate("ErrorList", u"\u6211\u8981\u201c\u624b\u52a8\u5f55\u5165\u201d", None))
    # retranslateUi

