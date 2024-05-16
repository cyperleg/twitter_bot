import os


DB_NAME = "DB"
DB_LOCATION = f"sqlite:///{os.path.join(os.getcwd(),'database', DB_NAME + '.db')}"  # on Windows
SERVER_LINK = "http://127.0.0.1:5000"
STATUS = {"on_hold": "On hold", "active": "Active"}
#DB_LOCATION = f"sqlite:////{os.path.join(os.getcwd(), DB_NAME + '.db')}"  # on Linux