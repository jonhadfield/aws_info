from __future__ import print_function
import re
import sys
import time
from utils import spinning_cursor
spinner = spinning_cursor()

def get_orphaned_snapshots(conn):
    snapshot_to_ami = {}
    for ami in conn.get_all_images(owners=['self']):
        for (device, volume) in ami.block_device_mapping.iteritems():
            if volume.snapshot_id:
                snapshot_to_ami[volume.snapshot_id] = ami

    snapshots = dict([ (snapshot.id, snapshot) for snapshot in conn.get_all_snapshots(owner='self') ])
    orphaned = []
    for (snapshot_id, snapshot) in snapshots.iteritems():
        if not snapshot_to_ami.has_key(snapshot_id):
            if snapshot.description: # confirmation
                matched = re.search(r'ami-[0-9A-Fa-f]+', snapshot.description)
                if matched:
                    sys.stdout.write(spinner.next())
                    sys.stdout.flush()
                    time.sleep(0.05)
                    sys.stdout.write('\b')
                    try:
                        ami = conn.get_image(matched.group())
                        orphaned.append((snapshot_id, snapshot.description, snapshot.tags))
                    except:    
                        continue
    return orphaned

def get_unattached_volumes(conn):
    volumes = conn.get_all_volumes()
    return [vol for vol in volumes if not vol.attachment_state()]
    
