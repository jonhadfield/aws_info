#!/usr/bin/env python
#import boto.ec2
#import boto.ec2.image
#import boto.exception
#import os
#import re
#import sys

def get_unassociated_eips(connection):
    all_ips = connection.get_all_addresses()
    return [x for x in all_ips if not x.instance_id]

