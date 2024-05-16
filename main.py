import sys
import os
import traceback

from PyQt5.QtWidgets import QApplication
from gui.main_app import MainApp
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from config import DB_LOCATION


Session = Session(create_engine(DB_LOCATION))


def start_app():
    try:
        app = QApplication(sys.argv)
        maine_appe = MainApp(Session)
        maine_appe.show()
        app.exec_()
    except Exception:
        traceback.print_exc()


if __name__ == "__main__":
    os.environ['NO_PROXY'] = 'http://127.0.0.1:5000'
    start_app()




# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.service import Service
#
# # Путь к исполняемому файлу Chrome WebDriver
# webdriver_path = "./chromedriver.exe"
#
# # URL сайта, который нужно открыть
# url = "https://twitter.com"
#
# proxy_host = "200.19.177.120"
# proxy_port = "80"
# proxy_protocol = "HTTP"
#
# # Создание сервиса Chrome WebDriver
# service = Service(webdriver_path)
#
# # Запуск сервиса Chrome WebDriver
# service.start()
#
# # Настройка опций для браузера Chrome
# options = webdriver.ChromeOptions()
#
# #options.add_argument(f"--proxy-server={proxy_protocol}://{proxy_host}:{proxy_port}")
#
# # Если нужно скрыть окно браузера (работа в фоновом режиме)
# # options.add_argument('--headless')
#
# # Создание экземпляра браузера Chrome
# driver = webdriver.Chrome(service=service, options=options)
#
#
# try:
#     # Открытие сайта
#     driver.get(url)
#
#     # Явные ожидания: ждем, пока элемент с тегом 'body' не станет видимым
#     WebDriverWait(driver, 10).until(
#         EC.visibility_of_element_located((By.TAG_NAME, 'body'))
#     )
#
#     element = driver.find_element(By.CSS_SELECTOR, '[href="/login"]')
#     element.click()
#
#     time.sleep(1)
#
#     element = driver.find_element(By.XPATH, '//input[@name="text"]')
#     element.send_keys("Legendjojo19320")
#
#     element = driver.find_element(By.XPATH, '//*[text()="Далее"]')
#     element.click()
#
#     time.sleep(1)
#
#     element = driver.find_element(By.XPATH, '//input[@name="password"]')
#     element.send_keys("Lolka19320")
#     time.sleep(1)
#     element = driver.find_element(By.XPATH, '//*[text()="Войти"]')
#     element.click()
#
#     WebDriverWait(driver, 10).until(EC.url_changes("https://twitter.com"))
#
#
#     # Пример: получение заголовка страницы и его вывод
#     print("Title of the webpage is:", driver.title)
#
# except Exception as e:
#     print(e)
# finally:
#     # Закрытие браузера
#     input()
#     driver.quit()