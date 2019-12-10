import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from widgets.mainwidgets import MainWrapper

def main():
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    wrapper = MainWrapper()
    mainWindow.setCentralWidget(wrapper)
    mainWindow.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()