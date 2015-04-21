# ec2-utils

This is a collection of scripts I use to manage EC2 objects. Quick and dirty scripts that have evolved over time.

## ec2-auto-purge.py

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
