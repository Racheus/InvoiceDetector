# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'success.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QLabel, QSizePolicy, QWidget)

class Ui_Success(object):
    def setupUi(self, Success):
        if not Success.objectName():
            Success.setObjectName(u"Success")
        Success.resize(400, 146)
        self.buttonBox = QDialogButtonBox(Success)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 80, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.Errorlabel = QLabel(Success)
        self.Errorlabel.setObjectName(u"Errorlabel")
        self.Errorlabel.setGeometry(QRect(40, 30, 171, 31))
        self.Errorlabel.setStyleSheet(u"color: rgb(255, 0, 0);\n"
"font: 12pt \"\u9ed1\u4f53\";")

        self.retranslateUi(Success)
        self.buttonBox.accepted.connect(Success.accept)
        self.buttonBox.rejected.connect(Success.reject)

        QMetaObject.connectSlotsByName(Success)
    # setupUi

    def retranslateUi(self, Success):
        Success.setWindowTitle(QCoreApplication.translate("Success", u"Success\uff01", None))
        self.Errorlabel.setText(QCoreApplication.translate("Success", u"\u68c0\u6d4b\u6210\u529f\uff01\u65e0\u9057\u6f0f\u53d1\u7968\uff01", None))
    # retranslateUi

