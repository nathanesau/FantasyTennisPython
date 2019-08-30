from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import qrc_resources  # pyrcc5 resources.qrc -o qrc_resources.py
import os.path

from bracket import *
from database import *
from loadBracketDialog import *
from convertHtmlDialog import *
from drawParser import *

data_dir = os.path.dirname(os.path.realpath(__file__)) + "/data/"
html_dir = os.path.dirname(os.path.realpath(__file__)) + "/html_data/"

class PlayerNodeData:
    def __init__(self, name, seed, country):
        self.name = name
        self.seed = seed
        self.country = country

class BracketNodeData:
    def __init__(self, playerOneNodeData, playerTwoNodeData):
        self.playerOneNodeData = playerOneNodeData
        self.playerTwoNodeData = playerTwoNodeData

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

        #
        #node1Data = BracketNodeData(playerOneData, playerTwoData)
        #node1 = BracketNode(node1Data)
        #node2Data = BracketNodeData(playerThreeData, playerFourData)
        #node2 = BracketNode(node2Data)
        #node3Data = BracketNodeData(playerOneData, playerThreeData)
        #node3 = BracketNode(node3Data)
        #
        # temp code
        #node4Data = node1Data
        #node5Data = node1Data
        #node6Data = node1Data
        #node7Data = node1Data
        #node8Data = node1Data
        #node9Data = node1Data
        #
        #node4 = BracketNode(node4Data)
        #node5 = BracketNode(node5Data)
        #node6 = BracketNode(node6Data)
        #node7 = BracketNode(node7Data)
        #node8 = BracketNode(node8Data)
        #node9 = BracketNode(node9Data)
        #
        #round1Bracket = RoundBracket([node1, node2, node4, node5, node6, node7, node8, node9])
        #round2Bracket = RoundBracket([node3, node4, node5, node6])
        #round3Bracket = RoundBracket([node3, node4])
        #self.bracket = Bracket([round1Bracket, round2Bracket, round3Bracket])

        self.scrollArea = QScrollArea()
        #self.scrollArea.setWidget(self.bracket)

        self.setCentralWidget(self.scrollArea)
        self.setWindowTitle("Fantasy Tennis")
        self.setWindowIcon(QIcon(":icon.png"))
        self.resize(600, 600)

    def onConvertHTMLToDB(self):

        convertHTMLDlg = ConvertHTMLDialog()
        result = convertHTMLDlg.exec()

        html_to_db(html_dir + "wimbledon_draw.html", data_dir + "wimbledon_draw.db")

    def onLoadBracket(self):
        
        loadBracketDlg = LoadBracketDialog()
        result = loadBracketDlg.exec()

        tennisData = TennisData([], [])
        db = TennisDatabase()
        db.LoadFromDb(data_dir + "wimbledon_draw.db", tennisData)

        # fill tennisData.drawRowList (round 3 = 32, 4 = 16, 5 = 8, 6 = 4, 7 = 2, 8 = 1)
        #tennisData.drawRowList.extend([[3, "unknown", "unknown"] for i in range(32)]) # 3
        #tennisData.drawRowList.extend([[4, "unknown", "unknown"] for i in range(16)]) # 4
        #tennisData.drawRowList.extend([[5, "unknown", "unknown"] for i in range(8)]) # 5
        #tennisData.drawRowList.extend([[6, "unknown", "unknown"] for i in range(4)]) # 6 
        #tennisData.drawRowList.extend([[7, "unknown", "unknown"] for i in range(2)])# 7
        #tennisData.drawRowList.extend([[8, "unknown", "unknown"] for i in range(1)]) # 8

        seedDict = {}
        countryDict = {}
        for row in tennisData.playerRowList:
            player = row[0]
            seed = row[1]
            country = row[2]
            seedDict[player] = seed 
            countryDict[player] = country

        bracketNodes = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[]}
        for row in tennisData.drawRowList:
            round = row[0]
            player1 = row[1]
            player2 = row[2]
            seed1 = '0'
            seed2 = '0'
            country1 = ""
            country2 = ""
            if player1 in seedDict:
                seed1 = seedDict[player1]
            if player2 in seedDict:
                seed2 = seedDict[player2]
            if player1 in countryDict:
                country1 = countryDict[player1]
            if player2 in countryDict:
                country2 = countryDict[player2]
            nodeData = BracketNodeData(PlayerNodeData(player1, seed1, country1), PlayerNodeData(player2, seed2, country2))
            bracketNodes[round].append(BracketNode(nodeData, False))

        round1Bracket = RoundBracket(bracketNodes[1], 1)
        round2Bracket = RoundBracket(bracketNodes[2], 2)
        round3Bracket = RoundBracket(bracketNodes[3], 3)
        round4Bracket = RoundBracket(bracketNodes[4], 4)
        round5Bracket = RoundBracket(bracketNodes[5], 5)
        round6Bracket = RoundBracket(bracketNodes[6], 6)
        round7Bracket = RoundBracket(bracketNodes[7], 7)
        self.bracket = Bracket([round1Bracket, round2Bracket, round3Bracket, round4Bracket, round5Bracket, round6Bracket, round7Bracket])
        self.scrollArea.setWidget(self.bracket)
        
        self.setWindowTitle("Fantasy Tennis (usopen2019.db)")

    def onResetPred(self):
        x = 5

    def onSavePred(self):
        x = 10

    def onLoadPred(self):
        x = 12