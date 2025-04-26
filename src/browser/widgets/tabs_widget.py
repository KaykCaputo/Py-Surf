from PyQt5.QtWidgets import QApplication, QTabWidget, QTabBar, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, QSize
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPen, QColor
from PyQt5.QtWebEngineWidgets import QWebEngineView

PLUS_DATA_KEY = "plus"


def make_round_plus_icon(
    icon_size=16, circle_color=QColor(200, 200, 200), plus_color=QColor(50, 50, 50)
) -> QIcon:
    """Generate a small circular '+' icon."""
    pix = QPixmap(icon_size, icon_size)
    pix.fill(Qt.transparent)
    painter = QPainter(pix)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setPen(Qt.NoPen)
    painter.setBrush(circle_color)
    painter.drawEllipse(0, 0, icon_size, icon_size)
    pen = QPen(plus_color)
    pen.setWidth(2)
    painter.setPen(pen)
    offset = icon_size * 0.3
    center = icon_size / 2
    painter.drawLine(int(center), int(offset), int(center), int(icon_size - offset))
    painter.drawLine(int(offset), int(center), int(icon_size - offset), int(center))
    painter.end()
    return QIcon(pix)


class CustomTabBar(QTabBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setElideMode(Qt.ElideRight)
        self.setDrawBase(False)
        self.setStyleSheet(
            """
            QTabBar::tab:last {
                background: transparent;
                border: none;
            }
            QTabBar::tab:last:selected,
            QTabBar::tab:last:hover {
                background: transparent;
            }
        """
        )

    def tabSizeHint(self, index):
        if self.tabData(index) == PLUS_DATA_KEY:
            size = 16 + 8
            return QSize(size, size)
        size = super().tabSizeHint(index)
        size.setHeight(30)
        return size

    def minimumTabSizeHint(self, index):
        return self.tabSizeHint(index)


class TabWidget(QWidget):
    titleChanged = pyqtSignal(str)
    iconChanged = pyqtSignal(QIcon)

    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView(self)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.browser)
        self.browser.titleChanged.connect(self.titleChanged)
        self.browser.iconChanged.connect(self.iconChanged)

    def setUrl(self, url: QUrl):
        self.browser.setUrl(url)


class TabsWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setTabBar(CustomTabBar(self))
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setElideMode(Qt.ElideRight)
        self.setUsesScrollButtons(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.tabBarClicked.connect(self.on_tab_clicked)
        self.add_real_tab()
        self.add_plus_tab()

    def current_view(self):
        return self.currentWidget()

    def add_real_tab(self, url: QUrl = QUrl("https://www.google.com")):
        plus_index = self.count() - 1 if self.count() > 0 else 0
        new_tab = TabWidget()
        idx = self.insertTab(plus_index, new_tab, "New Tab")
        new_tab.setUrl(url)
        self.setCurrentIndex(idx)
        new_tab.titleChanged.connect(lambda t, i=idx: self.setTabText(i, t))
        new_tab.iconChanged.connect(lambda ic, i=idx: self.setTabIcon(i, ic))

    def add_plus_tab(self):
        if (
            self.count() > 0
            and self.tabBar().tabData(self.count() - 1) == PLUS_DATA_KEY
        ):
            return
        self.addTab(QWidget(), "")
        idx = self.count() - 1
        self.tabBar().setTabData(idx, PLUS_DATA_KEY)
        self.setIconSize(QSize(16, 16))
        self.setTabIcon(idx, make_round_plus_icon(16))
        self.tabBar().setTabButton(idx, QTabBar.RightSide, None)

    def on_tab_clicked(self, index: int):
        if index == self.count() - 1 and self.tabBar().tabData(index) == PLUS_DATA_KEY:
            self.add_real_tab()

    def close_tab(self, index: int):
        if index == self.count() - 1 and self.tabBar().tabData(index) == PLUS_DATA_KEY:
            return
        self.removeTab(index)
        remaining = self.count()
        if remaining == 0 or (
            remaining == 1 and self.tabBar().tabData(0) == PLUS_DATA_KEY
        ):
            QApplication.quit()
            return
        new_idx = index - 1 if index > 0 else 0
        if self.tabBar().tabData(new_idx) == PLUS_DATA_KEY:
            new_idx = 0 if new_idx == self.count() - 1 else new_idx + 1
        self.setCurrentIndex(new_idx)
