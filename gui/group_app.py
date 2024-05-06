from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QFileDialog
from database.database import Group
import csv


class GroupApp(QWidget):
    TWITTER_START = "https://twitter.com/"

    def __init__(self, db, group: list = None, twitter_id: int = None):
        super().__init__()
        self.init_ui()
        self.db = db
        self.group = group
        self.twitter_id = twitter_id

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
            file = file_dialog.selectedFile()

        if file:
            with open(file, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')

                if self.group:
                    for link in reader:
                        if link[0].startswith(self.TWITTER_START):
                            self.group.append(Group(link=link[0]))
                elif self.twitter_id:
                    for link in reader:
                        if link[0].startswith(self.TWITTER_START):
                            self.group.append(Group(twitter_account_id=self.twitter_id, link=link[0]))
        else:
            raise Exception("File was not chosen")
