import sys
import os

import PyQt5
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QMessageBox, QDialog, QVBoxLayout, QLineEdit, QFileDialog, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon, QFont

import sources.lab_2_materials.default_dataset_operations
import sources.lab_2_materials.united_dataset
import sources.lab_2_materials.mixed_dataset
import sources.lab_2_materials.iterator

class Selection_window(QWidget):
        def __init__(self, executable_task_name: str):
            window = QMessageBox()
            window.setWindowTitle(executable_task_name)
            window.exec_()

class Interface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("ImageMaster")
        self.setWindowIcon(QIcon("sources/images/icon.png"))

        self.centralwidget = QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)

        self.type_dataset = "single"
        self.window_image = QLabel(self)
        self.image = QPixmap("sources/images/test_image.png")
        self.image = self.image.scaled(1280, 720, QtCore.Qt.KeepAspectRatio)
        self.window_image.setPixmap(self.image)
        self.window_image.setAlignment(Qt.AlignCenter)
        
        self.choose_folder_button = QPushButton(text = "Choose folder", clicked = self.choose_folder)
        self.choose_folder_button.setFont(QFont("IMPACT", 18))

        self.button_change_end = QPushButton(text = "End", clicked = self.handle_end_button)
        self.button_change_end.setFont(QFont("IMPACT", 18))

        self.button_1 = QPushButton(text = "Two datasets(ordered)")
        self.button_1.setFont(QFont("IMPACT", 18))

        self.button_2 = QPushButton(text = "Two datasets(mixed)")
        self.button_2.setFont(QFont("IMPACT", 18))
    
        self.button_create_annotation = QtWidgets.QPushButton(text = "Create annotation", clicked = self.create_annotation)
        self.button_create_annotation.setFont(QFont("IMPACT", 15))

        self.previous = QPushButton(text = "", clicked = self.option_previous)
        self.previous.setIcon(QtGui.QIcon("sources/images/left-arrow.png"))
        self.previous.setFixedSize(50, 50)

        self.next = QPushButton(text = "", clicked = self.option_next)
        self.next.setIcon(QtGui.QIcon("sources/images/right-arrow.png"))
        self.next.setFixedSize(50, 50)

        self.file_path = QLabel(self)
        self.file_path.setText("PATH")
        self.file_path.setFont(QFont("IMPACT", 10))
        self.file_path.setAlignment(Qt.AlignCenter)

        self.layout = QGridLayout(self.centralwidget)
        self.layout.addWidget(self.button_change_end, 0, 0)
        self.layout.addWidget(self.choose_folder_button, 0, 1)
        self.layout.addWidget(self.button_1, 0, 2)
        self.layout.addWidget(self.button_2, 0, 3)
        self.layout.addWidget(self.window_image, 1, 0, 4, 4)
        self.layout.addWidget(self.previous, 5, 0)
        self.layout.addWidget(self.next, 5, 1)
        self.layout.addWidget(self.file_path, 5, 2)
        self.layout.addWidget(self.button_create_annotation, 5, 3)

        self.show()

    def create_annotation(self):
        sources.lab_2_materials.default_dataset_operations.create_file("annotation_of_default_dataset.csv")
        sources.lab_2_materials.default_dataset_operations.input_data(self.folderpath, "annotation_of_default_dataset.csv")
    
    def choose_folder(self):
        try:
            self.folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, "Select folder", "")
            if not "." in self.folderpath:
                self.iterator = sources.lab_2_materials.iterator.Iterator(self.folderpath)
                image_path = next(self.iterator)                  
                self.image = QPixmap(image_path)
                self.image = self.image.scaled(1280, 720, QtCore.Qt.KeepAspectRatio)
                self.window_image.setPixmap(self.image)
                self.window_image.setAlignment(Qt.AlignCenter)
                self.file_path.setText(image_path)
        except FileNotFoundError:
            error = QMessageBox()
            error.setWindowTitle("Problem")
            error.setText("This action cannot be performed now")
            error.setInformativeText("Please, choose a folder")
            error.exec_()
            self.choose_folder_button.click()

    def option_next(self):
        if self.button_change_end.text() == "End":
            try:
                image_path = next(self.iterator)
                self.image = QPixmap(image_path)
                self.image = self.image.scaled(1280, 720, QtCore.Qt.KeepAspectRatio)
                self.window_image.setPixmap(self.image)
                self.window_image.setAlignment(Qt.AlignCenter)
                self.file_path.setText(image_path)
            except StopIteration:
                self.iterator.counter -= 1
                error = QMessageBox()
                error.setWindowTitle("Problem")
                error.setText("This action cannot be performed now")
                error.setInformativeText("There is no next element")
                error.exec_()
            except AttributeError:
                error = QMessageBox()
                error.setWindowTitle("Problem")
                error.setText("This action cannot be performed now")
                error.setInformativeText("There is no next element")
                error.exec_()
        if self.button_change_end.text() == "Cycle":
            try:
                image_path = next(self.iterator)
                self.image = QPixmap(image_path)
                self.image = self.image.scaled(1280, 720, QtCore.Qt.KeepAspectRatio)
                self.window_image.setPixmap(self.image)
                self.window_image.setAlignment(Qt.AlignCenter)
                self.file_path.setText(image_path)
            except StopIteration:
                self.iterator.counter -= self.iterator.limit
                image_path = next(self.iterator)
                self.image = QPixmap(image_path)
                self.image = self.image.scaled(1280, 720, QtCore.Qt.KeepAspectRatio)
                self.window_image.setPixmap(self.image)
                self.window_image.setAlignment(Qt.AlignCenter)
                self.file_path.setText(image_path)

    def option_previous(self):
        if self.button_change_end.text() == "End":
            try:
                image_path = self.iterator.previous()
                self.image = QPixmap(image_path)
                self.image = self.image.scaled(1280, 720, QtCore.Qt.KeepAspectRatio)
                self.window_image.setPixmap(self.image)
                self.window_image.setAlignment(Qt.AlignCenter)
                self.file_path.setText(image_path)
            except StopIteration:
                self.iterator.counter += 1
                error = QMessageBox()
                error.setWindowTitle("Problem")
                error.setText("This action cannot be performed now")
                error.setInformativeText("There is no element behind")
                error.exec_()
            except AttributeError:
                error = QMessageBox()
                error.setWindowTitle("Problem")
                error.setText("This action cannot be performed now")
                error.setInformativeText("There is no element behind")
                error.exec_()
        if self.button_change_end.text() == "Cycle":
            try:
                image_path = self.iterator.previous()
                self.image = QPixmap(image_path)
                self.image = self.image.scaled(1280, 720, QtCore.Qt.KeepAspectRatio)
                self.window_image.setPixmap(self.image)
                self.window_image.setAlignment(Qt.AlignCenter)
                self.file_path.setText(image_path)
            except StopIteration:
                self.iterator.counter = self.iterator.limit
                image_path = self.iterator.previous()
                self.image = QPixmap(image_path)
                self.image = self.image.scaled(1280, 720, QtCore.Qt.KeepAspectRatio)
                self.window_image.setPixmap(self.image)
                self.window_image.setAlignment(Qt.AlignCenter)
                self.file_path.setText(image_path)

    def handle_end_button(self):
        if self.button_change_end is not None:
            text = self.button_change_end.text()
            self.button_change_end.setText("Cycle" if text == "End" else "End")



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
    sys.exit(app.exec_())

if __name__ == "__main__":
    application()