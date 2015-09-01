import boto.ec2.securitygroup as sg
def get_open_secgroups(conn):
    groups = conn.get_all_security_groups()
    open_groups = []
    for group in groups:
        has_open = False
        #print group.rules
        #print help(group.rules)
        for rule in group.rules:
            #print "--"
            #print rule.grants
            #print rule.grants.__class__.__name__
            for a in rule.grants:
                #print a
                if "0.0.0.0/0" == a.cidr_ip:
                    has_open = True
        if has_open:
            open_groups.append(group)
    return open_groups
