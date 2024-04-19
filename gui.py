import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt5.QtCore import pyqtSignal


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = None  # data base
        self.path_db: str = str()  # db path
        self.settings_change_flag: bool = False  # False - default, True - premium
        self.login: str = str() # login name
        self.initUI()

    def initUI(self):
        uic.loadUi("main.ui", self)

    def set_info_text(self):
        # Set text in top right
        # TODO: change number in f-string to real values

        self.login_label.setText(f"Login {123}")
        self.expires_label.setText(f"Expires {123}")
        self.account_label.setText(f"Account {123}")

    def set_settings_text(self, max_tweets: int, my_retweets: int, cooldown: int, like_chance_edit: int,
                          react_chance: int):
        # Set settings QLineEdit text like input params

        self.max_tweets_edit.setText(f"{max_tweets}")
        self.my_retweets_edit.setText(f"{my_retweets}")
        self.cooldown_edit.setText(f"{cooldown}")
        self.like_chance_edit.setText(f"{like_chance_edit}")
        self.react_chance_edit.setText(f"{react_chance}")

    def set_settings_database(self):
        # Set settings from QLineEdit text to DataBase
        # TODO: change pass to real db request

        sender_name = self.sender().objectName()
        match sender_name:
            case "max_tweets_edit":
                if self.settings_change_flag:
                    # db set premium
                    pass
                else:
                    # db set default
                    pass
            case "my_retweets_edit":
                if self.settings_change_flag:
                    # db set premium
                    pass
                else:
                    # db set default
                    pass
            case "cooldown_edit":
                if self.settings_change_flag:
                    # db set premium
                    pass
                else:
                    # db set default
                    pass
            case "like_chance_edit":
                if self.settings_change_flag:
                    # db set premium
                    pass
                else:
                    # db set default
                    pass
            case "react_chance_edit":
                if self.settings_change_flag:
                    # db set premium
                    pass
                else:
                    # db set default
                    pass

    def change_settings_profile(self):
        # Function for change settings button

        if self.settings_change_flag:
            self.settings_change_label.setText("Settings: Premium")
        else:
            self.settings_change_label.setText("Settings: Normal")

        self.settings_change_flag = not self.settings_change_flag

    def set_status_text(self, flag: bool):
        # Set program status text to left corner label

        if flag:
            self.status_label.setText("Status: Active")
        else:
            self.status_label.setText("Status: Disable")

    def set_program_activity(self):
        # Set enable/disable to all usable elements, if we add more need to change object_list

        sender_flag = self.sender().objectName() == "enable_button"
        object_list = [self.account_table, self.account_button, self.message_table, self.message_button,
                       self.logout_button, self.max_tweets_edit, self.my_retweets_edit, self.cooldown_edit,
                       self.react_chance_edit, self.enable_button if sender_flag else self.disable_button]

        for obj in object_list:
            obj.setEnabled(sender_flag)

        self.set_status_text(sender_flag)

    def receive_login(self, login):
        # Function for connection to signal from login widget
        # TODO: write right request
        self.login = login
        # get some values from db
        self.set_info_text()

    def get_authorise(self):
        # Get string from login widget
        # TODO: write request

        if not self.login:
            login_widget = LoginApp()
            login_widget.info_signal.connect(self.receive_login)
            login_widget.exec_()
        else:
            # request to db for changing all staff
            pass





class LoginApp(QWidget):
    info_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
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
                print(e)
            finally:
                self.error_label.setText("Can't connect to the server, check your internet")






if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())


