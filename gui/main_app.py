from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QCheckBox
from sqlalchemy import select
from database.database import Group, Retweet, Twitter_account, Attachment, User
from login_app import LoginApp
from account_app import AccountApp
from group_app import GroupApp
from message_app import MessageApp


class MainApp(QMainWindow):
    def __init__(self, session):
        super().__init__()
        self.db = session
        self.settings_change_flag: bool = False  # False - default, True - premium
        # self.login: str = str()  # login name
        self.init_ui()

    def init_ui(self):
        uic.loadUi("main.ui", self)

        # Buttons connect
        self.logout_button.clicked.connect(self.get_authorise)
        self.settings_change_button.clicked.connect(self.change_settings_profile)
        self.disable_button.clicked.connect(self.set_program_activity)
        self.account_button.clicked.connect(self.add_account)

        self.set_ui()

    # Section: UI setter ----------------------------------------------------------------

    def set_ui(self):
        user = self.db.execute(select(User).where(User.current_user == 1).scalar_one_or_none())
        if user:
            self.set_info_text(user.app_login, user.subscription_expire_date,
                               len(self.db.execute(select(User).where(User.id == user.id)).scalars().all()))
            self.set_settings_text(user.settings.max_tweets, user.settings.max_retweets,
                                   user.settings.period_cooldown_minutes, user.settings.like_chance,
                                   user.settings.react_chance)
            self.set_table()
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

        user = self.db.execute(select(User).where(User.current_user == 1).scalar_one_or_none())

        if user:
            items = user.twitter_accounts

            for i, d in enumerate(items):
                self.account_table.setItem(i, 0, QTableWidgetItem(d.auth.login))

                self.account_table.setItem(i, 1, QTableWidgetItem(d.proxy.ip))

                self.account_table.setItem(i, 2, QTableWidgetItem(
                    len(self.db.execute(select(Group).where(Group.twitter_account_id == d.id)).scalars().all())
                ))
                self.account_table.item(i, 2).setObjectName(f"table_item_group_{d.id}")
                self.account_table.item(i, 2).itemClicked.connect(self.group_show)

                self.account_table.setItem(i, 3, QTableWidgetItem(d.stats.total_msg_sent_num))
                self.account_table.item(i, 3).itemClicked.connect(self.message_show)

                self.account_table.setItem(i, 4, QTableWidgetItem(d.stats.total_retweets_num))

                self.account_table.setItem(i, 5, QTableWidgetItem(d.stats.status))

                check_box = QCheckBox()
                check_box.setChecked(True if d.premium else False)
                check_box.stateChanged.connect(set_account_premium)
                self.account_table.setItem(i, 6, check_box)
                self.account_table.item(i, 6).setObjectName(f"table_item_premium_{d.id}")  # account id
        else:
            raise Exception("Unauthorised user before setting table")

    # Section: Button functions ----------------------------------------------------------------

    def set_settings_to_database(self):
        # Set settings from QLineEdit text to DataBase
        # TODO: validate data first

        user = self.db.execute(select(User).where(User.current_user == 1).scalar_one_or_none())
        settings = user.settings
        sender = self.sender()
        sender_name = sender.objectName()
        sender_text = sender.text()

        match sender_name:
            case "max_tweets_edit":
                if self.settings_change_flag:
                    settings.max_tweets_premium = sender_text
                else:
                    settings.max_tweets = sender_text
            case "my_retweets_edit":
                if self.settings_change_flag:
                    settings.max_retweets_premium = sender_text
                else:
                    settings.max_retweets = sender_text
            case "cooldown_edit":
                if self.settings_change_flag:
                    settings.period_cooldown_minutes_premium = sender_text
                else:
                    settings.period_cooldown_minutes_premium = sender_text
            case "like_chance_edit":
                if self.settings_change_flag:
                    settings.like_chance_premium = sender_text
                else:
                    settings.like_chance = sender_text
            case "react_chance_edit":
                if self.settings_change_flag:
                    settings.react_chance_premium = sender_text
                else:
                    settings.react_chance = sender_text

    def change_settings_profile(self):
        # Function for change settings button
        user = self.db.execute(select(User).where(User.current_user == 1).scalar_one_or_none())
        if user:
            self.set_settings_to_database()
            if self.settings_change_flag:
                self.settings_change_label.setText("Settings: Premium")
                self.set_settings_text(user.settings.max_tweets_premium, user.settings.max_retweets_premium,
                                       user.settings.period_cooldown_minutes_premium, user.settings.like_chance_premium,
                                       user.settings.react_chance_premium)
            else:
                self.settings_change_label.setText("Settings: Normal")
                self.set_settings_text(user.settings.max_tweets, user.settings.max_retweets,
                                       user.settings.period_cooldown_minutes, user.settings.like_chance,
                                       user.settings.react_chance)

            self.settings_change_flag = not self.settings_change_flag
        else:
            raise Exception("User unauthorised for change settings")

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

    def get_authorise(self):
        # Get string from login widget
        login_widget = LoginApp(self.db)
        login_widget.exec_()

    # Section: Table functions ----------------------------------------------------------------
    def group_show(self, item_id=-1):
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

        item_id = int(self.sender().objectName()[17:]) if item_id == -1 else item_id  # twitter id
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

        # Set info button to "Add group" and link function
        self.info_button.setText("Add group")
        self.info_button.clicked.connect(self.add_group(item_id))

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

        # Set info_button text to "Add message" and connect function
        self.info_button.setText("Add message")
        self.info_button.clicked.connect(self.add_message)

    def add_account(self):
        account_app = AccountApp(self.db)
        account_app.exec_()
        self.set_table()

    def add_group(self, twitter_account_id: int):
        group_app = GroupApp(self.db)
        group_app.exec_()
        self.group_show(item_id=twitter_account_id)

    def add_message(self):
        message_app = MessageApp(self.db)
        message_app.exec_()
        self.message_show()
