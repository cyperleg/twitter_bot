from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget


class AccountApp(QWidget):
    info_signal = pyqtSignal(str)

    def __init__(self, db):
        super().__init__()
        self.init_ui()
        self.is_password: bool = True
        self.proxy_type: str = str()
        self.db = db

    def init_ui(self):
        uic.loadUi("account.ui", self)

        # Connect to radio buttons function that changes account login
        self.password_check.toggled.connect(self.button_password)
        self.token_check.toggled.connect(self.button_token)

        # Connect to radio buttons changes the proxy type
        self.http_button.toggled.connect(self.http_button)
        self.https_button.toggled.connect(self.https_button)
        self.socks5_button.toggled.connect(self.socks5_button)

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

    def confirm(self):
        # TODO: create input data validator
        # Function to confirm account adding
        login = self.login_edit.text()
        auth = self.edit_edit.text()
        premium = self.premium_check().isChecked()
        proxy = self.proxy_edit.text()
        port = self.port_edit.text()

        # separator -> ;  login, auth(psw or token), auth type, premium flag, proxy, port, proxy type
        self.info_signal.emit(f"{login};{auth};{self.is_password};{premium};{proxy};{port};{self.proxy_type}")