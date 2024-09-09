# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDateEdit, QDialog,
    QDialogButtonBox, QFrame, QLabel, QSizePolicy,
    QTextEdit, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(460, 480)
        icon = QIcon(QIcon.fromTheme(u"face-smirk"))
        Dialog.setWindowIcon(icon)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(90, 440, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.frame_INFO = QFrame(Dialog)
        self.frame_INFO.setObjectName(u"frame_INFO")
        self.frame_INFO.setGeometry(QRect(40, 20, 381, 401))
        self.frame_INFO.setFrameShape(QFrame.StyledPanel)
        self.frame_INFO.setFrameShadow(QFrame.Raised)
        self.label_invoice_code_2 = QLabel(self.frame_INFO)
        self.label_invoice_code_2.setObjectName(u"label_invoice_code_2")
        self.label_invoice_code_2.setGeometry(QRect(20, 30, 81, 21))
        self.label_invoice_code_2.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";")
        self.label_invoice_date = QLabel(self.frame_INFO)
        self.label_invoice_date.setObjectName(u"label_invoice_date")
        self.label_invoice_date.setGeometry(QRect(20, 70, 81, 21))
        self.label_invoice_date.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";")
        self.label_invoice_buyername = QLabel(self.frame_INFO)
        self.label_invoice_buyername.setObjectName(u"label_invoice_buyername")
        self.label_invoice_buyername.setGeometry(QRect(20, 110, 81, 21))
        self.label_invoice_buyername.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";")
        self.label_invoice_buyercode = QLabel(self.frame_INFO)
        self.label_invoice_buyercode.setObjectName(u"label_invoice_buyercode")
        self.label_invoice_buyercode.setGeometry(QRect(20, 150, 81, 21))
        self.label_invoice_buyercode.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";")
        self.label_invoice_sellername = QLabel(self.frame_INFO)
        self.label_invoice_sellername.setObjectName(u"label_invoice_sellername")
        self.label_invoice_sellername.setGeometry(QRect(20, 190, 81, 21))
        self.label_invoice_sellername.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";")
        self.label_invoice_sellercode = QLabel(self.frame_INFO)
        self.label_invoice_sellercode.setObjectName(u"label_invoice_sellercode")
        self.label_invoice_sellercode.setGeometry(QRect(20, 230, 81, 21))
        self.label_invoice_sellercode.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";")
        self.label_invoice_totalprice = QLabel(self.frame_INFO)
        self.label_invoice_totalprice.setObjectName(u"label_invoice_totalprice")
        self.label_invoice_totalprice.setGeometry(QRect(20, 270, 81, 21))
        self.label_invoice_totalprice.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";")
        self.label_invoice_notes = QLabel(self.frame_INFO)
        self.label_invoice_notes.setObjectName(u"label_invoice_notes")
        self.label_invoice_notes.setGeometry(QRect(20, 310, 81, 21))
        self.label_invoice_notes.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";")
        self.label_Adding_2 = QLabel(self.frame_INFO)
        self.label_Adding_2.setObjectName(u"label_Adding_2")
        self.label_Adding_2.setGeometry(QRect(90, 0, 221, 31))
        self.label_Adding_2.setStyleSheet(u"font: 16pt \"Consolas\";")
        self.dateEdit = QDateEdit(self.frame_INFO)
        self.dateEdit.setObjectName(u"dateEdit")
        self.dateEdit.setGeometry(QRect(100, 70, 121, 31))
        self.dateEdit.setDateTime(QDateTime(QDate(2024, 8, 7), QTime(16, 0, 0)))
        self.dateEdit.setCalendarPopup(True)
        self.textEdit_code_add = QTextEdit(self.frame_INFO)
        self.textEdit_code_add.setObjectName(u"textEdit_code_add")
        self.textEdit_code_add.setGeometry(QRect(100, 30, 251, 31))
        self.textEdit__buyername_add = QTextEdit(self.frame_INFO)
        self.textEdit__buyername_add.setObjectName(u"textEdit__buyername_add")
        self.textEdit__buyername_add.setGeometry(QRect(100, 110, 251, 31))
        self.textEdit_buyercode_add = QTextEdit(self.frame_INFO)
        self.textEdit_buyercode_add.setObjectName(u"textEdit_buyercode_add")
        self.textEdit_buyercode_add.setGeometry(QRect(100, 150, 251, 31))
        self.textEdit_sellername_add = QTextEdit(self.frame_INFO)
        self.textEdit_sellername_add.setObjectName(u"textEdit_sellername_add")
        self.textEdit_sellername_add.setGeometry(QRect(100, 190, 251, 31))
        self.textEdit_sellercode_add = QTextEdit(self.frame_INFO)
        self.textEdit_sellercode_add.setObjectName(u"textEdit_sellercode_add")
        self.textEdit_sellercode_add.setGeometry(QRect(100, 230, 251, 31))
        self.textEdit_totalprice_add = QTextEdit(self.frame_INFO)
        self.textEdit_totalprice_add.setObjectName(u"textEdit_totalprice_add")
        self.textEdit_totalprice_add.setGeometry(QRect(100, 270, 251, 31))
        self.textEdit_note_add = QTextEdit(self.frame_INFO)
        self.textEdit_note_add.setObjectName(u"textEdit_note_add")
        self.textEdit_note_add.setGeometry(QRect(100, 310, 251, 81))

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Add New Invoice", None))
        self.label_invoice_code_2.setText(QCoreApplication.translate("Dialog", u"\u53d1\u7968\u4ee3\u7801\uff1a", None))
        self.label_invoice_date.setText(QCoreApplication.translate("Dialog", u"\u5f00\u7968\u65e5\u671f\uff1a", None))
        self.label_invoice_buyername.setText(QCoreApplication.translate("Dialog", u"\u8d2d\u65b9\u540d\u79f0\uff1a", None))
        self.label_invoice_buyercode.setText(QCoreApplication.translate("Dialog", u"\u8d2d\u65b9\u7f16\u53f7\uff1a", None))
        self.label_invoice_sellername.setText(QCoreApplication.translate("Dialog", u"\u9500\u65b9\u540d\u79f0\uff1a", None))
        self.label_invoice_sellercode.setText(QCoreApplication.translate("Dialog", u"\u9500\u65b9\u7f16\u53f7\uff1a", None))
        self.label_invoice_totalprice.setText(QCoreApplication.translate("Dialog", u"\u4ef7\u7a0e\u5408\u8ba1\uff1a", None))
        self.label_invoice_notes.setText(QCoreApplication.translate("Dialog", u"\u5907\u6ce8\uff1a", None))
        self.label_Adding_2.setText(QCoreApplication.translate("Dialog", u"Adding new Invoice", None))
    # retranslateUi

