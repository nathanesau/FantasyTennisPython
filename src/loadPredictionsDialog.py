from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os.path
import os
from settings import *

class LoadPredictionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fileComboBoxLabel = QLabel()
        self.fileComboBoxLabel.setText("Select predictions to load")
        self.fileComboBox = QComboBox()
        cb_items = []
        for root, directories, files in os.walk(Settings.readCustomDir()):
            for f in files:
                if '.db' in f:
                    cb_items.append(f)
        self.fileComboBox.addItems(cb_items)
        self.fileComboBox.setCurrentIndex(0)
        
        self.fileLayout = QHBoxLayout()
        self.fileLayout.addWidget(self.fileComboBoxLabel)
        self.fileLayout.addWidget(self.fileComboBox)
        
        self.okButton = QPushButton()
        self.okButton.setText("OK")
        self.okButton.pressed.connect(super().accept)
        
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.okButton)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.fileLayout)
        self.mainLayout.addStretch(1)
        self.mainLayout.addLayout(self.buttonLayout)

        self.setLayout(self.mainLayout)

        self.setWindowTitle("Select predictions")
        self.setWindowIcon(QIcon(":icon.png"))