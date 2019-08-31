from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os.path
import os

class SavePredictionsDialog(QDialog):
    def __init__(self, defaultFileName, parent=None):
        super().__init__(parent)
        self.fileNameLabel = QLabel()
        self.fileNameLabel.setText("Specify file name (.db)")
        self.fileNameLE = QLineEdit()
        self.fileNameLE.setText(defaultFileName)
        
        self.fileLayout = QHBoxLayout()
        self.fileLayout.addWidget(self.fileNameLabel)
        self.fileLayout.addWidget(self.fileNameLE)
        
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

        self.setWindowTitle("Save predictions")
        self.setWindowIcon(QIcon(":icon.png"))