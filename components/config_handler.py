from configparser import ConfigParser

from conf import settings


class DBConfiguration:
    def __init__(self):
        self.config_file_path = settings.CONFIG_FILE_DIR
        self.config_parser = ConfigParser()
        self.config_parser.read(self.config_file_path)

    def get_db_configuration(self, section, data=None):
        if data is not None:
            config_dict = dict()
            for key in data:
                config_dict[key] = self.config_parser.get(section,
                                                          key)
            return config_dict