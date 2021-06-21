import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from resources import design
import os
from string import ascii_uppercase

drive_letter = ""


class EmulateApp(QtWidgets.QMainWindow, design.Ui_MainWindow):

    # # # Variables # # #
    font = QtGui.QFont()
    font.setFamily("Arial")
    font.setPointSize(10)
    folder = ""

    # # # Main # # #
    def __init__(self):
        # Accessing variables from the "design.py" file
        super().__init__()
        self.setupUi(self)  # Design initialization
        # Folder
        self.folderButton.clicked.connect(self.setFolder)
        # On/Off
        self.buttonOn.setEnabled(False)
        self.buttonOff.setEnabled(False)
        self.buttonOn.clicked.connect(lambda: self.emulate("On"))
        self.buttonOff.clicked.connect(lambda: self.emulate("Off"))

    # # # Commands # # #

    def setFolder(self):
        folder = str(QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Folder", "./"))
        self.folder = folder
        # Folder selected
        if self.folder:
            self.statusText.setText("Not created")
            self.statusText.setFont(self.font)
            self.statusText.setStyleSheet("color:red")
            self.folderText.setText(self.folder)
            self.buttonOn.setEnabled(True)

    def emulate(self, index):
        global drive_letter
        
        if index == "On":
            # Checking if the disk is created
            if drive_letter != "":
                os.system(f"subst {drive_letter}: /d")
            else:
                # Selection of a free drive letter
                for letter in ascii_uppercase:
                    if os.path.isdir(f"{letter}:/"):
                        continue
                    else:
                        drive_letter = letter
                        break

            # CREATE AN EMULATED DISC
            try:
                os.system(f'subst {drive_letter}: "{self.folder}"')
                if os.path.isdir(f"{drive_letter}:/"):
                    self.statusText.setText("Success")
                    self.statusText.setStyleSheet("color:green")
                    self.statusText.setFont(self.font)
                    self.buttonOn.setEnabled(False)
                    self.buttonOff.setEnabled(True)
                else:
                    self.statusText.setText("Error. Check a folder path")
                    self.statusText.setStyleSheet("color:red")
                    self.statusText.setFont(self.font)
                    self.buttonOn.setEnabled(False)
                    self.buttonOff.setEnabled(True)
            except Exception as ex:
                self.statusText.setText(f"Error. Description: {ex}")
                self.statusText.setStyleSheet("color:red")
                self.statusText.setFont(self.font)

        elif index == "Off":
            # DELETE EMULATED DISC
            try:
                os.system(f"subst {drive_letter}: /d")
                self.statusText.setText("Drive remove")
                self.statusText.setFont(self.font)
                self.statusText.setStyleSheet("color:gray")
                self.buttonOn.setEnabled(False)
                self.buttonOff.setEnabled(False)
            except Exception as ex:
                self.statusText.setText(f"Error. Description: {ex}")
                self.statusText.setStyleSheet("color:red")
                self.statusText.setFont(self.font)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = EmulateApp()
    window.show()
    app.exec_()
    # The "exit" command deletes the created disk
    if QtGui.QCloseEvent:
        if os.path.isdir(f"{drive_letter}:/"):
            os.system(f"subst {drive_letter}: /d")


if __name__ == '__main__':
    main()
