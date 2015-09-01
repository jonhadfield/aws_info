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

#def release_addresses(addresses):
#    for address in addresses:
#    print "Releasing: {0}".format(address.public_ip)
#        address.release()

#if __name__ == "__main__":
#    conn = boto.ec2.connect_to_region("eu-west-1",
#                    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY', None),
#                    aws_secret_access_key=os.environ.get('AWS_SECRET_KEY', None))
#    unassigned_addresses = get_unassigned_eips(conn)
#    if unassigned_addresses:
#        pass
#        #release_addresses(unassigned_addresses)
#    else:
#        print "No unassigned EIPs found."
