import paramiko

from conf import settings
from logger import Logger


class SCPHandler:
    def __init__(self, host, username, password, port=22):
        self.sftp = None
        self.sftp_open = False

        # initialize logging parameters
        self.log_params = {
            "error":{
                "file_name": "error.log",
                "log_dir": settings.LOG_DIR,
                "stream_handler": True,
                "file_handler": True
            }
        }
        self.logger = Logger(**self.log_params["error"])

        # open ssh Transport stream
        try:
            self.transport = paramiko.Transport((host, port))
            self.transport.connect(username=username,
                                   password=password)

        except Exception as err:
            self.logger.error("{}::{}".format("SCPHandler.__init__",
                                              err.message))

    def open_sftp_connection(self):
        try:
            if not self.sftp_open:
                self.sftp = paramiko.SFTPClient.from_transport(self.transport)
                self.sftp_open = True

        except Exception as err:
            self.logger.error("{}::{}".format("SCPHandler.open_sftp_connection",
                                              err.message))

    def get_file(self, remote_path, local_path=None):
        try:
            self.open_sftp_connection()
            self.sftp.get(remote_path, local_path)

        except Exception as err:
            self.logger.error("{}::{}".format("SCPHandler.get_file",
                                              err.message))

    def put_file(self, local_path, remote_path=None):
        try:
            self.open_sftp_connection()
            self.sftp.put(local_path, remote_path)

        except Exception as err:
            self.logger.error("{}::{}".format("SCPHandler.put_file",
                                              err.message))


def main():
    user = "luvm"
    host = "192.168.1.33"
    port = 22
    password = "vm123#"
    scp_handler = SCPHandler(host, user, password, port)
    scp_handler.put_file("/home/sud/alag.py", "/home/luvm/alag.py")


if __name__ == "__main__":
    main()
