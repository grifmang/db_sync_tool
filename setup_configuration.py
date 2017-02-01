import os
import sys
import getpass
import subprocess

from crontab import CronTab

from components import config_handler


class SetupConfiguration:
    def __init__(self):
        self.python_venv_name = None
        self.user_home_dir = os.environ['HOME']
        self.current_user = getpass.getuser()
        self.db_config_handler = config_handler.DBConfiguration()
        self.config_sections = self.db_config_handler.config_parser.sections()

    def initialize_configuration(self):
        try:
            self.python_venv_name = raw_input("Enter python virtual environment name")
            print("\n")
            print("select the configuration section as per your environment")
            print("\n")
            for index, section in enumerate(self.config_sections):
                print("{}: {}".format(index, section))

            print("\n")
            section_index = int(raw_input())
            if not type(section_index) == int and section_index < len(self.config_sections):
                print("invalid section index value")
                sys.exit(1)
            current_section = self.config_sections[section_index]
            current_section_config_dict = self.db_config_handler.get_db_configuration(current_section)

            for key, value in current_section_config_dict.items():
                print("current value: {}=>{}".format(key, value))
                print("\n")
                current_section_config_dict[key] = raw_input("new_value: ")
                print("\n")

            self.db_config_handler.set_db_configuration(current_section,
                                                        current_section_config_dict)

            print("Creating pgpass file in home directory...")
            pgpass_file_path = os.path.join(os.environ["HOME"],
                                            ".pgpass")
            if os.path.exists(pgpass_file_path):
                os.remove(pgpass_file_path)

            pg_pass_file_content = "*:*:*:*:{}".format(current_section_config_dict['password'])

            with open(pgpass_file_path, "wb") as file_handle:
                file_handle.write(pg_pass_file_content)

            os.chmod(pgpass_file_path, 0600)

            if current_section == "remote-db-setting":
                print("Initiating db_dump_importer server...")
                subprocess.Popen("nohup /home/sud/.virtualenvs/new_env/bin/python ./db_dump_importer.py &".split())

            elif current_section == "local-db-setting":
                print("Setting db_dump_exporter cron job...")
                current_user_cron = CronTab(user=self.current_user)
                cron_job_command = "{}/.virtualenvs/{}/bin/python ./db_dump_exporter.py".format(self.user_home_dir,
                                                                                                self.python_venv_name)
                job = current_user_cron.new(command=cron_job_command)
                job.setall("*/5 * * * *")

                if job.is_valid():
                    current_user_cron.write_to_user()
                else:
                    print("Invalid cron job!")

            print ("All Set. Adios Muchachos!!")

        except Exception as err:
            print err.message


def main():
    setup_config_instance = SetupConfiguration()
    setup_config_instance.initialize_configuration()


if __name__ == "__main__":
    main()
