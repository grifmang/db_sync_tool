import os


# directory path for placing log files
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "log")

# file containing db connection parameters & other settings
CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__),
                                "dbconfig")

# REMOTE SERVER CREDENTIALS
REMOTE_SERVER_CREDENTIAL = {
    "my_lubuntu_vm": {
        "host": "",
        "port": 22,
        "username": "",
    },
    "remote_vps": {
        "host": "",
        "port": 22,
        "username": "",
    }
}
