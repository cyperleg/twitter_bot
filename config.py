import os


DB_NAME = "DB"
DB_LOCATION = f"sqlite:///{os.path.join(os.getcwd(), DB_NAME + '.db')}"  # on Windows
#DB_LOCATION = f"sqlite:////{os.path.join(os.getcwd(), DB_NAME + '.db')}"  # on Linux