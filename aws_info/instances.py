def get_unnamed_instances(connection):
    reservations = [x for x in connection.get_all_instances()]
    instances = []
    for res in reservations:
        for inst in res.instances:
            if not inst.tags.get('Name', None):
                instances.append(inst)
    return instances
