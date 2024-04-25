from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget


class LoginApp(QWidget):
    info_signal = pyqtSignal(str)

    def __init__(self, db):
        super().__init__()
        self.init_ui()
        self.db = db

    def init_ui(self):
        uic.loadUi("login.ui", self)

        self.confirm_button.clicked.connect(self.login)

    def login(self):
        # Function to authorise, return string to mainApp

        login = self.login_edit.text()
        password = self.password_edit.text()

        if not login or not password:
            self.error_label.setText("Incorrect login or password")
        else:
            try:
                # try to get responce from server
                self.info_signal.emit(f"{login}")
                self.close()
            except Exception as e:
                self.error_label.setText("Can't connect to the server, check your internet")
                print(e)
            finally:
                # TODO: change this)
                print("CUMCUMCUMCUMCUMCUMCUMCUMCUMCUMCUMCUMCUMCUMCUMCUMCUMCUMCUMCUMCUM")
