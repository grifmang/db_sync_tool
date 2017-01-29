import os
import subprocess


class DumpExporter:
    def __init__(self):
        self.pg_dump_path = "/Opt/PostgreSQL/9.6/bin/pg_dump"
        self.user = "postgres"
        self.host = "localhost"
        self.db_name = "corseco_dashboard"
        self.port = 5432
        self.pgpass_file_path = os.path.join(os.getcwd(),
                                             "components",
                                             "conf",
                                             ".pgpass")
        os.putenv("PGPASSFILE", self.pgpass_file_path)

    def get_dump(self):
        command = "{0} --host={1} --username={2} --dbname={3} --port={4}".format(self.pg_dump_path,
                                                                                 self.host,
                                                                                 self.user,
                                                                                 self.db_name,
                                                                                 self.port)
        response = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE)
        out, err = response.communicate()
        with open("sqldump", "wb") as file_handle:
            file_handle.write(out)
            
