import re

def convert_camel_to_snake(name):
    # This stinks, but docker-machine's use of MixedCase and 'sometimes' capitalizing acronyms makes it required
    for k in ['SSH', 'IP', 'URL', 'ID', 'Vswitch', 'API', 'VLAN', 'CPU', 'CIDR', 'DNS', 'VTX', 'VBox', 'VM', 'ISO',
              'VDC', 'VApp']:
        name = name.replace(k, k.lower().capitalize())

    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def convert_keys_from_camel_to_snake(d):
    new = {}
    for k, v in d.iteritems():
        if isinstance(v, dict):
            v = convert_keys_from_camel_to_snake(v)
        new[convert_camel_to_snake(k)] = v
    return new
