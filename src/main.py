from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QToolBar, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
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

        self.setupUi()

    def setupUi(self):
        self.toolbar = QToolBar("MainToolbar")
        self.toolbar.setObjectName("MainToolbar")
        self.addToolBar(self.toolbar)

        self.central_widget = QWidget()
        self.central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        
        self.content_label = QLabel("Pyalysis")
        self.content_label.setObjectName("ContentLabel")
        self.content_label.setAlignment(Qt.AlignCenter)

        self.logo
        
        self.action_button = QPushButton("Click Me")
        self.action_button.setFixedSize(200, 50)
        
        self.layout.addWidget(self.content_label)
        self.layout.addWidget(self.action_button, alignment=Qt.AlignCenter)

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