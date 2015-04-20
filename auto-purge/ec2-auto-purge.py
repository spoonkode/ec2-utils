from apscheduler.schedulers.background import BackgroundScheduler
import argparse
import ConfigParser


class AutoPurge:
    args = None
    config = None
    scheduler = BackgroundScheduler()

    def __init__(self):
        self.args = self.process_args()
        self.config = self.process_config(self.args.config_file)

    @staticmethod
    def process_args():
        """
        Process the command line arguments
        :return:args
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("--config", dest='config_file', type=file, help="configuration file")
        return parser.parse_args()

    @staticmethod
    def process_config(config_file_handle):
        """
        Process configuration file
        :param config_file_handle: file object
        :return:config
        """
        global_defaults = {
            'tag-name': 'auto-purge',
            'default-aws-region': 'eu-west',
        }

        cfg = ConfigParser.SafeConfigParser(global_defaults)
        cfg.readfp(config_file_handle)
        return cfg

    def setup_schedules(self):
        pass


if __name__ == "__main__":

    ap = AutoPurge()

    print ap.config.get('global', 'tag-name')