# ec2-utils

This is a collection of scripts I use to manage EC2 objects. Quick and dirty scripts that have evolved over time.

## auto-purge/ec2-auto-purge.py

A service that will shutdown all instances at a given time that have a given tag.

### Installation

I would suggest installing into a virtual env...

    $ git clone git@github.com:spoonkode/ec2-utils.git
    $ cd auto-purge
    $ pip install -r requirements.txt

### Usage

    $ nohup python auto-purge/ec2-auto-purge.py --config /path/to/config.ini &

### Configuration

Example...

    [global]
    aws-region = eu-west-1
    tag-name = auto-purge
    aws-access-key = XXXXXXXXXXXXX
    aws-secret-key = XXXXXXXXXXXXX

    [office-hours-only]
    tag-value = office-hours-only
    hour = 18
    action = stop

[global] - this section holds the global configuration variables

All other sections are "jobs" and each job defines which action is applied to instances that have a given tag value and at what time (cron) it happens.

Example:

    [office-hours-only]
    tag-value = office-hours-only
    hour = 18
    action = stop

The job named *office-hours-only* will stop all instances that have a tag named *auto-purge* with a value of *office-hours-only* at 18h00 each day.

## gmail-mx/ec2-gmail-mx.py

A script which adds Gmail-specific MX records to a Route53-hosted DNS zone. Usefull if you need to get ad-hoc domains setup for Google Apps.

### Installation

I would suggest installing into a virtual env...

    $ git clone git@github.com:spoonkode/ec2-utils.git
    $ cd gmail-mx
    $ pip install -r requirements.txt

### Credentials

You need to store your credentials in a boto-support manner. Example: in the ~/.boto file

Read http://boto.readthedocs.org/en/latest/boto_config_tut.html#credentials

### Usage

    usage: ec2-gmail-mx.py [-h] [--action ACTION] [--domain DOMAIN]
                           [--force-create FORCE] [--aws-region AWS_REGION]

    optional arguments:
      -h, --help                show this help message and exit
      --action ACTION           Action - add or delete MX records (default: add)
      --domain DOMAIN           DNS Zone
      --force-create FORCE      Force creation of missing zones (default: no)
      --aws-region AWS_REGION   AWS Region (default: eu-west-1)

    *WARNING* If you use action delete, it will delete *ALL* existing MX records.