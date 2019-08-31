from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os.path
import os

ORGANIZATION_NAME = "nathanesau_software"
APPLICATION_NAME = "FantasyTennis"

class Settings:
    default_data_dir = "data/"
    default_html_dir = "html_data/"
    default_custom_dir = "custom_data/"

    @staticmethod
    def readDataDir():
        settings = QSettings(ORGANIZATION_NAME, APPLICATION_NAME)
        settings.beginGroup("Directories")
        dataDir = settings.value("dataDir", Settings.default_data_dir)
        settings.endGroup()
        try:
            if not os.path.exists(dataDir):
                os.mkdir(dataDir)
        except:
            print("cannot create data dir")
        return dataDir

    @staticmethod
    def writeDataDir(dataDir):
        if len(dataDir) > 0:
            dataDir = dataDir if dataDir[-1] == '/' else dataDir + "/"
        settings = QSettings(ORGANIZATION_NAME, APPLICATION_NAME)
        settings.beginGroup("Directories")
        settings.setValue("dataDir", dataDir)
        settings.endGroup()
    
    @staticmethod
    def readHtmlDir():
        settings = QSettings(ORGANIZATION_NAME, APPLICATION_NAME)
        settings.beginGroup("Directories")
        htmlDir = settings.value("htmlDir", Settings.default_html_dir)
        settings.endGroup()
        try:
            if not os.path.exists(htmlDir):
                os.mkdir(htmlDir)
        except:
            print("cannot create html dir")
        return htmlDir

    @staticmethod
    def writeHtmlDir(htmlDir):
        if len(htmlDir) > 0:
            htmlDir = htmlDir if htmlDir[-1] == '/' else htmlDir + "/"
        settings = QSettings(ORGANIZATION_NAME, APPLICATION_NAME)
        settings.beginGroup("Directories")
        settings.setValue("htmlDir", htmlDir)
        settings.endGroup()

    @staticmethod
    def readCustomDir():
        settings = QSettings(ORGANIZATION_NAME, APPLICATION_NAME)
        settings.beginGroup("Directories")
        customDir = settings.value("customDir", Settings.default_custom_dir)
        settings.endGroup()
        try:
            if not os.path.exists(customDir):
                os.mkdir(customDir)
        except:
            print("cannot create predictions dir")
        return customDir
    
    @staticmethod
    def writeCustomDir(customDir):
        if len(customDir) > 0:
            customDir = customDir if customDir[-1] == '/' else customDir + "/"
        settings = QSettings(ORGANIZATION_NAME, APPLICATION_NAME)
        settings.beginGroup("Directories")
        settings.setValue("customDir", customDir)
        settings.endGroup()

class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.dataDirLabel = QLabel()
        self.dataDirLabel.setText("Data Directory")
        self.dataDirLE = QLineEdit()
        self.dataDirLE.setText(Settings.readDataDir())
        self.dataDirLE.setFixedWidth(300)

        self.htmlDirLabel = QLabel()
        self.htmlDirLabel.setText("HTML Directory")
        self.htmlDirLE = QLineEdit()
        self.htmlDirLE.setText(Settings.readHtmlDir())
        self.htmlDirLE.setFixedWidth(300)

        self.customDirLabel = QLabel()
        self.customDirLabel.setText("Predictions Directory")
        self.customDirLE = QLineEdit()
        self.customDirLE.setText(Settings.readCustomDir())
        self.customDirLE.setFixedWidth(300)

        self.gridLayout = QGridLayout()
        self.gridLayout.addWidget(self.dataDirLabel, 0, 0)
        self.gridLayout.addWidget(self.dataDirLE, 0, 1)
        self.gridLayout.addWidget(self.htmlDirLabel, 1, 0)
        self.gridLayout.addWidget(self.htmlDirLE, 1, 1)
        self.gridLayout.addWidget(self.customDirLabel, 2, 0)
        self.gridLayout.addWidget(self.customDirLE, 2, 1)
        self.gridLayout.setSizeConstraint(QLayout.SetMinimumSize)

        self.okButton = QPushButton()
        self.okButton.setText("OK")
        self.okButton.clicked.connect(self.accept)
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.okButton)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.gridLayout)
        self.mainLayout.addLayout(self.buttonLayout)
        
        self.setLayout(self.mainLayout)
        self.setWindowTitle("Preferences")
        self.setWindowIcon(QIcon(":icon.png"))