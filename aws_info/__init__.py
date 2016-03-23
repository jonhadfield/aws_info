#!/usr/bin/env python
from __future__ import print_function
import boto.ec2 
import boto
import boto.ec2.image
import boto.ec2.elb
import boto.exception
import os
import re
import sys
from account import get_account_aliases, get_account_id
from eip import get_unassociated_eips
from storage import get_orphaned_snapshots, get_unattached_volumes
from instances import get_unnamed_instances
from secgroups import get_open_secgroups


def real_main():
    dashes = "-----------------------------------------------"
    ec2_conn = boto.ec2.connect_to_region("eu-west-1",
                    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY', None),
                    aws_secret_access_key=os.environ.get('AWS_SECRET_KEY', None))
    iam_conn = boto.connect_iam(aws_access_key_id=os.environ.get('AWS_ACCESS_KEY', None),
                    aws_secret_access_key=os.environ.get('AWS_SECRET_KEY', None))
    elb_region = boto.regioninfo.RegionInfo( name='eu-west-1', endpoint='elasticloadbalancing.eu-west-1.amazonaws.com')
    elb_conn = boto.connect_elb(region=elb_region, aws_access_key_id=os.environ.get('AWS_ACCESS_KEY', None), aws_secret_access_key=os.environ.get('AWS_SECRET_KEY', None))

    # ACCOUNT INFO
    account_aliases = get_account_aliases(iam_conn)
    print("{0}\nAccount ID:      {1}".format(dashes, get_account_id(iam_conn)))
    print("Account Aliases: {0}\n{1}".format(",".join(account_aliases),dashes))

    # UNNAMED INSTANCES
    unnamed_instances = get_unnamed_instances(ec2_conn)
    if unnamed_instances:
        print("Unnamed instances\n{0}".format(dashes))
        for inst in unnamed_instances:
            print("{0} | {1}".format(inst.id, inst.instance_type))
        print("{0}".format(dashes))

    # EIPS
    unassigned_addresses = get_unassociated_eips(ec2_conn)
    if unassigned_addresses:
        print("Unassigned EIPs\n{0}".format(dashes))
        for addr in unassigned_addresses:
            print(addr)
        print("{0}".format(dashes))

    # OPEN SECURITY GROUPS
    open_groups = get_open_secgroups(ec2_conn)
    elbs = elb_conn.get_all_load_balancers()
    if open_groups:
        print("Open Security Groups\n{0}".format(dashes))
        for og in open_groups:
            og_instances = og.instances()
            has_running_instance = False
            has_elb = False
            for ins in og_instances:
                if ins.state == 'running':
                    has_running_instance = True
                    break
            for elb in elbs:
                if (og.name == elb.source_security_group.name) or ([x for x in elb.security_groups if og.name == x[0]]):
                    has_elb = True

            if has_elb:
                print("{0} associated with ELBs:".format(og.name))
                for elb in elbs:
                    if (og.name == elb.source_security_group.name) or ([x for x in elb.security_groups if og.name == x[0]]):
                        print("  Name: {0}".format(elb.name))
            if has_running_instance:
                print("{0} associated with running instances:".format(og.name))
                for int in og_instances:
                    if ins.state == 'running':
                        print("  id: {0} | Name: {1}".format(ins.id, ins.tags.get('Name', '<Unnamed>')))
            if not any((has_elb, has_running_instance)):
                print("{0}".format(og.name))
        print("{0}".format(dashes))

    # UNATTACHED VOLUMES
    unattached_volumes = get_unattached_volumes(ec2_conn)
    if unattached_volumes:
       print("Unattached Volumes\n{0}".format(dashes))
       for vol in unattached_volumes:
           print("  {} | {}".format(vol.id, vol.tags.get('Name','<Unnamed>')))
       print("{0}".format(dashes))

        
    # ORPHANED SNAPSHOTS
    orphaned_snapshots = get_orphaned_snapshots(ec2_conn)
    if orphaned_snapshots:
       print("Orphaned Snapshots\n{0}".format(dashes))
       for snap in orphaned_snapshots:
           print("{0} | {1} | {2}".format(snap[0], snap[1], snap[2]))
       print("{0}".format(dashes))

if __name__ == '__main__':
    real_main()
