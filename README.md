# ec2-utils


## ec2-auto-purge.py

A service that will shutdown all instances at a given time that have a given tag.

### Installation

'''
$ git clone git@github.com:spoonkode/ec2-utils.git
$ cd auto-purge
$ pip install -r requirements.txt
'''

### Usage


'''
$ nohup python auto-purge/ec2-auto-purge.py --config /path/to/config.ini &
'''

### Configuration

Example...

'''
[global]
aws-region = eu-west-1
tag-name = auto-purge
aws-access-key = XXXXXXXXXXXXX
aws-secret-key = XXXXXXXXXXXXX

[office-hours-only]
tag-value = office-hours-only
hour = 18
action = stop
'''

[global] - this section holds the global configuration variables

All other sections are "jobs" each job definines which action is applied to instances that have a given tag value and at what time (cron) it happens
