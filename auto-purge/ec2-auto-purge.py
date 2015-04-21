from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
import argparse
from boto import ec2
import ConfigParser
import logging
import time


class AutoPurge:
    args = None
    config = None
    scheduler = BackgroundScheduler()
    #scheduler = BlockingScheduler()

    def __init__(self):
        self.args = self.process_args()
        self.config = self.process_config(self.args.config_file)
        self.setup_logging()

    @staticmethod
    def ec2connect(aws_region, aws_access_key, aws_secret_key):
        logging.debug("Connecting to AWS: aws_region=%s, aws_access_key=%s", aws_region, aws_access_key)
        conn = ec2.connect_to_region(aws_region,
                                     aws_access_key_id=aws_access_key,
                                     aws_secret_access_key=aws_secret_key)
        return conn

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
            'log-level': 'DEBUG',
            'log-file': '/var/log/auto-purge.log',
            'tag-name': 'auto-purge',
            'aws-region': 'eu-west-1',
            'action': 'stop',
        }

        cfg = ConfigParser.SafeConfigParser(global_defaults)
        cfg.readfp(config_file_handle)
        return cfg

    def setup_logging(self):
        """
        Set up logging.
        :return: void
        """
        levels = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARN': logging.WARN,
            'CRITICAL': logging.CRITICAL,
            'ERROR': logging.ERROR
        }

        loglevel = self.config.get('global', 'log-level')
        logfile = self.config.get('global', 'log-file')
        logformat = '%(asctime)s - %(levelname)s - %(message)s'

        logging.basicConfig(filename=logfile, level=levels[loglevel], format=logformat)

        logging.info("Starting up!!!")
        logging.info("Config File: %s", str(self.args.config_file))

    def job_callback(self, aws_region, tag_name, tag_value, action, job_id):
        """
        This method is called each time apscheduler is triggered.
        :param aws_region: the region we are connecting to
        :param tag_name: instances that have this tag name and;
        :param tag_value: instances that have this tag value
        :param action: the action to perform on the instance. Either stop (default) or terminate
        :param job_id: the job_id (can be anything really)
        :return: void
        """
        logging.info("Job %s - Firing callback: aws_region=%s, tag_name=%s, tag_value=%s, action=%s",
                     job_id, aws_region, tag_name, tag_value, action)

        ecc = self.ec2connect(aws_region,
                              self.config.get('global', 'aws-access-key'),
                              self.config.get('global', 'aws-secret-key'))

        reservations = ecc.get_all_reservations(filters={"tag:%s" % tag_name: tag_value})

        if len(reservations) < 1:
            logging.info("Job %s - No reservations found with tag '%s' having value '%s' ...nothing to do.",
                         job_id,
                         tag_name,
                         tag_value)
            return

        instances = [i.id for r in reservations for i in r.instances if i.state in ('running', 'pending')]

        if len(instances) < 1:
            logging.info("Job %s - No running/pending instances found ...nothing to do.", job_id)
            return

        logging.debug("Job %s - Found instances: %s", job_id, instances)

        if action == 'stop':
            ecc.stop_instances(instance_ids=instances)
        else:
            ecc.terminate_instances(instance_ids=instances)

        logging.info("Job %s - Callback completed", job_id)

    def setup_schedules(self):
        """
        Reads sections and sets up the apscheduler jobs
        :return: void
        """
        for section in self.config.sections():
            section_opts = []
            cron_opts = {}

            if section == 'global':
                continue

            for opt in ['aws-region', 'tag-name', 'tag-value', 'action']:
                if self.config.has_option(section, opt):
                    section_opts.append(self.config.get(section, opt))
                else:
                    raise Exception("Could not determine %s for %s" % (opt, section))

            for opt in ('year', 'month', 'day', 'week', 'day_of_week', 'hour', 'minute', 'second',
                        'start_date', 'end_date', 'timezone'):
                if self.config.has_option(section, opt):
                    cron_opts[opt] = self.config.get(section, opt)

            section_opts.append(section)
            self.scheduler.add_job(self.job_callback, trigger='cron', args=section_opts, id=section, **cron_opts)

if __name__ == "__main__":

    ap = AutoPurge()

    # Move this to the constructor?
    ap.setup_schedules()
    ap.scheduler.start()

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logging.info("Shutting down...")
        ap.scheduler.shutdown()
