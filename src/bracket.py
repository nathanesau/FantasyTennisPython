from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import qrc_resources


class QRightClickButton(QPushButton):
    rightClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.rightClicked.emit()


class PlayerNode(QWidget):
    clicked = pyqtSignal()
    rightClicked = pyqtSignal()

    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.nameSeedLabel = QRightClickButton()
        if data.country.rfind('/') > 0:
            ico_file = data.country[data.country.rfind('/')+1:]
            self.nameSeedLabel.setIcon(QIcon(":"+ico_file))
        #self.nameSeedLabel.setIcon(QIcon(":icon.png"))
        if data.seed != '0':
            self.nameSeedLabel.setText(data.name + " " + "(" + str(data.seed) + ")")
        else:
            self.nameSeedLabel.setText(data.name)
        self.nameSeedLabel.clicked.connect(self.clicked.emit)
        self.nameSeedLabel.rightClicked.connect(self.rightClicked.emit)
        self.mainLayout = QHBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.addWidget(self.nameSeedLabel)
        self.setLayout(self.mainLayout)


class BracketNode(QWidget):
    def __init__(self, data, is_prediction, parent=None):
        super().__init__(parent)
        self.is_prediction = is_prediction

        self.playerOneNode = PlayerNode(data.playerOneNodeData)
        self.playerOneNode.clicked.connect(self.onNode1Clicked)
        self.playerOneNode.rightClicked.connect(self.onRightClicked)
        
        if self.is_prediction:
            self.playerOneNode.setStyleSheet("background-color: red")

        self.playerTwoNode = PlayerNode(data.playerTwoNodeData)
        self.playerTwoNode.clicked.connect(self.onNode2Clicked)
        self.playerTwoNode.rightClicked.connect(self.onRightClicked)

        if self.is_prediction:
            self.playerTwoNode.setStyleSheet("background-color: red")

        self.groupBoxLayout = QVBoxLayout()
        self.groupBoxLayout.setSpacing(0)
        self.groupBoxLayout.addStretch(1)
        self.groupBoxLayout.setAlignment(Qt.AlignBottom)
        self.groupBoxLayout.addWidget(self.playerOneNode)
        self.groupBoxLayout.addWidget(self.playerTwoNode)
        self.groupBoxLayout.addStretch(1)

        self.groupBox = QGroupBox()
        # score of match could go here
        #self.groupBox.setTitle("64 76(4)")
        self.groupBox.setLayout(self.groupBoxLayout)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.groupBox)
        
        self.setLayout(self.mainLayout)
    
    def onNode1Clicked(self):
        # updateBracket
        # redrawBracket
        pass

    def onNode2Clicked(self):
        # updateBracket
        # redrawBracket
        pass

    def onRightClicked(self):
        pass # can be used to show detailed match info (not implemented)


class RoundBracket(QWidget):
    def __init__(self, bracketNodeList, roundNum, parent=None):
        super().__init__(parent)

        self.bracketNodes = bracketNodeList
        
        self.title = QLabel()
        self.title.setText("Round " + str(roundNum))

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.addWidget(self.title)
        for bracketNode in self.bracketNodes:
            self.mainLayout.addWidget(bracketNode)

        self.setLayout(self.mainLayout)


class Bracket(QWidget):
    def __init__(self, roundBracketList, parent=None):
        super().__init__(parent)

        self.roundBrackets = roundBracketList

        self.mainLayout = QHBoxLayout()
        self.mainLayout.setSpacing(0)
        for roundBracket in self.roundBrackets:
            self.mainLayout.addWidget(roundBracket)

        self.setLayout(self.mainLayout)
