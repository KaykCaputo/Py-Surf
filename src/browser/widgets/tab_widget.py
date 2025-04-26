from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtGui import QIcon


class TabWidget(QWidget):
    titleChanged = pyqtSignal(str)
    iconChanged = pyqtSignal(QIcon)

    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView(self)
        self.devtools_view = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.browser)

        self.browser.titleChanged.connect(self.titleChanged)
        self.browser.iconChanged.connect(self.iconChanged)

    def setUrl(self, url):
        self.browser.setUrl(url)
