import sys
from PyQt6 import QtWidgets, QtCore, QtGui, QtWebEngineWidgets

# 定义 HelpWindow 类
class HelpWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('帮助文档')
        self.resize(1200, 900)
        widget = QtWebEngineWidgets.QWebEngineView(self)
        widget.move(0, 0)
        widget.resize(1200, 900)
        widget.load(QtCore.QUrl("https://github.com/Racheus/Robotics-Caprice/tree/master"))

# 创建主窗口类
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.help_window = None  # 初始化为 None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("主窗口")
        self.resize(800, 600)

        # 创建菜单栏
        menubar = self.menuBar()

        # 添加菜单
        help_menu = menubar.addMenu('帮助')

        # 创建菜单项并连接到 open_help_web 函数
        help_action = QtGui.QAction('打开帮助文档', self)
        help_action.triggered.connect(self.open_help_web)
        help_menu.addAction(help_action)

    def open_help_web(self):
        # 只有在帮助文档窗口不存在时才创建一个新的
        if self.help_window is None or not self.help_window.isVisible():
            self.help_window = HelpWindow()
            self.help_window.show()

# 程序的入口
def main():
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
