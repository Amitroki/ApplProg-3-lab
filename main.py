import sys

import PyQt5
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QMessageBox, QToolBar, QToolTip, QVBoxLayout, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon

class Interface(QMainWindow):
    def __init__(self):

        super(Interface, self).__init__()
        self.setWindowTitle("ImageMaster")
        self.setWindowIcon(QIcon("sources/icon.png"))
        self.setGeometry(100, 100, 1600, 800)

        self.centralwidget = QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget) 

        font = QtGui.QFont()
        font.setWeight(20)
        font.setPointSize(17)
        font.setBold(True)

        self.button_change_end = QtWidgets.QPushButton(text = "End", clicked = self.handle_end_button)
        self.button_change_end.setFont(font)

        self.button_1 = QtWidgets.QPushButton(text = "Two datasets(ordered)")
        self.button_1.setFont(font)

        self.button_2 = QtWidgets.QPushButton(text = "Two datasets(mixed)")
        self.button_2.setFont(font)

        self.button_create_annotation = QtWidgets.QPushButton(text = "Create annotation")
        self.button_create_annotation.setFont(font)

        self.window_image = QLabel(self)
        self.image = QPixmap("sources/test_image.png")
        self.image = self.image.scaled(1280, 720, QtCore.Qt.KeepAspectRatio)
        self.window_image.setPixmap(self.image)
        self.window_image.setAlignment(Qt.AlignCenter)

        self.previous = QPushButton("", self)
        self.previous.setIcon(QtGui.QIcon("sources/left-arrow.png"))

        self.next = QPushButton("", self)
        self.next.setIcon(QtGui.QIcon("sources/right-arrow.png"))

        self.file_path = QLabel(self)
        self.file_path.setText("PATH")
        self.file_path.setFont(font)
        self.file_path.setAlignment(Qt.AlignCenter)

        self.layout = QGridLayout(self.centralwidget)
        self.layout.addWidget(self.button_change_end, 0, 0)
        self.layout.addWidget(self.button_1, 0, 1)
        self.layout.addWidget(self.button_2, 0, 2)
        self.layout.addWidget(self.button_create_annotation, 0, 3, 1, 2)
        self.layout.addWidget(self.window_image, 1, 0, 4, 5)
        self.layout.addWidget(self.previous, 5, 0)
        self.layout.addWidget(self.next, 5, 1)
        self.layout.addWidget(self.file_path, 5, 2, 1, 3)


    def handle_end_button(self):
        button = self.sender()
        if button is not None:
            text = button.text()
            button.setText("Cycle" if text == "End" else "End")


stylesheet = """
    Interface {
        background-color: lightcyan;
        background-repeat: no-repeat; 
        background-position: center;
    }
"""

def application():
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    window = Interface()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    application()