from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from browser.widgets.main_widget import MainWidget
from PyQt5.QtGui import QIcon

import os

QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)


def main():
    app = QApplication([])

    base_path = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_path, "resources", "icon.png")
    icon = QIcon(icon_path)

    with open("src/browser/themes/dark_theme.qss", "r") as f:
        app.setStyleSheet(f.read())

    app.setWindowIcon(icon)

    window = MainWidget()
    window.setWindowIcon(icon)
    window.resize(1200, 800)
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
