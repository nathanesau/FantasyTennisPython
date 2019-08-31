from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os.path
import os

html_dir = os.path.dirname(os.path.realpath(__file__)) + "/html_data/"

class DownloadDialog(QDialog):
    def __init__(self, defaultURL, defaultFName, parent=None):
        super().__init__(parent)
        self.urlLabel = QLabel()
        self.urlLabel.setText("Specify URL to download HTML bracket from...\t\t\t\t\t")
        self.urlLE = QLineEdit()
        self.urlLE.setText(defaultURL)
        self.urlLabel.setToolTip("Example: https://www.atptour.com/en/scores/archive/cincinnati/422/2019/draws")
        
        self.urlLayout = QVBoxLayout()
        self.urlLayout.addWidget(self.urlLabel)
        self.urlLayout.addWidget(self.urlLE)
        
        self.fnameLabel = QLabel()
        self.fnameLabel.setText("Specify output filename...")
        self.fnameLE = QLineEdit()
        self.fnameLE.setText(defaultFName)
        self.fnameLabel.setToolTip("Example: out.html")

        self.fnameLayout = QVBoxLayout()
        self.fnameLayout.addWidget(self.fnameLabel)
        self.fnameLayout.addWidget(self.fnameLE)

        self.okButton = QPushButton()
        self.okButton.setText("OK")
        self.okButton.pressed.connect(super().accept)
        
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.okButton)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.urlLayout)
        self.mainLayout.addStretch(1)
        self.mainLayout.addLayout(self.fnameLayout)
        self.mainLayout.addStretch(1)
        self.mainLayout.addLayout(self.buttonLayout)

        self.setLayout(self.mainLayout)

        self.setWindowTitle("Download HTML bracket")
        self.setWindowIcon(QIcon(":icon.png"))