import subprocess

from tornado.ioloop import IOLoop
import tornado.web


class DumpImportRequestHandler(tornado.web.RequestHandler):

    def post(self, *args, **kwargs):
        try:
            host = "localhost"
            username = "postgres"
            file_name = self.get_argument("file_name")
            command = "cat {0} | psql --host={1} --username={2}".format(file_name,
                                                                        host,
                                                                        username)
            response = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE)
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
