from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import Session
from config import DB_LOCATION,DB_NAME
from database.database import Base


db_engine = create_engine(DB_LOCATION)

# Creating database file if not existed
def database_create():
    _engine = create_engine(f"sqlite:///{DB_NAME}.db", echo=True)
    if not database_exists(_engine.url):
        print(f"Database file within path {_engine.url} not found. Creating database file {DB_LOCATION}")
        try:
            Base.metadata.create_all(_engine)
            print(f"Database created")
        except Exception as e:
            print(f"Error occered: \n {e}")

def create_test_data():
    with Session(db_engine) as session:
        # Adding app user
        new_user = User(
            app_login = "test_login",
            app_password = "test_password",
            subscription_expire_date = 123
        )
        session.add(new_user)
        session.commit() # to get user.id later

        # Adding attachments
        new_attachment_1 = Attachment(
            user_id= new_user.id,
            is_text = 0,
            text = None,
            attachment_path = "test_path"
        )
        new_attachment_2 = Attachment(
            user_id= new_user.id,
            is_text = 1,
            text = "some test text",
            attachment_path = None
        )
        session.add_all([new_attachment_1, new_attachment_2])

        # Adding app settings
        new_settings = Settings(
            user_id = new_user.id,
            max_tweets = 1000,
            max_retweets = 500,
            period_cooldown_minutes = 30,
            linke_chance = 0.1,
            react_chance = 0.05,
            action_delay_seconds = 3,
            normal_acc_retweets_cap = 1200,
            premium_acc_retweets_cap = 1500
        )
        session.add(new_settings)

        # Adding Twitter accounts
        new_twitter_account_1 = Twitter_account(
            user_id = new_user.id,
            is_premium = 1
        )
        new_twitter_account_2 = Twitter_account(
            user_id = new_user.id,
            is_premium = 0
        )
        session.add_all([new_twitter_account_1, new_twitter_account_2])
        session.commit() # To use twitter_account.id later

        # Adding Twitter accounts statistics
        new_statistics_1 = Stats(
            twitter_account_id= new_twitter_account_1.id,
            total_msg_sent_num = 123,
            current_period_msg_sent = 11,
            total_retweets_num = 321,
            current_period_retweets_num =12,
            status = "Working"
        )
        new_statistics_2 = Stats(
            twitter_account_id= new_twitter_account_2.id,
            total_msg_sent_num = 456,
            current_period_msg_sent = 22,
            total_retweets_num = 789,
            current_period_retweets_num = 33,
            status = "On hold"
        )
        session.add_all([new_statistics_1, new_statistics_2])

        # Adding Twitter accounts auth
        new_auth_1 = Auth(
            twitter_account_id = new_twitter_account_1.id,
            login = "some_login",
            password = "some_password",
            auth_token = None
        )
        new_auth_2 = Auth(
            twitter_account_id = new_twitter_account_2.id,
            login = None,
            password = None,
            auth_token = "some_auth_token"
        )
        session.add_all([new_auth_1, new_auth_2])

        # Adding Twitter accounts proxy
        new_proxy_1 = Proxy(
            twitter_account_id = new_twitter_account_1.id,
            ip = "192.168.0.0",
            port = "5000",
            type = "type 1"
        )
        new_proxy_2 = Proxy(
            twitter_account_id = new_twitter_account_2.id,
            ip = "192.168.0.1",
            port = "6868",
            type = "type 2"
        )
        session.add_all([new_proxy_1, new_proxy_2])

        # Adding Twitter accounts groups
        new_group_1 = Group(
            twitter_account_id = new_twitter_account_1.id,
            enabled = 1,
            link = "link 1",
            previous_msg_check_num = 5,
            )
        new_group_2 = Group(
            twitter_account_id = new_twitter_account_1.id,
            enabled = 0,
            link = "link 2",
            previous_msg_check_num = 3,
            )
        new_group_3 = Group(
            twitter_account_id = new_twitter_account_2.id,
            enabled = 1,
            link = "link 3",
            previous_msg_check_num = 0,
            )
        session.add_all([new_group_1, new_group_2, new_group_3])
        session.commit() # To use group.id later

        # Adding retweets to Twitter accounts groups
        new_tweet_1 = Retweet(
            group_id = new_group_1.id,
            retweet_id = 123
        )
        new_tweet_2 = Retweet(
            group_id = new_group_1.id,
            retweet_id = 789
        )
        new_tweet_3 = Retweet(
            group_id = new_group_2.id,
            retweet_id = 963
        )
        session.add_all([new_tweet_1, new_tweet_2, new_tweet_3])

        session.commit()


if __name__ == "__main__":  # DB Tests
    from database import User
    from database import Attachment
    from database import Settings
    from database import Twitter_account
    from database import Stats
    from database import Auth
    from database import Proxy
    from database import Group
    from database import Retweet

    #database_create()

    #create_test_data()

    # Testing getting data from the table
    from sqlalchemy import select
    with Session(db_engine) as session:
        selected_user = session.execute(select(User).where(User.id == 1)).scalar_one_or_none()

        # Printing attachments
        for attachment in selected_user.attachments:
            print(attachment)

        # Printing settings
        print(selected_user.settings)

        # Printing Twitter accounts
        for account in selected_user.twitter_accounts:
            print(account)
            # Printing Twitter account statistics
            print(account.stats)
            # Printing Twitter account auth
            print(account.auth)
            # Printing Twitter account proxy
            print(account.proxy)
            # Printing Twitter account groups
            for group in account.groups:
                print(group)
                # Print Twitter group retweets
                for retweet in group.retweets_done:
                    print(retweet)
