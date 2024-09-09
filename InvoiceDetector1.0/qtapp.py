# 使用例子
import sys
from PyQt5 import QtWidgets
from qt_material import apply_stylesheet

def on_button_click():
    QtWidgets.QMessageBox.information(window, "信息", "按钮被点击了！")


# create the application and the main window
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()

window.setWindowTitle('Invoice Detector 2.0')
window.setGeometry(100, 100, 800, 600)
central_widget = QtWidgets.QWidget()
window.setCentralWidget(central_widget)
layout = QtWidgets.QVBoxLayout()
central_widget.setLayout(layout)

# 创建一个按钮并添加到布局中
button = QtWidgets.QPushButton('点击我')
layout.addWidget(button)
button.clicked.connect(on_button_click)
# setup stylesheet
apply_stylesheet(app, theme='light_lightgreen.xml')

# run
window.show()
app.exec_()