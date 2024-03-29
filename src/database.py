from PyQt5.QtSql import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from data import *


class TennisData:
    def __init__(self, drawRowList, drawPredictionsRowList, playerRowList):
        self.drawRowList = drawRowList
        self.drawPredictionsRowList = drawPredictionsRowList
        self.playerRowList = playerRowList


class TennisDatabase:
    def DatabaseConnect(self, dbName):
        driver = "QSQLITE"
        if QSqlDatabase.isDriverAvailable(driver):
            db = QSqlDatabase.addDatabase(driver)
            db.setDatabaseName(dbName)
            if not db.open():
                qWarning("DatabaseConnect - ERROR " + db.lastError().text())
        else:
            qWarning("DatabaseConnect - ERROR: no driver " +
                     driver + " available")

    def DatabaseInit(self):
        query = QSqlQuery()
        if not query.exec("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
            qWarning("DatabaseInit - ERROR " + query.lastError().text())

        availableTableNames = []
        while query.next():
            availableTableNames.append(query.value(0))

        for tableName in ["DRAW", "DRAWPREDICTIONS", "PLAYER"]:
            if tableName in availableTableNames:
                if not query.exec("DELETE FROM " + tableName):
                    qWarning("DatabaseInit - ERROR " +
                             query.lastError().text())
            else:  # table doesn't exist
                if tableName == "DRAW":
                    self.createTableDraw()
                elif tableName == "DRAWPREDICTIONS":
                    self.createTableDrawPredictions()
                elif tableName == "PLAYER":
                    self.createTablePlayer()

    def SaveDrawToDb(self, dbName, tennisData):
        self.DatabaseConnect(dbName)
        self.DatabaseInit()
        self.populateTableDraw(tennisData.drawRowList)
        self.populateTableDrawPredictions(tennisData.drawPredictionsRowList)
        self.populateTablePlayer(tennisData.playerRowList)

    def LoadDrawFromDb(self, dbName, tennisData):
        self.DatabaseConnect(dbName)
        self.loadTableDraw(tennisData.drawRowList)
        self.loadTableDrawPredictions(tennisData.drawPredictionsRowList)
        self.loadTablePlayer(tennisData.playerRowList)

    def createTableDraw(self):
        query = QSqlQuery(
            "CREATE TABLE DRAW (id INTEGER PRIMARY KEY, Round INTEGER, Player1 TEXT, Player2 TEXT)")
        if not query.isActive():
            qWarning("createTableDraw - ERROR: " + query.lastError().text())

    def createTableDrawPredictions(self):
        query = QSqlQuery(
            "CREATE TABLE DRAWPREDICTIONS (id INTEGER PRIMARY KEY, Round INTEGER, Player1 TEXT, Player2 TEXT)")
        if not query.isActive():
            qWarning("createTableDrawPredictions - ERROR: " +
                     query.lastError().text())

    def createTablePlayer(self):
        query = QSqlQuery(
            "CREATE TABLE PLAYER (id INTEGER PRIMARY KEY, Player TEXT, Seed TEXT, Country TEXT)")
        if not query.isActive():
            qWarning("createTablePlayer - ERROR: " + query.lastError().text())

    def populateTableDraw(self, drawRowList):
        query = QSqlQuery()
        query.prepare(
            "INSERT INTO Draw(Round, Player1, Player2) VALUES(?,?,?)")
        QSqlDatabase.database().transaction()
        for row in drawRowList:
            query.bindValue(0, row[0])
            query.bindValue(1, row[1])
            query.bindValue(2, row[2])
            if not query.exec():
                qWarning("populateTableDraw - ERROR: " +
                         query.lastError().text())
        QSqlDatabase.database().commit()

    def populateTableDrawPredictions(self, drawRowList):
        query = QSqlQuery()
        query.prepare(
            "INSERT INTO DrawPredictions(Round, Player1, Player2) VALUES(?,?,?)")
        QSqlDatabase.database().transaction()
        for row in drawRowList:
            query.bindValue(0, row[0])
            query.bindValue(1, row[1])
            query.bindValue(2, row[2])
            if not query.exec():
                qWarning("populateTableDrawPredictions - ERROR: " +
                         query.lastError().text())
        QSqlDatabase.database().commit()

    def populateTablePlayer(self, playerRowList):
        query = QSqlQuery()
        query.prepare(
            "INSERT INTO Player(Player, Seed, Country) VALUES(?,?,?)")
        QSqlDatabase.database().transaction()
        for row in playerRowList:
            query.bindValue(0, row[0])
            query.bindValue(1, row[1])
            query.bindValue(2, row[2])
            if not query.exec():
                qWarning("populateTablePlayer - ERROR: " +
                         query.lastError().text())
        QSqlDatabase.database().commit()

    def loadTableDraw(self, drawRowList):
        query = QSqlQuery()
        if not query.exec("SELECT Round, Player1, Player2 FROM DRAW"):
            qWarning("loadTableDraw - ERROR " + query.lastError().text())
        while query.next():
            roundNum = query.value(0)
            player1 = query.value(1)
            player2 = query.value(2)
            drawRowList.append([roundNum, player1, player2])

    def loadTableDrawPredictions(self, drawRowList):
        query = QSqlQuery()
        if not query.exec("SELECT Round, Player1, Player2 FROM DRAWPREDICTIONS"):
            qWarning("loadTableDrawPredictions - ERROR " +
                     query.lastError().text())
        while query.next():
            roundNum = query.value(0)
            player1 = query.value(1)
            player2 = query.value(2)
            drawRowList.append([roundNum, player1, player2])

    def loadTablePlayer(self, playerRowList):
        query = QSqlQuery()
        if not query.exec("SELECT Player, Seed, Country FROM PLAYER"):
            qWarning("loadTablePlayer - ERROR " + query.lastError().text())
        while query.next():
            player = query.value(0)
            seed = query.value(1)
            country = query.value(2)
            playerRowList.append([player, seed, country])
