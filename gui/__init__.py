from PyQt5.QtWidgets import QApplication
from main_app import MainApp
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from config import DB_LOCATION


Session = Session(create_engine(DB_LOCATION))


def start_app():
    maine_appe = MainApp(Session)
    app = QApplication(maine_appe)
    maine_appe.show()
    app.exec_()


if __name__ == "__main__":
    start_app()
