from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
import re
from database.database import Proxy, Twitter_account, Auth, User
from sqlalchemy import select
from gui.group_app import GroupApp


class AccountApp(QWidget):
    info_signal = pyqtSignal(str)

    def __init__(self, db):
        super().__init__()
        self.init_ui()
        self.is_password: bool = True
        self.proxy_type: str = str()
        self.db = db
        self.groups = list()

    def init_ui(self):
        uic.loadUi("account.ui", self)

        # Connect to radio buttons function that changes account login
        self.password_check.toggled.connect(self.button_password)
        self.token_check.toggled.connect(self.button_token)

        # Connect to radio buttons changes the proxy type
        self.http_button.toggled.connect(self.http_button)
        self.https_button.toggled.connect(self.https_button)
        self.socks5_button.toggled.connect(self.socks5_button)

        # Connect lineEdit to change text color to white
        self.proxy_edit.textChanged.connect(self.on_change_text)
        self.port_edit.textChanged.connect(self.on_change_text)

        # Connect group button
        self.group_button.clicked.connect(self.group_add_button)

    def button_password(self):
        self.edit_label.setText("Password:")
        self.is_password = True

    def button_token(self):
        self.edit_label.setText("Token:")
        self.is_password = False

    def http_button(self):
        self.proxy_type = "HTTP"

    def https_button(self):
        self.proxy_type = "HTTPS"

    def socks5_button(self):
        self.proxy_type = "SOCKS5"

    def group_add_button(self):
        group_app = GroupApp(self.db, group=self.groups)
        group_app.exec_()

    def on_change_text(self):
        self.sender().setStyleSheet("""
                            QLineEdit {
                                border: 1px solid #515f75;
                                border-radius: 6px;
                                padding: 5px;
                                background-color: #252e3d;
                            }""")

    def confirm(self):
        # Function to confirm account adding

        proxy_regex = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
        port_regex = re.compile(r"^(?:\d{4}|\d{5})$")

        login = self.login_edit.text()
        auth = self.edit_edit.text()
        premium = self.premium_check().isChecked()
        proxy = self.proxy_edit.text()
        port = self.port_edit.text()

        if not proxy_regex.match(proxy):
            self.proxy_edit.setStyleSheet("""
                                QLineEdit {
                                    border: 1px solid #515f75;
                                    border-radius: 6px;
                                    padding: 5px;
                                    background-color: #252e3d;
                                    color: red;
                                }""")
        elif not port_regex.match(port):
            self.port_edit.setStyleSheet("""
                                            QLineEdit {
                                                border: 1px solid #515f75;
                                                border-radius: 6px;
                                                padding: 5px;
                                                background-color: #252e3d;
                                                color: red;
                                            }""")
        else:
            # TODO: check this bd commit
            user_id = self.db.execute(select(User).where(User.current_user == 1).scalar_one_or_none()).id
            new_account = Twitter_account(user_id=user_id, premium=premium,
                                          auth=Auth(login=login, password=auth if self.is_password else None,
                                                    auth=None if self.is_password else auth),
                                          proxy=Proxy(ip=proxy, port=port, type=self.proxy_type))
            self.db.add(new_account)
            self.db.commit()
            for item in self.groups:
                item.twitter_account_id = new_account.id
                self.db.add(item)
                self.db.commit()
