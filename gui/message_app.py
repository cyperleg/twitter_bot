from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QFileDialog
from sqlalchemy import select
from database.database import User, Attachment
import csv


class MessageApp(QWidget):
    def __init__(self, db):
        super().__init__()
        self.init_ui()
        self.db = db

    def init_ui(self):
        uic.loadUi("messages.ui", self)

        self.csv_button.clicked.connect(self.import_text)

    def import_text(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Choose file")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("CSV Files (*.csv)")

        file = None

        if file_dialog.exec_():
            file = file_dialog.selectedFile()

        if file:
            with open(file, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)

                for text in reader:
                    user_id = self.db.execute(select(User).where(User.current_user == 1).scalar_one_or_none()).id
                    text = Attachment(user_id=user_id, is_text=1, text=text[0])
                    self.db.add(text)
                    self.db.commit()
        else:
            raise Exception("File was not chosen")

    def import_image(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Choose file")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("PNG Files (*.png);;JPG Files (*.jpg);;JPEG Files (*.jpeg)")

        file = None

        if file_dialog.exec_():
            file = file_dialog.getOpenFileName()[0]

        if file:
            user_id = self.db.execute(select(User).where(User.current_user == 1).scalar_one_or_none()).id
            attachment = Attachment(user_id=user_id, is_text=0, attachment_path=file)
            self.db.add(attachment)
            self.db.commit()
        else:
            raise Exception("File was not chosen")
