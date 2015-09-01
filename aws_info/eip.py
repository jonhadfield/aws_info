#!/usr/bin/env python

def get_unassociated_eips(connection):
    all_ips = connection.get_all_addresses()
    return [x for x in all_ips if not x.instance_id]

