import os
import subprocess

from components.logger import Logger
from components.conf import settings


class DumpExporter:
    def __init__(self):
        self.pg_dump_path = "/opt/PostgreSQL/9.6/bin/pg_dump"
        self.user = "postgres"
        self.host = "localhost"
        self.db_name = "corseco_dashboard"
        self.port = 5432

        self.log_params = {
            "error": {
                "file_name": "error.log",
                "log_dir": settings.LOG_DIR,
                "stream_handler": None,
                "file_handler": True
            }
        }

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
            with open("db_dump", "wb") as file_handle:
                file_handle.write(out)
                
        except Exception as err:
            self.error_logger.error("{}::{}".format("DumpExporter.get_dump",
                                                    err.message))


def main():
    exporter_obj = DumpExporter()
    exporter_obj.get_dump()


if __name__ == "__main__":
    main()
