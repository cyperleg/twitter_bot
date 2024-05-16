from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QFileDialog
from sqlalchemy import select
from database.database import User, Attachment
import csv


class MessageApp(QDialog):
    def __init__(self, db):
        super().__init__()
        self.init_ui()
        self.db = db

    def init_ui(self):
        uic.loadUi("messages.ui", self)

        self.image_button.clicked.connect(self.import_image)
        self.text_button.clicked.connect(self.import_text)

    def import_text(self):
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

                    user_id = self.db.execute(select(User).where(User.current_user == 1)).scalar_one_or_none()
                    if user_id:
                        user_id = user_id.id
                    else:
                        raise Exception("User was undefined for message")

                    for text in reader:
                        text = Attachment(user_id=user_id, is_text=1, text=text[0], enabled=1)
                        self.db.add(text)
                        self.db.commit()
                self.close()
            else:
                raise Exception("File was not chosen")
        except Exception as e:
            print(e)

    def import_image(self):
        try:
            file_dialog = QFileDialog(self)
            file_dialog.setWindowTitle("Choose file")
            file_dialog.setFileMode(QFileDialog.ExistingFile)
            file_dialog.setNameFilter("PNG Files (*.png);;JPG Files (*.jpg);;JPEG Files (*.jpeg)")

            file = None

            if file_dialog.exec_():
                file = file_dialog.getOpenFileName()[0]

            if file:
                user_id = self.db.execute(select(User).where(User.current_user == 1)).scalar_one_or_none().id
                attachment = Attachment(user_id=user_id, is_text=0, attachment_path=file, enabled=1)
                self.db.add(attachment)
                self.db.commit()
                self.close()
            else:
                raise Exception("File was not chosen")
        except Exception as e:
            print(e)
