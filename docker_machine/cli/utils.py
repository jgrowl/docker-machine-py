import re

def convert_camel_to_snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def convert_keys_from_camel_to_snake(d):
    new = {}
    for k, v in d.iteritems():
        if isinstance(v, dict):
            v = convert_keys_from_camel_to_snake(v)
        new[convert_camel_to_snake(k)] = v
    return new



# def kwargs_from_env(ssl_version=None, assert_hostname=None):
#     params = {}
#
#     return params
