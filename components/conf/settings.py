import os


LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "log")
CONFIG_FILE_DIR = ""


# REMOTE SERVER CREDENTIALS

REMOTE_SERVER_CREDENTIAL = {
    "my_lubuntu_vm": {
        "host": "192.168.1.33",
        "port": 22,
        "username": "luvm",
        "password": "vm123#"
    }
}