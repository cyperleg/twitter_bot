import requests
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from werkzeug.security import generate_password_hash
from sqlalchemy import select
from database.database import User


class LoginApp(QWidget):
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
            # try to get response from server

            # TODO: change to real response
            response = requests.get(
                f"localhost:5000/api/auth?login={login}&passwd_hash={generate_password_hash(password)}")

            if response.ok:
                response = response.json()
                if response.get("exists") == "True":

                    user = self.db.execute(select(User).where(User.app_login == login).scalar_one_or_none())

                    if user:
                        user.current_user = 1
                    else:
                        user = User(current_user=1, app_login=login, app_password=generate_password_hash(password),
                                    subscription_expire_date=int(response.get("will_be_expired_after")))
                        self.db.add(user)
                        self.db.commit()

                    self.close()
                else:
                    self.error_label.setText("Login and password aren`t match")
            else:
                self.error_label.setText("Can't connect to the server, check your internet")
