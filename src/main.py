import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from mainWindow import *

if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()

    app.exec()

"""headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
url = "https://www.atptour.com/en/scores/archive/cincinnati/422/2019/draws"
html_dir = os.path.dirname(os.path.realpath(__file__)) + "/html_data/"
fname = html_dir + "out2.html"

from urllib.request import urlopen, Request

req = Request(url=url, headers=headers)
html = urlopen(req).read()
html_file = open(fname, "w")
html_file.write(html.decode("utf-8"))
html_file.close()
"""