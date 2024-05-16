import sys
import traceback

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from sqlalchemy import select
from database.database import Group, Retweet, Twitter_account, Attachment, User
from gui.login_app import LoginApp
from gui.account_app import AccountApp
from gui.group_app import GroupApp
from gui.message_app import MessageApp
from config import SERVER_LINK
import requests


class MainApp(QMainWindow):
    def __init__(self, session):
        super().__init__()
        self.db = session
        self.settings_change_flag: bool = False  # False - default, True - premium
        self.login: str = str()  # login name
        self.table_item_ignore = True
        self.init_ui()

    def init_ui(self):
        uic.loadUi("main.ui", self)

        # Buttons connect
        self.logout_button.clicked.connect(self.get_authorise)
        self.settings_change_button.clicked.connect(self.change_settings_profile)
        self.disable_button.clicked.connect(self.set_program_activity)
        self.enable_button.clicked.connect(self.set_program_activity)
        self.account_button.clicked.connect(self.add_account)

        self.max_tweets_edit.textChanged.connect(self.set_settings_to_database)
        self.my_retweets_edit.textChanged.connect(self.set_settings_to_database)
        self.cooldown_edit.textChanged.connect(self.set_settings_to_database)
        self.like_chance_edit.textChanged.connect(self.set_settings_to_database)
        self.react_chance_edit.textChanged.connect(self.set_settings_to_database)

        self.account_table.cellPressed.connect(self.cell_separator)
        self.account_table.itemChanged.connect(self.set_account_premium)

        self.set_ui()

    # Section: UI setter ----------------------------------------------------------------

    def set_ui(self):
        user = self.db.execute(select(User).where(User.current_user == 1)).scalar_one_or_none()

        if user:
            self.check_user(user)

            self.set_info_text(user.app_login, user.subscription_expire_date,
                               len(self.db.execute(
                                   select(Twitter_account).where(Twitter_account.user_id == user.id)).scalars().all()))
            self.set_settings_from_database(user.settings[0].max_tweets, user.settings[0].max_retweets,
                                            user.settings[0].period_cooldown_minutes, user.settings[0].like_chance,
                                            user.settings[0].react_chance)
            self.set_table()
            self.set_status_text(True)
        else:
            self.get_authorise()
            self.set_ui()

    def set_info_text(self, login: str = "", expires: str = "", accounts_num: int = 0):
        # Set text in top right

        self.login_label.setText(f"Login {login}")
        self.expires_label.setText(f"Expires {expires}")
        self.account_label.setText(f"Accounts {accounts_num}")

    def set_settings_from_database(self, max_tweets: int, my_retweets: int, cooldown: int, like_chance_edit: int,
                                   react_chance: int):
        # Set settings QLineEdit text like input params

        self.max_tweets_edit.setText(f"{max_tweets}")
        self.my_retweets_edit.setText(f"{my_retweets}")
        self.cooldown_edit.setText(f"{cooldown}")
        self.like_chance_edit.setText(f"{like_chance_edit}")
        self.react_chance_edit.setText(f"{react_chance}")

    def set_table(self):
        # Set table of Twitter accounts to the accounts table

        self.account_table.setColumnCount(7)
        self.account_table.setHorizontalHeaderLabels(
            ["Login", "Proxy", "Groups", "Messages", "Retweets", "Status", "Premium"])

        user = self.db.execute(select(User).where(User.current_user == 1)).scalar_one_or_none()

        if user:

            items = user.twitter_accounts

            self.account_table.setRowCount(len(items))

            for i, d in enumerate(items):
                # При вызове функции повторно, может быть такое что ячейки привязаны к функциям несколько раз, надо чекнуть
                self.table_item_ignore = True
                self.account_table.setItem(i, 0, self.set_item_table(d.auth[0].login))

                self.account_table.setItem(i, 1, self.set_item_table(d.proxy[0].ip))

                temp_table_item = QTableWidgetItem(
                    str(len(self.db.execute(select(Group).where(Group.twitter_account_id == d.id)).scalars().all())))
                temp_table_item.setData(Qt.UserRole, d.id)
                temp_table_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                temp_table_item.setTextAlignment(Qt.AlignCenter)
                self.account_table.setItem(i, 2, temp_table_item)

                self.account_table.setItem(i, 3, self.set_item_table(str(d.stats[0].total_msg_sent_num)))

                self.account_table.setItem(i, 4, self.set_item_table(str(d.stats[0].total_retweets_num)))

                self.account_table.setItem(i, 5, self.set_item_table(d.stats[0].status))

                temp_table_item = QTableWidgetItem()
                temp_table_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                temp_table_item.setData(Qt.UserRole, d.id)
                temp_table_item.setCheckState(Qt.Checked if d.premium else Qt.Unchecked)
                temp_table_item.setTextAlignment(Qt.AlignCenter)
                self.account_table.setItem(i, 6, temp_table_item)  # account id

                self.table_item_ignore = False
        else:
            raise Exception("Unauthorised user before setting table")

    # Section: Button functions ----------------------------------------------------------------

    def set_settings_to_database(self):
        # Set settings from QLineEdit text to DataBase

        def data_validator(val: str, sender_type: str):
            match sender_type:
                case "max_tweets_edit" | "my_retweets_edit":
                    # Tweets and retweets
                    return val.isdigit() and 0 < int(val) < 200
                case "cooldown_edit":
                    # Cooldown
                    return val.isdigit() and 20 < int(val) < 300
                case "like_chance_edit" | "react_chance_edit":
                    # Like and react chance
                    return val.replace(".", "").isdigit() and 0 < float(val) < 100 and val.count(".") < 2

        user = self.db.execute(select(User).where(User.current_user == 1)).scalar_one_or_none()
        settings = user.settings[0]
        sender = self.sender()
        sender_name = sender.objectName()
        sender_text = sender.text()

        if data_validator(sender_text, sender_name):
            sender.setStyleSheet("""
                                QLineEdit {
                                    border: 1px solid #515f75;
                                    border-radius: 6px;
                                    padding: 5px;
                                    background-color: #252e3d;
                                    color: white;
                                }""")
            match sender_name:
                case "max_tweets_edit":
                    if self.settings_change_flag:
                        settings.max_tweets_premium = int(sender_text)
                    else:
                        settings.max_tweets = int(sender_text)
                case "my_retweets_edit":
                    if self.settings_change_flag:
                        settings.max_retweets_premium = int(sender_text)
                    else:
                        settings.max_retweets = int(sender_text)
                case "cooldown_edit":
                    if self.settings_change_flag:
                        settings.period_cooldown_minutes_premium = int(sender_text)
                    else:
                        settings.period_cooldown_minutes_premium = int(sender_text)
                case "like_chance_edit":
                    if self.settings_change_flag:
                        settings.like_chance_premium = float(sender_text)
                    else:
                        settings.like_chance = float(sender_text)
                case "react_chance_edit":
                    if self.settings_change_flag:
                        settings.react_chance_premium = float(sender_text)
                    else:
                        settings.react_chance = float(sender_text)

            self.db.add(settings)
            self.db.commit()
        else:
            sender.setStyleSheet("""
                                QLineEdit {
                                    border: 1px solid #515f75;
                                    border-radius: 6px;
                                    padding: 5px;
                                    background-color: #252e3d;
                                    color: red;
                                }""")

    def change_settings_profile(self):
        # Function for change settings button
        try:
            user = self.db.execute(select(User).where(User.current_user == 1)).scalar_one_or_none()
            if user:
                self.settings_change_flag = not self.settings_change_flag
                settings = user.settings[0]
                if self.settings_change_flag:
                    self.settings_change_label.setText("Settings: Premium")
                    self.set_settings_from_database(settings.max_tweets_premium, settings.max_retweets_premium,
                                                    settings.period_cooldown_minutes_premium,
                                                    settings.like_chance_premium, settings.react_chance_premium)
                else:
                    self.settings_change_label.setText("Settings: Normal")
                    self.set_settings_from_database(settings.max_tweets, settings.max_retweets,
                                                    settings.period_cooldown_minutes, settings.like_chance,
                                                    settings.react_chance)
            else:
                raise Exception("User unauthorised for change settings")
        except Exception as e:
            print(e)

    def set_status_text(self, flag: bool):
        # Set program status text to left corner label

        if flag:
            self.status_lable.setText("Status: Active")
        else:
            self.status_lable.setText("Status: Disable")

    def set_program_activity(self):
        # Set enable/disable to all usable elements, if we add more need to change object_list

        # TODO: fix this
        try:
            sender_flag = self.sender().objectName() == "enable_button"
            object_list = [self.account_table, self.account_button, self.info_table, self.info_button,
                           self.logout_button, self.max_tweets_edit, self.my_retweets_edit, self.cooldown_edit,
                           self.react_chance_edit, self.enable_button if sender_flag else self.disable_button]

            for obj in object_list:
                obj.setEnabled(sender_flag)

            self.set_status_text(sender_flag)
        except Exception as e:
            print(e)

    def get_authorise(self):
        # Get string from login widget
        login_widget = LoginApp(self.db)
        login_widget.exec()

    # Section: Table functions ----------------------------------------------------------------
    def cell_separator(self, row, column):
        try:
            match column:
                case 2:
                    self.group_show(self.account_table.item(row, column).data(Qt.UserRole))
                case 3:
                    self.message_show()
        except Exception:
            traceback.print_exc()

    def set_account_premium(self, item_table):
        if not self.table_item_ignore:
            account_item = self.db.execute(
                select(Twitter_account).where(Twitter_account.id == item_table.data(Qt.UserRole))).scalar_one_or_none()
            print(item_table.data(Qt.UserRole))
            if account_item:
                account_item.premium = not account_item.premium

                self.db.add(account_item)
                self.db.commit()
            else:
                raise Exception("premium checkbox was deleted")

    def group_show(self, item_id):
        # Show table of group for certain twitter acc in the info table

        try:
            self.table_item_ignore = True
            groups = self.db.execute(select(Group).where(Group.twitter_account_id == item_id)).scalars().all()

            self.info_table.setColumnCount(3)
            self.info_table.setHorizontalHeaderLabels(["Link", "Retweets", "Enabled"])
            self.info_table.setRowCount(len(groups))

            for index, item in enumerate(groups):
                self.info_table.setItem(index, 0, self.set_item_table(item.link))

                self.info_table.setItem(index, 1, self.set_item_table(
                    str(len(self.db.execute(select(Retweet).where(Retweet.group_id == item.id)).scalars().all()))))

                temp_table_item = QTableWidgetItem()
                temp_table_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                temp_table_item.setData(Qt.UserRole, item.id)
                temp_table_item.setCheckState(Qt.Checked if item.enabled else Qt.Unchecked)
                self.info_table.setItem(index, 2, temp_table_item)

            self.info_table.disconnect()
            self.info_table.itemChanged.connect(self.group_separator)

            # Set info button to "Add group" and link function
            self.info_button.setText("Add group")
            self.info_button.disconnect()
            self.info_button.clicked.connect(lambda: self.add_group(item_id))
            self.table_item_ignore = False
        except Exception as e:
            print(e)

    def group_separator(self, item_table):
        try:
            if not self.table_item_ignore:
                print(item_table.data(Qt.UserRole))
                group_item = self.db.execute(
                    select(Group).where(Group.id == item_table.data(Qt.UserRole))).scalar_one_or_none()

                if group_item:
                    group_item.enabled = not group_item.enabled

                    self.db.add(group_item)
                    self.db.commit()
                else:
                    raise Exception("Check box for group in info table has not found")
        except Exception as e:
            print(e)

    def message_show(self):
        # Show table of message in the info table

        try:
            self.table_item_ignore = True
            self.info_table.setColumnCount(2)
            self.info_table.setHorizontalHeaderLabels(["Message", "Enabled"])

            message_items = self.db.execute(select(User).where(User.current_user == 1)).scalar_one_or_none()

            if message_items:
                message_items = message_items.attachments
                self.info_table.setRowCount(len(message_items))
                for index, item in enumerate(message_items):
                    self.info_table.setItem(index, 0,
                                            self.set_item_table(item.text if item.is_text else item.attachment_path))

                    temp_table_item = QTableWidgetItem()
                    temp_table_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                    temp_table_item.setData(Qt.UserRole, item.id)
                    temp_table_item.setCheckState(Qt.Checked if item.enabled else Qt.Unchecked)
                    self.info_table.setItem(index, 1, temp_table_item)

                self.info_table.disconnect()
                self.info_table.itemChanged.connect(self.message_separator)
            else:
                raise Exception("Messages can`t be loaded due to unacceptable login")

            # Set info_button text to "Add message" and connect function
            self.info_button.setText("Add message")
            self.info_button.disconnect()
            self.info_button.clicked.connect(self.add_message)
            self.table_item_ignore = False
        except Exception as e:
            print(e)

    def message_separator(self, item_table):
        try:
            if not self.table_item_ignore:
                print(item_table.data(Qt.UserRole))
                message_item = self.db.execute(
                    select(Attachment).where(Attachment.id == item_table.data(Qt.UserRole))).scalar_one_or_none()

                if message_item:
                    message_item.enabled = not message_item.enabled

                    self.db.add(message_item)
                    self.db.commit()
                else:
                    raise Exception("Check box for message in info table has not found")
        except Exception as e:
            print(e)

    def add_account(self):
        try:
            account_app = AccountApp(self.db)
            account_app.exec_()
            self.set_table()
        except Exception as e:
            print(e)

    def add_group(self, twitter_account_id: int):
        try:
            group_app = GroupApp(self.db, twitter_id=twitter_account_id)
            group_app.exec_()
            self.group_show(item_id=twitter_account_id)
            self.set_table()
        except Exception as e:
            print(e)

    def add_message(self):
        try:
            message_app = MessageApp(self.db)
            message_app.exec_()
            self.message_show()
            self.set_table()
        except Exception as e:
            print(e)

    # Section: Server response -------------------------------------------------------
    def check_user(self, user):

        # TODO: change to real response
        try:
            response = requests.get(f"{SERVER_LINK}/api/auth?login={user.app_login}&passwd_hash={user.app_password}")
            if response.ok:
                response = response.json()
                if response.get("exists"):
                    user.subscription_expire_date = int(response.get("will_be_expired_after"))

                    if user.subscription_expire_date <= 0:
                        msg_box = QMessageBox()
                        msg_box.setIcon(QMessageBox.Information)
                        msg_box.setText("Your trial was expired")
                        msg_box.setWindowTitle("Trial expired")
                        msg_box.setStandardButtons(QMessageBox.Ok)
                        msg_box.exec()
                        self.get_authorise()
                else:
                    self.get_authorise()
        except Exception as e:
            print(e)
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setText("Can't connect to the server, check your internet")
            msg_box.setWindowTitle("Network error")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()
            sys.exit()

    # Sector: Static functions ------------------------------------------------------
    @staticmethod
    def set_item_table(var):
        item_table = QTableWidgetItem(var)
        item_table.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        item_table.setTextAlignment(Qt.AlignCenter)
        return item_table
