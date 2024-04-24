import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidgetItem, QCheckBox
from PyQt5.QtCore import pyqtSignal
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from database.database import Group, Retweet, Twitter_account, Attachment, User
from sqlalchemy import select


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Session(create_engine(self.path_db))  # data base
        self.path_db: str = str()  # db path
        self.settings_change_flag: bool = False  # False - default, True - premium
        self.login: str = str()  # login name
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

    def set_table(self):
        # Set table of twitter accounts to the accounts table

        def set_account_premium():
            sender = self.sender()
            check_box_id = int(sender.objectName()[18:])
            account_item = self.db.execute(
                select(Twitter_account).where(Twitter_account.id == check_box_id).scalar_one_or_none())

            if account_item:
                account_item.premium = sender.isChecked()
                self.db.commit()
            else:
                raise Exception("Check box for twitter account in account table has not found")

        self.account_table.setColumnCount(7)
        self.account_table.setHorizontalHeaderLabel(
            ["Login", "Proxy", "Groups", "Messages", "Retweets", "Status", "Premium"])

        if not self.login:
            items = self.db.execute(select(User).where(User.app_login == self.login).scalar_one_or_none())

            if items:
                items = items.twitter_accounts

                for i, d in enumerate(items):
                    self.account_table.setItem(i, 0, QTableWidgetItem(d.auth.login))

                    self.account_table.setItem(i, 1, QTableWidgetItem(d.proxy.ip))

                    self.account_table.setItem(i, 2, QTableWidgetItem(
                        len(self.db.execute(select(Group).where(Group.twitter_account_id == d.id)).scalars().all())
                    ))
                    self.account_table.item(i, 2).setObjectName(f"table_item_group_{d.id}")
                    self.account_table.item(i, 2).itemClicked.connect(self.group_show)

                    self.account_table.setItem(i, 3, QTableWidgetItem(d.stats.total_msg_sent_num))
                    self.account_table.item(i, 3).setObjectName(f"table_item_message_{d.id}")
                    self.account_table.item(i, 3).itemClicked.connect(self.message_show)

                    self.account_table.setItem(i, 4, QTableWidgetItem(d.stats.total_retweets_num))

                    self.account_table.setItem(i, 5, QTableWidgetItem(d.stats.status))

                    check_box = QCheckBox()
                    check_box.setChecked(True if d.premium else False)
                    check_box.stateChanged.connect(set_account_premium)
                    self.account_table.setItem(i, 6, check_box)
                    self.account_table.item(i, 6).setObjectName(f"table_item_premium_{d.id}")  # account id
            else:
                raise Exception("Unexpected login to load twitter accounts")

    def group_show(self):
        # Show table of group for certain twitter acc in the info table

        def set_group_enable():
            sender = self.sender()
            check_box_id = int(sender.objectName()[24:])
            group_item = self.db.execute(select(Group).where(Group.id == check_box_id).scalar_one_or_none())

            if group_item:
                group_item.enabled = sender.isChecked()
                self.db.commit()
                # sender.setChecked(not sender.isChecked()) # if it wont be automatic
            else:
                raise Exception("Check box for group in info table has not found")

        item_id = int(self.sender().objectName()[17:])  # twitter id
        groups = self.db.execute(select(Group).where(Group.twitter_account_id == item_id).scalars().all())

        self.info_table.setColumnCount(3)
        self.info_table.setHorizontalHeaderLabel(["Link", "Retweets", "Enabled"])

        for index, item in enumerate(groups):
            self.info_table.setItem(index, 0, QTableWidgetItem(item.link))

            self.info_table.setItem(index, 1, QTableWidgetItem(
                len(self.db.execute(select(Retweet).where(Retweet.group_id == item.id)).scalars().all())
            ))

            check_box = QCheckBox()
            check_box.setChecked(True if item.enables else False)
            check_box.stateChanged.connect(set_group_enable)
            self.info_table.setItem(index, 2, check_box)
            self.info_table.item(index, 2).setObjectName(f"table_item_group_enabled_{item.id}")  # group id

    def message_show(self):
        # Show table of message in the info table

        def set_message_enable():
            sender = self.sender()
            check_box_id = int(sender.objectName()[25:])
            message_item = self.db.execute(select(Attachment).where(Attachment.id == check_box_id).scalar_one_or_none())

            if message_item:
                message_item.enabled = sender.isChecked()
                self.db.commit()
                # sender.setChecked(not sender.isChecked()) # if it wont be automatic
            else:
                raise Exception("Check box for group in info table has not found")

        self.info_table.setColumnCount(2)
        self.info_table.setHorizontalHeaderLabel(["Message", "Enabled"])

        message_items = self.db.execute(select(User).where(User.app_login == self.login).scalar_one_or_none())

        if message_items:
            message_items = message_items.attachments
            for index, item in enumerate(message_items):
                self.info_table.setItem(index, 0, QTableWidgetItem(item.text if item.is_text else item.image_path))

                check_box = QCheckBox()
                check_box.setChecked(True if item.enables else False)
                check_box.stateChanged.connect(set_message_enable)
                self.info_table.setItem(index, 1, check_box)
                self.info_table.item(index, 1).setObjectName(f"table_item_message_enabled{item.id}")  # message id
        else:
            raise Exception("Messages can`t be loaded due to unacceptable login")




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
                self.error_label.setText("Can't connect to the server, check your internet")
                print(e)
            finally:
                print("CUMCUMCUMCUMCUMCUMCUMCUMCUMCUMCUMCUMCUMCUMCUMCUMCUMCUMCUMCUMCUM")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
