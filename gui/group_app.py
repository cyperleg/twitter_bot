from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QFileDialog
import csv


class GroupApp(QWidget):
    def __init__(self, db, group):
        super().__init__()
        self.init_ui()
        self.db = db
        self.group = group

    def init_ui(self):
        uic.loadUi("groups.ui", self)

        self.import_button.clicked.connect(self.import_csv)

    def import_csv(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Choose file")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("CSV Files (*.csv)")

        file = None

        if file_dialog.exec_():
            file = file_dialog.selectFile()

        if file:
            with open(file, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)

                for row in reader:
                    # TODO: create data validator
                    group_link = row[0]
                    account_number = row[1]
                    # TODO: commit to db
        else:
            raise Exception("File was not chosen")