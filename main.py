import sys

import PyQt5
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

class Interface(QMainWindow):
    def __init__(self):
        super(Interface, self).__init__()

        self.setWindowTitle("ImageMaster")
        self.setGeometry(100, 100, 1600, 800)

        font = QtGui.QFont()
        font.setWeight(20)
        font.setPointSize(17)
        font.setBold(True)
        self.text = QtWidgets.QLabel(self)
        self.text.setFont(font)
        self.text.setText("abcde")
        self.text.move(50, 100)
        self.text.adjustSize()

def application():
    app = QApplication(sys.argv)
    window = Interface()

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    application()