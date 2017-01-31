import os
import datetime
import subprocess

import requests as rq

from components.logger import Logger
from components.conf import settings
from components.scp_handler import SCPHandler


class DumpExporter:
    def __init__(self):
        self.pg_dump_path = "/opt/PostgreSQL/9.6/bin/pg_dump"
        self.user = "postgres"
        self.host = "localhost"
        self.db_name = "corseco_dashboard"
        self.port = 5432

        # initialize logging parameters
        self.log_params = {
            "error": {
                "file_name": "error.log",
                "log_dir": settings.LOG_DIR,
                "stream_handler": None,
                "file_handler": True
            }
        }

        # initializing scp handler
        self.scp_handler = SCPHandler(**settings.REMOTE_SERVER_CREDENTIAL["my_lubuntu_vm"])

        self.error_logger = Logger(**self.log_params["error"])

    def get_dump(self):
        try:
            command = "{0} --host={1} --username={2} --dbname={3} --port={4}".format(self.pg_dump_path,
                                                                                     self.host,
                                                                                     self.user,
                                                                                     self.db_name,
                                                                                     self.port)
            response = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE)
            out, err = response.communicate()
            dump_file_name = "dump_{}.sql".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
            local_dump_path = os.path.join(os.path.dirname(__file__),
                                           "sql_dumps",
                                           dump_file_name)
            remote_dump_path = "/home/luvm/{}".format(dump_file_name)

            with open(local_dump_path, "wb") as file_handle:
                file_handle.write(out)
            self.scp_handler.put_file(local_path=local_dump_path,
                                      remote_path=remote_dump_path)

            remote_url = "http://{}:8002/import_dump".format(
                settings.REMOTE_SERVER_CREDENTIAL["my_lubuntu_vm"]["host"]
            )

            post_data = {"file_name": remote_dump_path }
            response = rq.post(remote_url, data=post_data)
            print response.status_code

        except Exception as err:
            print err.message
            self.error_logger.logger.error("{}::{}".format("DumpExporter.get_dump",
                                                           err.message))


def main():
    exporter_obj = DumpExporter()
    exporter_obj.get_dump()


if __name__ == "__main__":
    main()
