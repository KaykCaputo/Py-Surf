# main_widget.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from .tabs_widget import TabsWidget
from .search_bar import SearchBar


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySurf Browser")
        self.setGeometry(100, 100, 1024, 768)

        # Initialize TabsWidget and SearchBar
        self.tabs_widget = TabsWidget()
        self.search_bar = SearchBar(self.tabs_widget)

        # Keep track of the last connected tab to disconnect its signal
        self._last_tab = None

        # Connect URL change event on tab switch
        self.tabs_widget.currentChanged.connect(self.on_tab_changed)
        self.on_tab_changed(0)

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.search_bar)
        layout.addWidget(self.tabs_widget)
        self.setLayout(layout)

    def on_tab_changed(self, index: int):

        if self._last_tab and hasattr(self._last_tab, "browser"):
            try:
                self._last_tab.browser.urlChanged.disconnect(self.search_bar.update_url)
            except TypeError:
                pass

        current_tab = self.tabs_widget.widget(index)

        if not hasattr(current_tab, "browser"):
            self._last_tab = None
            return

        self.search_bar.update_url(current_tab.browser.url())
        current_tab.browser.urlChanged.connect(self.search_bar.update_url)
        self._last_tab = current_tab
