# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
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
    QLabel, QLineEdit, QSizePolicy, QWidget)

class Ui_Login(object):
    def setupUi(self, Login):
        if not Login.objectName():
            Login.setObjectName(u"Login")
        Login.resize(390, 247)
        self.buttonBox = QDialogButtonBox(Login)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(20, 190, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.label = QLabel(Login)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(40, 100, 71, 31))
        self.label.setStyleSheet(u"font: 11pt \"\u9ed1\u4f53\";")
        self.label_pswd = QLabel(Login)
        self.label_pswd.setObjectName(u"label_pswd")
        self.label_pswd.setGeometry(QRect(40, 140, 71, 31))
        self.label_pswd.setStyleSheet(u"font: 11pt \"\u9ed1\u4f53\";")
        self.lineEdit_account = QLineEdit(Login)
        self.lineEdit_account.setObjectName(u"lineEdit_account")
        self.lineEdit_account.setGeometry(QRect(120, 100, 231, 31))
        self.lineEdit_password = QLineEdit(Login)
        self.lineEdit_password.setObjectName(u"lineEdit_password")
        self.lineEdit_password.setGeometry(QRect(120, 140, 231, 31))
        self.label_2 = QLabel(Login)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(170, 30, 81, 41))
        self.label_2.setStyleSheet(u"font: 700 18pt \"\u5fae\u8f6f\u96c5\u9ed1\";")
        self.label_pic = QLabel(Login)
        self.label_pic.setObjectName(u"label_pic")
        self.label_pic.setGeometry(QRect(80, 20, 71, 61))
        self.label_pic.setPixmap(QPixmap(u"\u6821\u6807-\u6821\u5fbd.png"))

        self.retranslateUi(Login)
        self.buttonBox.accepted.connect(Login.accept)
        self.buttonBox.rejected.connect(Login.reject)

        QMetaObject.connectSlotsByName(Login)
    # setupUi

    def retranslateUi(self, Login):
        Login.setWindowTitle(QCoreApplication.translate("Login", u"Login", None))
        self.label.setText(QCoreApplication.translate("Login", u"\u8d26\u6237\u540d\u79f0\uff1a", None))
        self.label_pswd.setText(QCoreApplication.translate("Login", u"\u5bc6    \u7801\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("Login", u"\u8bf7\u767b\u5f55", None))
        self.label_pic.setText("")
    # retranslateUi

