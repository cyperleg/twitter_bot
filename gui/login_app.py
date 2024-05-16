import sys

import requests
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from werkzeug.security import generate_password_hash
from sqlalchemy import select
from database.database import User, Settings
from config import SERVER_LINK


class LoginApp(QDialog):
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

        try:
            if not login or not password:
                self.error_label.setText("Incorrect login or password")
            else:
                # try to get response from server

                # TODO: change to real response
                response = requests.get(
                    f"{SERVER_LINK}/api/auth?login={login}&passwd_hash={password}")

                if response.ok:
                    response = response.json()
                    print(response)
                    if response.get("exists"):

                        user = self.db.execute(select(User).where(User.app_login == login)).scalar_one_or_none()

                        if user:
                            user.current_user = 1
                            self.close()
                        else:
                            user = User(current_user=1, app_login=login, app_password=password,
                                        subscription_expire_date=int(response.get("will_be_expired_after")))
                            self.db.add(user)
                            self.db.commit()

                            user = self.db.execute(select(User).where(User.current_user == 1)).scalar_one_or_none()

                            settings = Settings(user_id=user.id, max_tweets=50, max_tweets_premium=50, max_retweets=5,
                                                max_retweets_premium=5, period_cooldown_minutes=30,
                                                period_cooldown_minutes_premium=30, like_chance=1,
                                                like_chance_premium=1, react_chance=20, react_chance_premium=20,
                                                action_delay_seconds=response.get("settings").get(
                                                    "action_delay_seconds"),
                                                normal_acc_retweets_cap=response.get("settings").get(
                                                    "normal_acc_retweets_cap"),
                                                premium_acc_retweets_cap=response.get("settings").get(
                                                    "premium_acc_retweets_cap"))
                            self.db.add(settings)
                            self.db.commit()

                        self.close()
                    else:
                        self.error_label.setText(f"{response.get('error')}")
                else:
                    self.error_label.setText("Can't connect to the server, check your internet")
        except Exception as e:
            print(e)

    def closeEvent(self, event):
        if event.spontaneous():
            sys.exit()
