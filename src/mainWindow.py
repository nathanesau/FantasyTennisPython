from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from urllib.request import urlopen, Request
import qrc_resources  # pyrcc5 resources.qrc -o qrc_resources.py
import os.path
import math
import copy

from bracket import *
from database import *
from loadBracketDialog import *
from convertHtmlDialog import *
from downloadDialog import *
from loadPredictionsDialog import *
from savePredictionsDialog import *
from drawParser import *
from data import *

data_dir = os.path.dirname(os.path.realpath(__file__)) + "/data/"
html_dir = os.path.dirname(os.path.realpath(__file__)) + "/html_data/"
custom_dir = os.path.dirname(os.path.realpath(__file__)) + "/custom_data/"


class MainWindow(QMainWindow):
    def setupActions(self):
        self.downloadBracketAction = QAction("Download Bracket (HTML)")
        self.downloadBracketAction.triggered.connect(self.onDownloadBracket)
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
        fileMenu.addAction(self.downloadBracketAction)
        fileMenu.addAction(self.convertHtmlToDbAction)
        fileMenu.addAction(self.loadAction)
        predMenu = self.menuBar().addMenu("Predictions")
        predMenu.addAction(self.resetPredAction)
        predMenu.addAction(self.savePredAction)
        predMenu.addAction(self.loadPredAction)

    def __init__(self, parent=None):
        super().__init__(parent)

        # create required folders
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        if not os.path.exists(html_dir):
            os.mkdir(html_dir)
        if not os.path.exists(custom_dir):
            os.mkdir(custom_dir)

        self.tournamentName = ""

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

    def onDownloadBracket(self):
        downloadArchive()

        download_options = getDownloadOptions()
        downloadDlg = DownloadDialog(download_options, "out.html")

        if not downloadDlg.exec():  # reject
            return
        
        # EXAMPLE: "https://www.atptour.com/en/scores/archive/cincinnati/422/2019/draws"
        key = list(download_options.keys())[downloadDlg.urlComboBox.currentIndex()]
        url = "https://www.atptour.com" + download_options[key]

        # example: out.html
        fname = html_dir + downloadDlg.fnameLE.text()

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        req = Request(url=url, headers=headers)
        html = urlopen(req).read()
        html_file = open(fname, "w")
        html_file.write(html.decode("utf-8"))
        html_file.close()
        
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Download complete")
        msgBox.setText("Download HTML bracket to html_data folder. Bracket can now be converted")
        msgBox.setWindowIcon(QIcon(":icon.png"))
        msgBox.exec()

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
        self.playerRowList = tennisData.playerRowList
        self.drawRowList = tennisData.drawRowList

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

        for i in range(len(tennisData.drawRowList)):
            drawRow = tennisData.drawRowList[i]
            drawPredictionsRow = drawRow
            if i < len(tennisData.drawPredictionsRowList):
                drawPredictionsRow = tennisData.drawPredictionsRowList[i]

            roundNum = drawRow[0]
            player1, player2 = drawRow[1], drawRow[2]
            player1Prediction, player2Prediction = drawPredictionsRow[1], drawPredictionsRow[2]

            if roundNum <= numRounds:
                seed1 = '0' if not player1 in seedDict else seedDict[player1]
                seed2 = '0' if not player2 in seedDict else seedDict[player2]
                country1 = "" if not player1 in countryDict else countryDict[player1]
                country2 = "" if not player2 in countryDict else countryDict[player2]
                d1 = PlayerNodeData(player1, seed1, country1)
                d2 = PlayerNodeData(player2, seed2, country2)

                seed1Prediction = '0' if not player1Prediction in seedDict else seedDict[
                    player1Prediction]
                seed2Prediction = '0' if not player2Prediction in seedDict else seedDict[
                    player2Prediction]
                country1Prediction = "" if not player1Prediction in countryDict else countryDict[
                    player1Prediction]
                country2Prediction = "" if not player2Prediction in countryDict else countryDict[
                    player2Prediction]
                d1Prediction = PlayerNodeData(
                    player1Prediction, seed1Prediction, country1Prediction)
                d2Prediction = PlayerNodeData(
                    player2Prediction, seed2Prediction, country2Prediction)

                nodeData = BracketNodeData(d1, d2)
                nodeDataPrediction = BracketNodeData(d1Prediction, d2Prediction)
                node = BracketNode(nodeData, roundNum, self)
                node.playerOneNode.update(d1Prediction)
                node.playerTwoNode.update(d2Prediction)
                node.data.playerOneNodeData = d1Prediction
                node.data.playerTwoNodeData = d2Prediction
                bracketNodes[roundNum].append(node)

        self.roundBrackets = []
        self.roundBracketVisible = {}
        for key in bracketNodes.keys():
            self.roundBrackets.append(
                RoundBracket(bracketNodes[key], key, self))
            self.roundBracketVisible[key] = True

        self.bracket = Bracket(
            self.roundBrackets, self.roundBracketVisible, self)
        self.scrollArea.setWidget(self.bracket)

    def hideShowRoundBracket(self, roundNum):
        if self.roundBracketVisible[roundNum]:
            self.roundBracketVisible[roundNum] = False
        else:
            self.roundBracketVisible[roundNum] = True

        self.bracket = Bracket(
            self.roundBrackets, self.roundBracketVisible, self)
        self.scrollArea.setWidget(self.bracket)
        self.repaint()

    def onLoadBracket(self):
        loadBracketDlg = LoadBracketDialog()

        if not loadBracketDlg.exec():  # reject
            return

        tennisData = TennisData([], [], [])
        db = TennisDatabase()
        db_file = loadBracketDlg.fileComboBox.currentText()
        db.LoadDrawFromDb(data_dir + db_file, tennisData)
        self.showData(tennisData)

        self.tournamentName = db_file.replace(".db", "")
        self.setWindowTitle("Fantasy Tennis " + "(" + self.tournamentName + ")")

    # data: BracketNodeData which was modified
    # winner: PlayerNodeData which won the match
    def updateBracket(self, data, winner, opponent, currRoundNum):
        roundBrackets = self.bracket.roundBrackets  # [0]: round1, ...
        numRounds = len(roundBrackets)
        indexDict = {}  # indices to update for each round

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
            top = prev_index % 2 != 0  # top of bracket if prev_index is odd
            playerNode = bracketNode.playerOneNode if top else bracketNode.playerTwoNode
            bracketData = bracketNode.data.playerOneNodeData if top else bracketNode.data.playerTwoNodeData
            if playerNode.data.name != winner.name:
                needUpdate = playerNode.data.name == opponent.name or \
                    (playerNode.data.name == "unknown" and roundNum == currRoundNum+1)
                if needUpdate:  # update needed
                    playerNode.update(winner)
                    if top:
                        bracketNode.data.playerOneNodeData = winner
                    else:
                        bracketNode.data.playerTwoNodeData = winner

        self.bracket.repaint()

    def onResetPred(self):
        for roundBracket in self.bracket.roundBrackets:
            for bracketNode in roundBracket.bracketNodes:
                bracketNode.playerOneNode.resetData()
                bracketNode.playerTwoNode.resetData()

    def onSavePred(self):
        savePredictionsDlg = SavePredictionsDialog(self.tournamentName)

        if not savePredictionsDlg.exec():  # reject
            return

        db_file = savePredictionsDlg.fileNameLE.text()
        db_file += ".db"

        drawPredictionsRowList = []  # note: doesn't include winner of final round

        for roundBracket in self.bracket.roundBrackets:
            roundNum = roundBracket.roundNum
            for bracketNode in roundBracket.bracketNodes:
                playerOneName = bracketNode.data.playerOneNodeData.name
                playerTwoName = bracketNode.data.playerTwoNodeData.name
                drawPredictionsRowList.append(
                    [roundNum, playerOneName, playerTwoName])

        tennisData = TennisData(
            self.drawRowList, drawPredictionsRowList, self.playerRowList)
        db = TennisDatabase()
        db.SaveDrawToDb(custom_dir + db_file, tennisData)

        self.tournamentName = db_file.replace(".db", "")
        self.setWindowTitle("Fantasy Tennis " + "(" + self.tournamentName + ")")

    def onLoadPred(self):
        loadPredictionsDlg = LoadPredictionsDialog()

        if not loadPredictionsDlg.exec():  # reject
            return

        tennisData = TennisData([], [], [])
        db = TennisDatabase()
        db_file = loadPredictionsDlg.fileComboBox.currentText()
        db.LoadDrawFromDb(custom_dir + db_file, tennisData)
        self.showData(tennisData)

        self.tournamentName = db_file.replace(".db", "")
        self.setWindowTitle("Fantasy Tennis " + "(" + self.tournamentName + ")")
