import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from mainWindow import *

if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    #mainWindow.setMaximumSize(800, 800)
    #mainWindow.setFixedSize(800, 800)

    #mainWindow.windowHandle().setFlags(Qt.FramelessWindowHint)
    #mainWindow.windowHandle().showFullScreen()

    mainWindow.show()

    app.exec()
