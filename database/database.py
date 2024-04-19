from app.database import db
from sqlalchemy.orm import backref


class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}
    __bind_key__ = "core_db"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    app_login = db.Column(db.String(30), unique=True)
    app_password = db.Column(db.String(30))
    subscription_expire_date = db.Column(db.DateTime)
    attachments = db.relationship('attachment', backref=backref('user',
                                                                uselist=False,
                                                                single_parent=True,
                                                                cascade="all, delete-orphan",
                                                                passive_deletes=True))
    twitter_accounts = db.relationship('twitter_account', backref=backref('user',
                                                                          uselist=False,
                                                                          single_parent=True,
                                                                          cascade="all, delete-orphan",
                                                                          passive_deletes=True))

    settings = db.relationship('settings', backref=backref('user',
                                                           uselist=False,
                                                           single_parent=True,
                                                           cascade="all, delete-orphan",
                                                           passive_deletes=True))


class Attachment(db.Model):
    __tablename__ = "attachment"
    __table_args__ = {'extend_existing': True}
    __bind_key__ = "core_db"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_text = db.Column(db.Boolean)
    text = db.Column(db.Text)
    attachment_path = db.Column(db.String(300))


class Settings(db.Model):
    __tablename__ = "settings"
    __table_args__ = {'extend_existing': True}
    __bind_key__ = "core_db"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    twitter_account_id = db.Column(db.Integer, db.ForeignKey('twitter_account.id'))
    max_tweets = db.Column(db.Integer)
    max_retweets = db.Column(db.Integer)
    period_cooldown_minutes = db.Column(db.Integer)
    linke_chance = db.Column(db.Float)
    react_chance = db.Column(db.Float)
    action_delay_seconds = db.Column(db.Integer)      # Data got from server
    normal_acc_retweets_cap = db.Column(db.Integer)   # Data got from server
    premium_acc_retweets_cap = db.Column(db.Integer)  # Data got from server


class Twitter_account(db.Model):
    __tablename__ = "twitter_account"
    __table_args__ = {'extend_existing': True}
    __bind_key__ = "core_db"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_premium = db.Column(db.Boolean)
    stats = db.relationship('stats', backref=backref('twitter_account',
                                                     uselist=False,
                                                     single_parent=True,
                                                     cascade="all, delete-orphan",
                                                     passive_deletes=True))
    auth = db.relationship('auth', backref=backref('twitter_account',
                                                   uselist=False,
                                                   single_parent=True,
                                                   cascade="all, delete-orphan",
                                                   passive_deletes=True))
    proxy = db.relationship('proxy', backref=backref('twitter_account',
                                                     uselist=False,
                                                     single_parent=True,
                                                     cascade="all, delete-orphan",
                                                     passive_deletes=True))
    groups = db.relationship('group', backref=backref('twitter_account',
                                                      uselist=False,
                                                      single_parent=True,
                                                      cascade="all, delete-orphan",
                                                      passive_deletes=True))


class Stats(db.Model):
    __tablename__ = "stats"
    __table_args__ = {'extend_existing': True}
    __bind_key__ = "core_db"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    twitter_account_id = db.Column(db.Integer, db.ForeignKey('twitter_account.id'))
    total_msg_sent_num = db.Column(db.Integer)
    current_period_msg_sent = db.Column(db.Integer)
    total_retweets_num = db.Column(db.Integer)
    current_period_retweets_num = db.Column(db.Integer)
    status = db.Column(db.String(30))


class Auth(db.Model):
    __tablename__ = "auth"
    __table_args__ = {'extend_existing': True}
    __bind_key__ = "core_db"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    twitter_account_id = db.Column(db.Integer, db.ForeignKey('twitter_account.id'))
    login = db.Column(db.String(30))
    password = db.Column(db.String(30))
    auth_token = db.Column(db.String(100))


class Proxy(db.Model):
    __tablename__ = "proxy"
    __table_args__ = {'extend_existing': True}
    __bind_key__ = "core_db"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    twitter_account_id = db.Column(db.Integer, db.ForeignKey('twitter_account.id'))
    ip = db.Column(db.String(16))
    port = db.Column(db.Integer)
    type = db.Column(db.String(20))  #TODO do we really need this? how to use?


class Group(db.Model):
    __tablename__ = "group"
    __table_args__ = {'extend_existing': True}
    __bind_key__ = "core_db"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    twitter_account_id = db.Column(db.Integer, db.ForeignKey('twitter_account.id'))
    link = db.Column(db.String(100))
    previous_msg_check_num = db.Column(db.Integer)
    retweets_done = db.relationship('retweet', backref=backref('group',
                                                                uselist=False,
                                                                single_parent=True,
                                                                cascade="all, delete-orphan",
                                                                passive_deletes=True))


class Retweet(db.Model):
    __tablename__ = "retweet"
    __table_args__ = {'extend_existing': True}
    __bind_key__ = "core_db"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    retweet_id = db.Column(db.Integer)
