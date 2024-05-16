from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QFileDialog
from database.database import Group
import csv


class GroupApp(QDialog):
    TWITTER_START = "https://twitter.com/"

    def __init__(self, db, twitter_id: int = None):
        super().__init__()
        self.init_ui()
        self.db = db
        self.twitter_id = twitter_id

    def init_ui(self):
        uic.loadUi("groups.ui", self)

        self.import_button.clicked.connect(self.import_csv)

    def import_csv(self):
        try:
            file_dialog = QFileDialog(self)
            file_dialog.setWindowTitle("Choose file")
            file_dialog.setFileMode(QFileDialog.ExistingFile)
            file_dialog.setNameFilter("CSV Files (*.csv)")

            file = None

            if file_dialog.exec_():
                file = file_dialog.selectedFiles()[0]

            if file:
                with open(file, 'r', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')

                    for text in reader:
                        if text[0].startswith(self.TWITTER_START):
                            self.db.add(Group(twitter_account_id=self.twitter_id, link=text[0], enabled=1))
                            self.db.commit()
                self.close()

            else:
                raise Exception("File was not chosen")
        except Exception as e:
            print(e)
