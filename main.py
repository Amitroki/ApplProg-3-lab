import sys
import os
import shutil

import PyQt5
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QMessageBox, QDialog, QVBoxLayout, QLineEdit, QFileDialog, QGridLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon, QFont

import sources.lab_2_materials.default_dataset_operations
import sources.lab_2_materials.united_dataset
import sources.lab_2_materials.mixed_dataset
import sources.lab_2_materials.iterator

class PopupWindow(QMessageBox):
    def __init__(self, title: str, text_inside: str, informative_text: str):
        error = QMessageBox()
        error.setWindowIcon(QIcon("sources/images/icon.png"))
        error.setFixedSize(200, 200)
        error.setWindowTitle(title)
        error.setIcon(QMessageBox.Warning)
        error.setText(text_inside)
        error.setInformativeText(informative_text)
        error.exec_()

class WindowWithRequest(QDialog):
    def __init__(self, title: str):
        self.request_window = QDialog()
        self.title = title
        self.request_window.setWindowTitle(self.title)
        self.request_window.setFixedSize(300, 100)
        self.file_name = QLineEdit(self.request_window)
        self.window_layout = QVBoxLayout(self.request_window)
        self.window_layout.addWidget(self.file_name)
        self.request_window.exec_()

    def checking_correctness(self) -> bool:
        for i in self.file_name.text():
            if i in ["<", ">", "«", ":", "#", "%", "&", "{", "}", "\\", "*", "$", "!", "'", "/", "|"]:
                PopupWindow("Incorrect file name", "Invalid characters are present", "Please, write another name for the file")
                return False
        return True

    def get_text(self) -> str:
        return self.file_name.text()


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

        self.status = "free"

        files = os.listdir(os.getcwd())

        for file in files:
            if file.endswith(".csv"):
                os.remove(os.path.join(os.getcwd(), file))
            
        if os.path.isdir("new_dataset"):
            shutil.rmtree("new_dataset")

        self.window_image = QLabel(self)
        self.image = QPixmap("sources/images/test_image.png")
        self.image = self.image.scaled(1280, 720, QtCore.Qt.KeepAspectRatio)
        self.window_image.setPixmap(self.image)
        self.window_image.setAlignment(Qt.AlignCenter)
        
        self.choose_folder_button = QPushButton(text = "Choose folder", clicked = self.choose_folder)
        self.choose_folder_button.setFont(QFont("IMPACT", 18))

        self.button_change_end = QPushButton(text = "End", clicked = self.handle_end_button)
        self.button_change_end.setFont(QFont("IMPACT", 18))

        self.button_1 = QPushButton(text = "Create ordered dataset", clicked = self.copy_dataset)
        self.button_1.setFont(QFont("IMPACT", 18))

        self.button_2 = QPushButton(text = "Create mixed dataset")
        self.button_2.setFont(QFont("IMPACT", 18))
    
        self.button_create_annotation = QtWidgets.QPushButton(text = "Create annotation", clicked = self.create_annotation)
        self.button_create_annotation.setFont(QFont("IMPACT", 15))

        self.previous1 = QPushButton(text = "", clicked = self.option_previous1)
        self.previous1.setIcon(QtGui.QIcon("sources/images/left-arrow.png"))

        self.next1 = QPushButton(text = "", clicked = self.option_next1)
        self.next1.setIcon(QtGui.QIcon("sources/images/right-arrow.png"))

        self.previous2 = QPushButton(text = "", clicked = self.option_previous2)
        self.previous2.setIcon(QtGui.QIcon("sources/images/left-arrow.png"))

        self.next2 = QPushButton(text = "", clicked = self.option_next2)
        self.next2.setIcon(QtGui.QIcon("sources/images/right-arrow.png"))

        self.previous1.setEnabled(False)
        self.previous2.setEnabled(False)
        self.next1.setEnabled(False)
        self.next2.setEnabled(False)

        self.file_path = QLabel(self)
        self.file_path.setText("PATH")
        self.file_path.setFont(QFont("IMPACT", 10))
        self.file_path.setStyleSheet("color: white;")
        self.file_path.setAlignment(Qt.AlignCenter)

        self.layout = QGridLayout(self.centralwidget)
        self.layout.addWidget(self.button_change_end, 0, 0, 1, 2)
        self.layout.addWidget(self.choose_folder_button, 0, 2, 1, 2)
        self.layout.addWidget(self.button_1, 0, 4, 1, 2)
        self.layout.addWidget(self.button_2, 0, 6, 1, 2)
        self.layout.addWidget(self.window_image, 1, 0, 4, 8)
        self.layout.addWidget(self.previous1, 5, 0)
        self.layout.addWidget(self.next1, 5, 1)
        self.layout.addWidget(self.previous2, 5, 2)
        self.layout.addWidget(self.next2, 5, 3)
        self.layout.addWidget(self.file_path, 5, 4, 1, 3)
        self.layout.addWidget(self.button_create_annotation, 5, 7)

        self.show()

    def create_annotation(self):
        window = WindowWithRequest("Creating the file")
        if window.checking_correctness() == True:
            sources.lab_2_materials.default_dataset_operations.create_file(f"{window.get_text()}.csv")
            if self.status == "two folders":
                sources.lab_2_materials.default_dataset_operations.input_data(self.folderpath, f"{window.get_text()}.csv")
            if self.status == "ordered dataset":
                sources.lab_2_materials.united_dataset.input_data(self.folderpath, f"{window.get_text()}.csv")

    def choose_folder(self):
        try:
            self.status = "two folders"
            self.previous1.setEnabled(True)
            self.previous2.setEnabled(True)
            self.next1.setEnabled(True)
            self.next2.setEnabled(True)
            self.folderpath = QFileDialog.getExistingDirectory(self, "Select folder", "")
            self.iterator1 = sources.lab_2_materials.iterator.Iterator(os.path.join(self.folderpath, os.listdir(self.folderpath)[0]))
            self.iterator2 = sources.lab_2_materials.iterator.Iterator(os.path.join(self.folderpath, os.listdir(self.folderpath)[1]))
            image_path = next(self.iterator1)
            self.image = QPixmap(image_path)
            self.image = self.image.scaled(1280, 720, QtCore.Qt.KeepAspectRatio)
            self.window_image.setPixmap(self.image)
            self.window_image.setAlignment(Qt.AlignCenter)
            self.file_path.setText(image_path)
        except FileNotFoundError:
            PopupWindow("Problem", "This action cannot be performed now", "Please, choose a folder")
            self.choose_folder_button.click()

    def copy_dataset(self):
        try:
            self.status = "ordered dataset"
            self.previous1.setEnabled(True)
            self.previous2.setEnabled(False)
            self.next1.setEnabled(True)
            self.next2.setEnabled(False)
            self.folderpath = QFileDialog.getExistingDirectory(self, "Select folder", "")
            self.folderpath = sources.lab_2_materials.united_dataset.copy_dataset(self.folderpath, "new_dataset")
            self.iterator1 = sources.lab_2_materials.iterator.Iterator(self.folderpath)
            image_path = next(self.iterator1)
            self.image = QPixmap(image_path)
            self.image = self.image.scaled(1280, 720, QtCore.Qt.KeepAspectRatio)
            self.window_image.setPixmap(self.image)
            self.window_image.setAlignment(Qt.AlignCenter)
            self.file_path.setText(image_path)
        except FileNotFoundError:
            PopupWindow("Problem", "This action cannot be performed now", "Please, choose a folder")
            self.choose_folder_button.click()

    def mixed_dataset(self):
        try:
            self.status = "mixed dataset"
            self.previous1.setEnabled(True)
            self.previous2.setEnabled(False)
            self.next1.setEnabled(True)
            self.next2.setEnabled(False)
            self.folderpath = sources.lab_2_materials.united_dataset.copy_dataset(self.folderpath, "new_dataset")
            
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
                PopupWindow("Problem", "This action cannot be performed now", "There is no next element")
            except AttributeError:
                PopupWindow("Problem", "This action cannot be performed now", "There is no next element")
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

    def option_next1(self):
        if self.button_change_end.text() == "End":
            try:
                image_path = next(self.iterator1)
                self.image = QPixmap(image_path)
                self.image = self.image.scaled(1280, 720, QtCore.Qt.KeepAspectRatio)
                self.window_image.setPixmap(self.image)
                self.window_image.setAlignment(Qt.AlignCenter)
                self.file_path.setText(image_path)
            except StopIteration:
                self.iterator1.counter -= 1
                PopupWindow("Problem", "This action cannot be performed now", "There is no next element")
            except AttributeError:
                PopupWindow("Problem", "This action cannot be performed now", "There is no next element")
        if self.button_change_end.text() == "Cycle":
            try:
                image_path = next(self.iterator1)
                self.image = QPixmap(image_path)
                self.image = self.image.scaled(1280, 720, QtCore.Qt.KeepAspectRatio)
                self.window_image.setPixmap(self.image)
                self.window_image.setAlignment(Qt.AlignCenter)
                self.file_path.setText(image_path)
            except StopIteration:
                self.iterator1.counter -= self.iterator1.limit
                image_path = next(self.iterator1)
                self.image = QPixmap(image_path)
                self.image = self.image.scaled(1280, 720, QtCore.Qt.KeepAspectRatio)
                self.window_image.setPixmap(self.image)
                self.window_image.setAlignment(Qt.AlignCenter)
                self.file_path.setText(image_path)

    def option_next2(self):
        if self.button_change_end.text() == "End":
            try:
                image_path = next(self.iterator2)
                self.image = QPixmap(image_path)
                self.image = self.image.scaled(1280, 720, QtCore.Qt.KeepAspectRatio)
                self.window_image.setPixmap(self.image)
                self.window_image.setAlignment(Qt.AlignCenter)
                self.file_path.setText(image_path)
            except StopIteration:
                self.iterator2.counter -= 1
                PopupWindow("Problem", "This action cannot be performed now", "There is no next element")
            except AttributeError:
                PopupWindow("Problem", "This action cannot be performed now", "There is no next element")
        if self.button_change_end.text() == "Cycle":
            try:
                image_path = next(self.iterator2)
                self.image = QPixmap(image_path)
                self.image = self.image.scaled(1280, 720, QtCore.Qt.KeepAspectRatio)
                self.window_image.setPixmap(self.image)
                self.window_image.setAlignment(Qt.AlignCenter)
                self.file_path.setText(image_path)
            except StopIteration:
                self.iterator2.counter -= self.iterator2.limit
                image_path = next(self.iterator2)
                self.image = QPixmap(image_path)
                self.image = self.image.scaled(1280, 720, QtCore.Qt.KeepAspectRatio)
                self.window_image.setPixmap(self.image)
                self.window_image.setAlignment(Qt.AlignCenter)
                self.file_path.setText(image_path)

    def option_previous1(self):
        if self.button_change_end.text() == "End":
            try:
                image_path = self.iterator1.previous()
                self.image = QPixmap(image_path)
                self.image = self.image.scaled(1280, 720, QtCore.Qt.KeepAspectRatio)
                self.window_image.setPixmap(self.image)
                self.window_image.setAlignment(Qt.AlignCenter)
                self.file_path.setText(image_path)
            except StopIteration:
                self.iterator1.counter += 1
                PopupWindow("Problem", "This action cannot be performed now", "There is no element behind")
            except AttributeError:
                PopupWindow("Problem", "This action cannot be performed now", "There is no element behind")
        if self.button_change_end.text() == "Cycle":
            try:
                image_path = self.iterator1.previous()
                self.image = QPixmap(image_path)
                self.image = self.image.scaled(1280, 720, QtCore.Qt.KeepAspectRatio)
                self.window_image.setPixmap(self.image)
                self.window_image.setAlignment(Qt.AlignCenter)
                self.file_path.setText(image_path)
            except StopIteration:
                self.iterator1.counter = self.iterator1.limit
                image_path = self.iterator1.previous()
                self.image = QPixmap(image_path)
                self.image = self.image.scaled(1280, 720, QtCore.Qt.KeepAspectRatio)
                self.window_image.setPixmap(self.image)
                self.window_image.setAlignment(Qt.AlignCenter)
                self.file_path.setText(image_path)

    def option_previous2(self):
        if self.button_change_end.text() == "End":
            try:
                image_path = self.iterator2.previous()
                self.image = QPixmap(image_path)
                self.image = self.image.scaled(1280, 720, QtCore.Qt.KeepAspectRatio)
                self.window_image.setPixmap(self.image)
                self.window_image.setAlignment(Qt.AlignCenter)
                self.file_path.setText(image_path)
            except StopIteration:
                self.iterator2.counter += 1
                PopupWindow("Problem", "This action cannot be performed now", "There is no element behind")
            except AttributeError:
                PopupWindow("Problem", "This action cannot be performed now", "There is no element behind")
        if self.button_change_end.text() == "Cycle":
            try:
                image_path = self.iterator2.previous()
                self.image = QPixmap(image_path)
                self.image = self.image.scaled(1280, 720, QtCore.Qt.KeepAspectRatio)
                self.window_image.setPixmap(self.image)
                self.window_image.setAlignment(Qt.AlignCenter)
                self.file_path.setText(image_path)
            except StopIteration:
                self.iterator2.counter = self.iterator2.limit
                image_path = self.iterator2.previous()
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
        background-image: url(sources/images/background.jpg);
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