from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QPushButton, QToolBar, QHBoxLayout
from PyQt5.QtCore import Qt, QPoint
import sys
from components.titlebar import TitleBar
from dotenv import load_dotenv

load_dotenv()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("Pyalysis")
        
        self.titlebar = TitleBar(self)
        self.setMenuWidget(self.titlebar)

        self.setup_ui()

    def setup_ui(self):
        self.toolbar = QToolBar("MainToolbar")
        self.toolbar.setObjectName("MainToolbar")
        self.addToolBar(self.toolbar)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        with open("src/stylesheets/styles.qss", 'r') as f:
            style = f.read()
            app.setStyleSheet(style)
    except FileNotFoundError:
        print("Stylesheet not found")
        
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())