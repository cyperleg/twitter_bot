from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from database.database import Twitter_account, Retweet
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class Class:
    def __init__(self, db, account_id):
        self.db = db
        self.twitter_account = self.db.session.execute(self.db.select(Twitter_account).filter_by(id=account_id)).scalar_one_or_none()
        self.driver = self.create_driver()
        self.url = "https://x.com"


    def create_driver(self):
        # create custom driver with unique chrome profile
        # MB need to use user agent to more security

        profile_path = self.twitter_account.chrome_profile_path
        chrome_options = Options()
        chrome_options.add_argument(f"user-data-dir={profile_path}")
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        return webdriver.Chrome(options=chrome_options)


    def auth(self, login="Legendjojo19320", password="Lolka19320") -> None:
        if self.twitter_account.auth.password:
            try:
                # Открытие сайта
                self.driver.get(self.url)

                # Явные ожидания: ждем, пока элемент с тегом 'body' не станет видимым
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))

                element = self.driver.find_element(By.CSS_SELECTOR, '[href="/login"]')
                element.click()

                time.sleep(1)

                element = self.driver.find_element(By.XPATH, '//input[@name="text"]')
                #TODO change to login
                element.send_keys(login)

                element = self.driver.find_element(By.XPATH, '//*[text()="Далее"]')
                element.click()

                time.sleep(1)

                element = self.driver.find_element(By.XPATH, '//input[@name="password"]')
                #TODO change to password
                element.send_keys(password)
                time.sleep(1)
                element = self.driver.find_element(By.XPATH, '//*[text()="Войти"]')
                element.click()

                WebDriverWait(self.driver, 10).until(EC.url_changes(self.url))

            except Exception as e:
                print("Unable to login with password", e)

        elif self.twitter_account.auth.auth_token:
            try:
                self.driver.add_cookie(self.twitter_account.auth.auth_token)
                self.driver.refresh()
            except Exception as e:
                print("Unable to login with cookie", e)

        raise Exception("Unknown login method")


    def get_groups(self) -> list:
        # return -> [group_link1, group_link2, group_link3...]
        try:
            self.driver.get(self.url + "/messages")

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[role='main']")))

            main_element = self.driver.find_element(By.CSS_SELECTOR, "[role='main']")

            links_elements = main_element.find_elements(By.CSS_SELECTOR, "a[role='link']")

            links = [i.get_attribute('href') for i in links_elements]

            # updating db if no groups in db found

            return links
        except Exception as e:
            print("Unable to parse groups", e)

        return None



    def get_group_users_IDs(self, group_id:int, users_num:int, checked_msg_cap:int=40) -> list:  #except curent user
        # users_num -> Number of user profiles we want to repost from
        # checked_msg_cap -> Number of messages, checked before break. Default = 40
        #
        # return -> [link1, link2, link3...]
        return


    def retweet(self, user_id:int) -> None:
        # user_id -> Page, post from which will be reposted

        def is_retweeted(tweet_id: int) -> bool:
            if self.db.session.execute(
                    self.db.select(Retweet).filter_by(retweet_id=tweet_id)
            ).scalar_one_or_none():
                return True
            return False


        # getting tweets IDs through user's page
        #TODO get tweets IDs
        post_IDs = []

        # checking if user have any posts
        if post_IDs:
            # trying to select tweet that was not retweeted
            for id in post_IDs:
                if not is_retweeted(id):
                    #TODO do retweet
                    return  # When at least 1 retweet done - finish task

            # Retweeting post_IDs[0] in case all tweets was retweeted
            #TODO retweet tweet with id post_IDs[0]


if __name__ == "main":
    pass