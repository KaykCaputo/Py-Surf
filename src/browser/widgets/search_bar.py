from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton
from PyQt5.QtCore import QUrl


class SearchBar(QWidget):
    def __init__(self, tabs_widget):
        super().__init__()
        self.tabs_widget = tabs_widget
        self.setFixedHeight(32)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Navigation buttons
        self.back_button = QPushButton("⟵", self)
        self.forward_button = QPushButton("⟶", self)
        self.reload_button = QPushButton("⟳", self)

        self.back_button.clicked.connect(self.go_back)
        self.forward_button.clicked.connect(self.go_forward)
        self.reload_button.clicked.connect(self.reload)

        # Address/search input field
        self.address_input = QLineEdit(self)
        self.address_input.setPlaceholderText("Enter address or search term")
        self.address_input.returnPressed.connect(self.search)

        # Go button
        self.go_button = QPushButton("Go", self)
        self.go_button.clicked.connect(self.search)

        layout.addWidget(self.back_button)
        layout.addWidget(self.forward_button)
        layout.addWidget(self.reload_button)
        layout.addWidget(self.address_input)
        layout.addWidget(self.go_button)

        self.setLayout(layout)

    def go_back(self):
        self.tabs_widget.current_view().browser.back()

    def go_forward(self):
        self.tabs_widget.current_view().browser.forward()

    def reload(self):
        self.tabs_widget.current_view().browser.reload()

    def search(self):
        query = self.address_input.text()
        if not query:
            return

        # If input looks like a URL, open it directly
        if query.startswith("http://") or query.startswith("https://"):
            url = QUrl(query)
        elif "." in query:  # possible domain without protocol
            url = QUrl(f"https://{query}")
        else:  # otherwise perform a Google search
            url = QUrl(f"https://www.google.com/search?q={query}")

        self.tabs_widget.current_view().browser.setUrl(url)

    def update_url(self, url: QUrl):
        self.address_input.setText(url.toString())
