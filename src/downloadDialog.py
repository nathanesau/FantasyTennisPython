from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os.path
import os

html_dir = os.path.dirname(os.path.realpath(__file__)) + "/html_data/"
tmp_dir = os.path.dirname(os.path.realpath(__file__)) + "/tmp/"


def downloadArchive():
    url = "https://www.atptour.com/en/scores/results-archive"
    fname = tmp_dir + "archive.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    req = Request(url=url, headers=headers)
    html = urlopen(req).read()
    html_file = open(fname, "w")
    html_file.write(html.decode("utf-8"))
    html_file.close()

# parse links from atptour.com/en/scores/results-archive using bs4


def getDownloadOptions():
    inputFName = tmp_dir + "archive.html"

    soup = BeautifulSoup(open(inputFName), "html.parser")

    download_options = {}  # key: title, value: links

    def stripTitle(titleTag):
        title = str(titleTag.contents)
        for substr in ["  ", '\\n', '\\', '[', ']', '\'', '\"']:
            title = title.replace(substr, '')
        return title

    for tourney in soup.find_all('tr', {'class': 'tourney-result'}):
        title = tourney.find_all('span', {'class': 'tourney-title'})
        title = stripTitle(title[0])
        links = tourney.find_all('a')
        for link in links:
            href = None if 'href' not in link.attrs else link['href']
            if href is not None:
                if "singles" in href:
                    download_options[title] = href
                    break

    return download_options


class DownloadDialog(QDialog):
    def __init__(self, download_options, defaultFName, parent=None):
        super().__init__(parent)
        self.urlLabel = QLabel()
        self.urlLabel.setText(
            "Specify tournmanet to download HTML bracket for...")

        self.urlComboBox = QComboBox()
        self.urlComboBox.addItems(download_options.keys())
        self.urlComboBox.setCurrentIndex(0)
        self.urlLabel.setToolTip(
            "Example: https://www.atptour.com/en/scores/archive/cincinnati/422/2019/draws")

        self.urlLayout = QVBoxLayout()
        self.urlLayout.addWidget(self.urlLabel)
        self.urlLayout.addWidget(self.urlComboBox)

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
