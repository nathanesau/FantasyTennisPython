from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import qrc_resources  # pyrcc5 resources.qrc -o qrc_resources.py
import os.path
import math

from bracket import *
from database import *
from loadBracketDialog import *
from convertHtmlDialog import *
from loadPredictionsDialog import *
from drawParser import *
from data import *

data_dir = os.path.dirname(os.path.realpath(__file__)) + "/data/"
html_dir = os.path.dirname(os.path.realpath(__file__)) + "/html_data/"
custom_dir = os.path.dirname(os.path.realpath(__file__)) + "/custom_data/"


class MainWindow(QMainWindow):
    def setupActions(self):
        self.convertHtmlToDbAction = QAction("Convert HTML to DB")
        self.convertHtmlToDbAction.triggered.connect(self.onConvertHTMLToDB)
        self.loadAction = QAction("Load Bracket")
        self.loadAction.setShortcuts(QKeySequence.Open)
        self.loadAction.triggered.connect(self.onLoadBracket)
        self.resetPredAction = QAction("Reset Predictions")
        self.resetPredAction.triggered.connect(self.onResetPred)
        self.savePredAction = QAction("Save Predictions")
        self.savePredAction.triggered.connect(self.onSavePred)
        self.loadPredAction = QAction("Load Predictions")
        self.loadPredAction.triggered.connect(self.onLoadPred)

    def setupMenus(self):
        fileMenu = self.menuBar().addMenu("File")
        fileMenu.addAction(self.loadAction)
        fileMenu.addAction(self.convertHtmlToDbAction)
        predMenu = self.menuBar().addMenu("Predictions")
        predMenu.addAction(self.resetPredAction)
        predMenu.addAction(self.savePredAction)
        predMenu.addAction(self.loadPredAction)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupActions()
        self.setupMenus()
        self.scrollArea = QScrollArea()

        instructionLabel = QLabel()
        instructionLabel.setText("Load a bracket to get started...")
        self.scrollArea.setWidget(instructionLabel)
        self.scrollArea.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(self.scrollArea)
        self.setWindowTitle("Fantasy Tennis")
        self.setWindowIcon(QIcon(":icon.png"))
        self.resize(600, 600)

    def onConvertHTMLToDB(self):
        convertHTMLDlg = ConvertHTMLDialog()

        if not convertHTMLDlg.exec():  # reject
            return

        html_file = convertHTMLDlg.fileComboBox.currentText()
        db_file = html_file.replace(".html", ".db")
        html_to_db(html_dir + html_file, data_dir + db_file)

        msgBox = QMessageBox()
        msgBox.setWindowTitle("Convert HTML to DB finished")
        msgBox.setText("HTML file converted. The bracket can now be loaded")
        msgBox.setWindowIcon(QIcon(":icon.png"))
        msgBox.exec()

    def showData(self, tennisData):
        seedDict = {}
        countryDict = {}
        for row in tennisData.playerRowList:
            player, seed, country = row[0], row[1], row[2]
            seedDict[player] = seed
            countryDict[player] = country

        round1Rows = []
        for row in tennisData.drawRowList:
            roundNum = row[0]
            if roundNum == 1:
                round1Rows.append(row)

        drawSize = len(round1Rows)
        numRounds = int(math.log(drawSize)/math.log(2)) + 1

        bracketNodes = {}
        for roundNum in range(0, numRounds, 1):
            bracketNodes[roundNum+1] = []

        for row in tennisData.drawRowList:
            roundNum, player1, player2 = row[0], row[1], row[2]
            if roundNum <= numRounds:
                seed1 = '0' if not player1 in seedDict else seedDict[player1]
                seed2 = '0' if not player2 in seedDict else seedDict[player2]
                country1 = "" if not player1 in countryDict else countryDict[player1]
                country2 = "" if not player2 in countryDict else countryDict[player2]
                d1 = PlayerNodeData(player1, seed1, country1)
                d2 = PlayerNodeData(player2, seed2, country2)
                nodeData = BracketNodeData(d1, d2)
                node = BracketNode(nodeData, roundNum, False, self)
                bracketNodes[roundNum].append(node)

        roundBrackets = []
        for key in bracketNodes.keys():
            roundBrackets.append(RoundBracket(bracketNodes[key], key))

        self.bracket = Bracket(roundBrackets)
        self.scrollArea.setWidget(self.bracket)

    def onLoadBracket(self):
        loadBracketDlg = LoadBracketDialog()

        if not loadBracketDlg.exec():  # reject
            return

        tennisData = TennisData([], [])
        db = TennisDatabase()
        db_file = loadBracketDlg.fileComboBox.currentText()
        db.LoadFromDb(data_dir + db_file, tennisData)
        self.showData(tennisData)
        self.setWindowTitle("Fantasy Tennis " + "(" + db_file + ")")

    # data: BracketNodeData which was modified
    # winner: PlayerNodeData which won the match
    def updateBracket(self, data, winner, opponent, currRoundNum):
        roundBrackets = self.bracket.roundBrackets  # [0]: round1, ...
        numRounds = len(roundBrackets)
        indexDict = {} # indices to update for each round

        for roundNum in range(1, numRounds+1, 1):
            indexDict[roundNum] = {}

        currRoundBracket = roundBrackets[currRoundNum - 1]
        for i in range(len(currRoundBracket.bracketNodes)):
            bracketNode = currRoundBracket.bracketNodes[i]
            if bracketNode.data == data:
                indexDict[currRoundNum] = int(i + 1)
                break

        # calculate affected indices mathematically
        for roundNum in range(currRoundNum+1, numRounds+1, 1):
            x = indexDict[roundNum-1]
            y = x if x % 2 == 0 else x + 1
            indexDict[roundNum] = int(y / 2)

        for roundNum in range(currRoundNum+1, numRounds+1, 1):
            roundBracket = roundBrackets[roundNum-1]
            roundBracketNodes = roundBracket.bracketNodes
            index = indexDict[roundNum]
            prev_index = indexDict[roundNum-1]
            bracketNode = roundBracketNodes[index-1]
            top = prev_index % 2 != 0 # top of bracket if prev_index is odd
            playerNode = bracketNode.playerOneNode if top else bracketNode.playerTwoNode
            bracketData = bracketNode.data.playerOneNodeData if top else bracketNode.data.playerTwoNodeData
            if playerNode.data.name != winner.name: 
                if playerNode.data.name == opponent.name: # update needed
                    playerNode.update(winner, True)
                    if top:
                        bracketNode.data.playerOneNodeData = winner
                    else:
                        bracketNode.data.playerTwoNodeData = winner
                        
        self.bracket.repaint()

    def onResetPred(self):
        pass

    def onSavePred(self):
        pass

    def onLoadPred(self):
        loadPredictionsDlg = LoadPredictionsDialog()

        if not loadPredictionsDlg.exec():  # reject
            return

        x = 5  # todo
