from sqlalchemy import ForeignKey
from sqlalchemy import Integer, Text, REAL
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    id = mapped_column(Integer, primary_key=True, unique=True)
    app_login = mapped_column(Text, unique=True)
    app_password = mapped_column(Text)
    subscription_expire_date = mapped_column(Integer)
    attachments = relationship('Attachment', backref='user', cascade="all, delete", passive_deletes=False)
    settings = relationship('Settings', backref='user', cascade="all, delete", passive_deletes=False)
    twitter_accounts = relationship('Twitter_account', backref='user', cascade="all, delete", passive_deletes=False)

    def __repr__(self):
        return("------------------------USER------------------------\n"+
              "{0: <30} {1: <30}\n".format("User id:", self.id)+
              "{0: <30} {1: <30}\n".format("app_login:", self.app_login)+
              "{0: <30} {1: <30}\n".format("app_password:", self.app_password)+
              "{0: <30} {1: <30}\n".format("subscription_expire_date:", self.subscription_expire_date)+
              "{0: <30} {1: <30}\n".format("attachments num:", len(self.attachments))+
              "{0: <30} {1: <30}\n".format("twitter_accounts num:", len(self.twitter_accounts))+
              "{0: <30} {1: <30}\n".format("settings num:", len(self.settings))+
              "-----------------------------------------------------")


class Attachment(Base):
    __tablename__ = "attachment"
    id = mapped_column(Integer, primary_key=True, unique=True)
    user_id = mapped_column(Integer, ForeignKey('user.id', ondelete="CASCADE"))
    is_text = mapped_column(Integer)
    text = mapped_column(Text)
    attachment_path = mapped_column(Text)

    def __repr__(self):
        return("---------------------ATTACHMENT---------------------\n"+
              "{0: <30} {1: <30}\n".format("Attachment id:", self.id)+
              "{0: <30} {1: <30}\n".format("user_id:", self.user_id)+
              "{0: <30} {1: <30}\n".format("is_text:", self.is_text)+
              "{0: <30} {1: <30}\n".format("text:", self.text if self.text else " ")+
              "{0: <30} {1: <30}\n".format("attachment_path:", self.attachment_path if self.attachment_path else " ")+
              "-----------------------------------------------------")


class Settings(Base):
    __tablename__ = "settings"
    id = mapped_column(Integer, primary_key=True, unique=True)
    user_id = mapped_column(Integer, ForeignKey('user.id'))
    max_tweets = mapped_column(Integer)
    max_retweets = mapped_column(Integer)
    period_cooldown_minutes = mapped_column(Integer)
    linke_chance = mapped_column(REAL)
    react_chance = mapped_column(REAL)
    action_delay_seconds = mapped_column(Integer)      # Data got from server
    normal_acc_retweets_cap = mapped_column(Integer)   # Data got from server
    premium_acc_retweets_cap = mapped_column(Integer)  # Data got from server

    def __repr__(self):
        return("----------------------SETTINGS----------------------\n"+
              "{0: <30} {1: <30}\n".format("Settings id:", self.id)+
              "{0: <30} {1: <30}\n".format("user_id:", self.user_id)+
              "{0: <30} {1: <30}\n".format("max_tweets:", self.max_tweets)+
              "{0: <30} {1: <30}\n".format("max_retweets:", self.max_retweets)+
              "{0: <30} {1: <30}\n".format("period_cooldown_minutes:", self.period_cooldown_minutes)+
              "{0: <30} {1: <30}\n".format("linke_chance:", self.linke_chance)+
              "{0: <30} {1: <30}\n".format("react_chance:", self.react_chance)+
              "{0: <30} {1: <30}\n".format("action_delay_seconds:", self.action_delay_seconds)+
              "{0: <30} {1: <30}\n".format("normal_acc_retweets_cap:", self.normal_acc_retweets_cap)+
              "{0: <30} {1: <30}\n".format("premium_acc_retweets_cap:", self.premium_acc_retweets_cap)+
              "-----------------------------------------------------")


class Twitter_account(Base):
    __tablename__ = "twitter_account"
    id = mapped_column(Integer, primary_key=True, unique=True)
    user_id = mapped_column(Integer, ForeignKey('user.id'))
    is_premium = mapped_column(Integer)
    stats = relationship('Stats', backref='twitter_account', cascade="all, delete", passive_deletes=False)
    auth = relationship('Auth', backref='twitter_account', cascade="all, delete", passive_deletes=False)
    proxy = relationship('Proxy', backref='twitter_account', cascade="all, delete", passive_deletes=False)
    groups = relationship('Group', backref='twitter_account', cascade="all, delete", passive_deletes=False)

    def __repr__(self):
        return("-------------------TWITTER ACCOUNT------------------\n"+
              "{0: <30} {1: <30}\n".format("Twitter_account id:", self.id)+
              "{0: <30} {1: <30}\n".format("user_id:", self.user_id)+
              "{0: <30} {1: <30}\n".format("is_premium:", self.is_premium)+
              "{0: <30} {1: <30}\n".format("stats num:", len(self.stats))+
              "{0: <30} {1: <30}\n".format("auth num:", len(self.auth))+
              "{0: <30} {1: <30}\n".format("proxy num:", len(self.proxy))+
              "{0: <30} {1: <30}\n".format("groups num:", len(self.groups))+
              "-----------------------------------------------------")

class Stats(Base):
    __tablename__ = "stats"
    id = mapped_column(Integer, primary_key=True, unique=True)
    twitter_account_id = mapped_column(Integer, ForeignKey('twitter_account.id'))
    total_msg_sent_num = mapped_column(Integer)
    current_period_msg_sent = mapped_column(Integer)
    total_retweets_num = mapped_column(Integer)
    current_period_retweets_num = mapped_column(Integer)
    status = mapped_column(Text)

    def __repr__(self):
        return("---------------------STATISTICS---------------------\n"+
              "{0: <30} {1: <30}\n".format("Statistics id:", self.id)+
              "{0: <30} {1: <30}\n".format("twitter_account_id:", self.twitter_account_id)+
              "{0: <30} {1: <30}\n".format("total_msg_sent_num:", self.total_msg_sent_num)+
              "{0: <30} {1: <30}\n".format("current_period_msg_sent:", self.current_period_msg_sent)+
              "{0: <30} {1: <30}\n".format("total_retweets_num:", self.total_retweets_num)+
              "{0: <30} {1: <30}\n".format("current_period_retweets_num:", self.current_period_retweets_num)+
              "{0: <30} {1: <30}\n".format("status:", self.status)+
              "-----------------------------------------------------")


class Auth(Base):
    __tablename__ = "auth"
    id = mapped_column(Integer, primary_key=True, unique=True)
    twitter_account_id = mapped_column(Integer, ForeignKey('twitter_account.id'))
    login = mapped_column(Text)
    password = mapped_column(Text)
    auth_token = mapped_column(Text)

    def __repr__(self):
        return("------------------------AUTH------------------------\n"+
              "{0: <30} {1: <30}\n".format("Auth id:", self.id)+
              "{0: <30} {1: <30}\n".format("twitter_account_id:", self.twitter_account_id)+
              "{0: <30} {1: <30}\n".format("login:", self.login if self.login else " ")+
              "{0: <30} {1: <30}\n".format("password:", self.password if self.password else " ")+
              "{0: <30} {1: <30}\n".format("auth_token:", self.auth_token if self.auth_token else " ")+
              "-----------------------------------------------------")


class Proxy(Base):
    __tablename__ = "proxy"
    id = mapped_column(Integer, primary_key=True, unique=True)
    twitter_account_id = mapped_column(Integer, ForeignKey('twitter_account.id'))
    ip = mapped_column(Text)
    port = mapped_column(Integer)
    type = mapped_column(Text)  #TODO do we really need this? how to use?

    def __repr__(self):
        return("-----------------------PROXY------------------------\n"+
              "{0: <30} {1: <30}\n".format("Proxy id:", self.id)+
              "{0: <30} {1: <30}\n".format("twitter_account_id:", self.twitter_account_id)+
              "{0: <30} {1: <30}\n".format("ip:", self.ip)+
              "{0: <30} {1: <30}\n".format("port:", self.port)+
              "{0: <30} {1: <30}\n".format("type:", self.type)+
              "-----------------------------------------------------")


class Group(Base):
    __tablename__ = "group"
    id = mapped_column(Integer, primary_key=True, unique=True)
    twitter_account_id = mapped_column(Integer, ForeignKey('twitter_account.id'))
    link = mapped_column(Text)
    previous_msg_check_num = mapped_column(Integer)
    retweets_done = relationship('Retweet', backref='group', cascade="all, delete", passive_deletes=False)

    def __repr__(self):
        return("-----------------------GROUP------------------------\n"+
              "{0: <30} {1: <30}\n".format("Group id:", self.id)+
              "{0: <30} {1: <30}\n".format("twitter_account_id:", self.twitter_account_id)+
              "{0: <30} {1: <30}\n".format("link:", self.link)+
              "{0: <30} {1: <30}\n".format("previous_msg_check_num:", self.previous_msg_check_num)+
              "{0: <30} {1: <30}\n".format("retweets_done num:", len(self.retweets_done))+
              "-----------------------------------------------------")


class Retweet(Base):
    __tablename__ = "retweet"
    id = mapped_column(Integer, primary_key=True, unique=True)
    group_id = mapped_column(Integer, ForeignKey('group.id'))
    retweet_id = mapped_column(Integer)

    def __repr__(self):
        return("-----------------------RETWEET-----------------------\n"+
              "{0: <30} {1: <30}\n".format("Retweet id:", self.id)+
              "{0: <30} {1: <30}\n".format("group_id:", self.group_id)+
              "{0: <30} {1: <30}\n".format("retweet_id:", self.retweet_id)+
              "-----------------------------------------------------")
