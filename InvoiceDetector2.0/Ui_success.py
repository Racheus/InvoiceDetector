# Form implementation generated from reading ui file 'c:\Users\dell\Desktop\InvoiceDetector2.0\success.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Success(object):
    def setupUi(self, Success):
        Success.setObjectName("Success")
        Success.resize(400, 146)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=Success)
        self.buttonBox.setGeometry(QtCore.QRect(10, 80, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.Errorlabel = QtWidgets.QLabel(parent=Success)
        self.Errorlabel.setGeometry(QtCore.QRect(40, 30, 171, 31))
        self.Errorlabel.setStyleSheet("color: rgb(255, 0, 0);\n"
"font: 12pt \"黑体\";")
        self.Errorlabel.setObjectName("Errorlabel")

        self.retranslateUi(Success)
        self.buttonBox.accepted.connect(Success.accept) # type: ignore
        self.buttonBox.rejected.connect(Success.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Success)

    def retranslateUi(self, Success):
        _translate = QtCore.QCoreApplication.translate
        Success.setWindowTitle(_translate("Success", "Success！"))
        self.Errorlabel.setText(_translate("Success", "检测成功！无遗漏发票！"))
