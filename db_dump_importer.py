import subprocess

from tornado.ioloop import IOLoop
import tornado.web

from components import config_handler


class DumpImportRequestHandler(tornado.web.RequestHandler):

    def post(self, *args, **kwargs):
        try:
            # initializing DB Configuration Handler
            db_config_handler = config_handler.DBConfiguration()

            # fetching db configuration through handler
            db_config_dict = db_config_handler.get_db_configuration(
                "remote-db-setting")

            host = db_config_dict["host"]
            username = db_config_dict["user"]
            dbname = db_config_dict["dbname"]

            file_name = self.get_argument("file_name")
            command = "sh backup.sh {0} {1} {2} {3}".format(
                host, username, dbname,  file_name)
            response = subprocess.Popen(
                command.split(" "), stdout=subprocess.PIPE)
            out, err = response.communicate()

        except Exception as err:
            print err.message


class DumpImporterApplication(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/import_dump", DumpImportRequestHandler),
        ]
        tornado.web.Application.__init__(self, handlers)


def main():
    app_instance = DumpImporterApplication()
    print("[*]starting socket app on 8002")
    app_instance.listen(8002)
    IOLoop.instance().start()


if __name__ == "__main__":
    main()
