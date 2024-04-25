from PyQt5.QtWidgets import QApplication
from main_app import MainApp
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


DB_path = ""
Session = Session(create_engine(DB_path))


def start_app():
    main_app = MainApp(Session)
    app = QApplication()
    main_app.show()
    app.exec_()


if __name__ == "__main__":
    start_app()
