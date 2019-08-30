from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import qrc_resources


class QRightClickButton(QPushButton):
    clicked = pyqtSignal()
    rightClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.rightClicked.emit()
        elif event.button() == Qt.LeftButton:
            self.clicked.emit()


class PlayerNode(QWidget):
    clicked = pyqtSignal()
    rightClicked = pyqtSignal()

    def update(self, data, isPrediction):
        self.data = data
        self.isPrediction = isPrediction
        
        if data.country.rfind('/') > 0:
            ico_file = data.country[data.country.rfind('/')+1:]
            self.nameSeedLabel.setIcon(QIcon(":"+ico_file))
        if data.seed != '0':
            text = data.name + " " + "(" + str(data.seed) + ")"
            self.nameSeedLabel.setText(text)
        else:
            self.nameSeedLabel.setText(data.name)

        if isPrediction:
            self.setStyleSheet("background-color: red")

    def __init__(self, data, isPrediction, parent=None):
        super().__init__(parent)

        self.nameSeedLabel = QRightClickButton()
        self.update(data, isPrediction)
        
        self.nameSeedLabel.clicked.connect(self.clicked.emit)
        self.nameSeedLabel.rightClicked.connect(self.rightClicked.emit)

        self.mainLayout = QHBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addWidget(self.nameSeedLabel)
        self.setLayout(self.mainLayout)


class BracketNode(QWidget):
    def __init__(self, data, roundNum, isPrediction, mainWindow, parent=None):
        super().__init__(parent)
        self.data = data
        self.roundNum = roundNum
        self.isPrediction = isPrediction
        self.mainWindow = mainWindow  # ref to mainWindow

        self.playerOneNode = PlayerNode(data.playerOneNodeData, self.isPrediction)
        self.playerOneNode.clicked.connect(self.onNode1Clicked)
        self.playerOneNode.rightClicked.connect(self.onRightClicked)

        self.playerTwoNode = PlayerNode(data.playerTwoNodeData, self.isPrediction)
        self.playerTwoNode.clicked.connect(self.onNode2Clicked)
        self.playerTwoNode.rightClicked.connect(self.onRightClicked)

        self.groupBoxLayout = QVBoxLayout()
        self.groupBoxLayout.setSpacing(0)
        self.groupBoxLayout.addStretch(1)
        self.groupBoxLayout.setAlignment(Qt.AlignBottom)
        self.groupBoxLayout.addWidget(self.playerOneNode)
        self.groupBoxLayout.addWidget(self.playerTwoNode)
        self.groupBoxLayout.setSizeConstraint(QLayout.SetMinimumSize);
        self.groupBoxLayout.addStretch(1)

        self.groupBox = QGroupBox()
        # score of match could go here
        #self.groupBox.setTitle("64 76(4)")
        self.groupBox.setLayout(self.groupBoxLayout)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.groupBox)

        self.setLayout(self.mainLayout)

    def onNode1Clicked(self):
        winner = self.data.playerOneNodeData
        opponent = self.data.playerTwoNodeData
        self.mainWindow.updateBracket(self.data, winner, opponent, self.roundNum)

    def onNode2Clicked(self):
        winner = self.data.playerTwoNodeData
        opponent = self.data.playerOneNodeData
        self.mainWindow.updateBracket(self.data, winner, opponent, self.roundNum)

    def onRightClicked(self):
        pass  # can be used to show detailed match info (not implemented)


class RoundBracket(QWidget):
    def __init__(self, bracketNodeList, roundNum, mainWindow, parent=None):
        super().__init__(parent)
        self.bracketNodes = bracketNodeList
        self.roundNum = roundNum
        self.mainWindow = mainWindow

        self.title = QRightClickButton()
        self.title.setText("Round " + str(roundNum))
        self.title.clicked.connect(self.onTitleClicked)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.addWidget(self.title)
        for bracketNode in self.bracketNodes:
            self.mainLayout.addWidget(bracketNode)
        self.mainLayout.setSizeConstraint(QLayout.SetMinimumSize);
        self.setLayout(self.mainLayout)

    def onTitleClicked(self):
        self.mainWindow.hideRoundBracket(self.roundNum)


class Bracket(QWidget):
    def __init__(self, roundBracketList, parent=None):
        super().__init__(parent)

        self.roundBrackets = roundBracketList

        self.mainLayout = QHBoxLayout()
        self.mainLayout.setSpacing(0)
        for roundBracket in self.roundBrackets:
            self.mainLayout.addWidget(roundBracket)

        self.mainLayout.setSizeConstraint(QLayout.SetMinimumSize);
        self.setLayout(self.mainLayout)
