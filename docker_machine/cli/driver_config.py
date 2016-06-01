import os
from .. import errors


class DriverConfig(object):
    def __init__(self, driver, required_args=[]):
        self.driver = driver
        self._require(required_args)

    def non_driver_keys(self):
        return ['driver']

    def args(self):
        arg_dictionary = {}
        for k, v in vars(self).iteritems():
            key = self._format_key(k) if k in self.non_driver_keys() else self._format_driver_key(k)
            value = self._format_val(v)
            arg_dictionary[key] = value

        no_none_values = {k: v for k, v in arg_dictionary.items() if v is not None}
        return ["{}={}".format(k, v) for k, v in no_none_values.iteritems()]

    def _format_key(self, arg):
        return '--{}'.format(arg.replace("_", "-"))

    def _format_driver_key(self, arg):
        return '--{}-{}'.format(self.driver, arg.replace("_", "-"))

    def _format_val(self, arg):
        if (isinstance(arg, bool)):
            return 'true' if arg else 'false'
        return arg

    def _lookup_arg(self, arg, env_var=None, default=None):
        if arg is not None:
            return arg

        return default if env_var is None else os.environ.get(env_var, default)

    def _require(self, tuples):
        for tuple in tuples:
            if self._lookup_arg(tuple[1], tuple[2]) is None:
                raise errors.MissingRequiredArgument(tuple[0])


class NoneDriverConfig(DriverConfig):
    def __init__(self, url='localhost'):
        super(NoneDriverConfig, self).__init__('none', [])
        self.url = url

    def non_driver_keys(self):
        return super(NoneDriverConfig, self).non_driver_keys() + ['url']


class Amazonec2DriverConfig(DriverConfig):
    def __init__(self, access_key=None, secret_key=None, vpc_id=None, session_token=None, ami=None, region=None,
                 zone=None, subnet_id=None, security_group=None, instance_type=None, root_size=None,
                 iam_instance_profile=None, ssh_user=None, request_spot_instance=None, spot_price=None,
                 private_address_only=None, monitoring=None):
        super(Amazonec2DriverConfig, self).__init__('amazonec2', [('access_key', access_key, 'AWS_ACCESS_KEY_ID'),
                                                                  ('secret_key', secret_key, 'AWS_SECRET_ACCESS_KEY'),
                                                                  ('vpc_id', vpc_id, 'AWS_VPC_ID')])

        # Required
        self.access_key = access_key
        self.secret_key = secret_key
        self.vpc_id = vpc_id

        # Optional
        self.session_token = session_token
        self.ami = ami
        self.region = region
        self.zone = zone
        self.subnet_id = subnet_id
        self.security_group = security_group
        self.instance_type = instance_type
        self.root_size = root_size
        self.iam_instance_profile = iam_instance_profile
        self.ssh_user = ssh_user
        self.request_spot_instance = request_spot_instance
        self.spot_price = spot_price
        self.private_address_only = private_address_only
        self.monitoring = monitoring


class AzureDriverConfig(DriverConfig):
    def __init__(self, subscription_id=None, subscription_cert=None, docker_port=None, image=None, location=None,
                 password=None, publish_settings_file=None, size=None, ssh_port=None, username=None):
        super(AzureDriverConfig, self).__init__('azure', [('subscription_id', subscription_id, 'AZURE_SUBSCRIPTION_ID'),
                                                          ('subscription_cert', subscription_cert, 'AZURE_SUBSCRIPTION_CERT')])

        # Required
        self.subscription_id = subscription_id
        self.subscription_cert = subscription_cert

        # Optional
        self.docker_port = docker_port
        self.image = image
        self.location = location
        self.password = password
        self.publish_settings_file = publish_settings_file
        self.size = size
        self.ssh_port = ssh_port
        self.username = username


class DigitaloceanDriverConfig(DriverConfig):
    def __init__(self, access_token=None, image=None, region=None, ipv6=None, private_networking=None, size=None,
                 backups=None, userdata=None):
        super(DigitaloceanDriverConfig, self).__init__('digitalocean', [('access_token', access_token, 'DIGITALOCEAN_ACCESS_TOKEN')])

        # Required
        self.access_token = access_token

        # Optional
        self.image = image
        self.ipv6 = ipv6
        self.region = region
        self.private_networking = private_networking
        self.size = size
        self.backups = backups
        self.userdata = userdata


class ExoscaleDriverConfig(DriverConfig):
    def __init__(self, api_key=None, api_secret_key=None, url=None, instance_profile=None, disk_size=None, image=None,
                 security_group=None, availability_zone=None):
        super(ExoscaleDriverConfig, self).__init__('exoscale', [('api_key', api_key, 'EXOSCALE_API_KEY'),
                                                                ('api_secret_key', api_secret_key, 'EXOSCALE_API_SECRET')])

        # Required
        self.api_key = api_key
        self.api_secret_key = api_secret_key

        # Optional
        self.url = url
        self.instance_profile = instance_profile
        self.disk_size = disk_size
        self.image = image
        self.security_group = security_group
        self.availability_zone = availability_zone


class GoogleDriverConfig(DriverConfig):
    def __init__(self, project=None, zone=None, machine_type=None, machine_image=None, username=None, scopes=None,
                 disk_size=None, disk_type=None, address=None, preemptible=None, tags=None, use_internal_ip=None):
        super(GoogleDriverConfig, self).__init__('google', [('project', project, 'GOOGLE_PROJECT')])

        # Required
        self.project = project

        # Optional
        self.zone = zone
        self.machine_type = machine_type
        self.machine_image = machine_image
        self.username = username
        self.scopes = scopes
        self.disk_size = disk_size
        self.disk_type = disk_type
        self.address = address
        self.preemptible = preemptible
        self.tags = tags
        self.use_internal_ip = use_internal_ip


class GenericDriverConfig(DriverConfig):
    def __init__(self, ip_address=None, ssh_user=None, ssh_key=None, ssh_port=None):
        super(GenericDriverConfig, self).__init__('generic', [('ip_address', ip_address, None)])

        # Required
        self.ip_address = ip_address

        # Optional
        self.ssh_user = ssh_user
        self.ssh_key = ssh_key
        self.ssh_port = ssh_port


class HypervDriverConfig(DriverConfig):
    def __init__(self, boot2docker_url=None, boot2docker_location=None, virtual_switch=None, disk_size=None,
                 memory=None):
        super(HypervDriverConfig, self).__init__('hyperv')

        # Optional
        self.boot2docker_url = boot2docker_url
        self.boot2docker_location = boot2docker_location
        self.virtual_switch = virtual_switch
        self.disk_size = disk_size
        self.memory = memory


class OpenstackDriverConfig(DriverConfig):
    def __init__(self, auth_url=None, flavor_name=None, flavor_id=None, image_name=None, image_id=None, insecure=None,
                 domain_name=None, domain_id=None, username=None, password=None, tenant_name=None, tenant_id=None,
                 region=None, availability_zone=None, endpoint_type=None, net_name=None, net_id=None, sec_groups=None,
                 floatingip_pool=None, ip_version=None, ssh_user=None, ssh_port=None, active_timeout=None):
        super(OpenstackDriverConfig, self).__init__('openstack')

        # Optional
        self.auth_url = auth_url
        self.flavor_name = flavor_name
        self.flavor_id = flavor_id
        self.image_name = image_name
        self.image_id = image_id
        self.insecure = insecure
        self.domain_name = domain_name
        self.domain_id = domain_id
        self.username = username
        self.password = password
        self.tenant_name = tenant_name
        self.tenant_id = tenant_id
        self.region	= region
        self.availability_zone = availability_zone
        self.endpoint_type = endpoint_type
        self.net_name = net_name
        self.net_id = net_id
        self.sec_groups	= sec_groups
        self.floatingip_pool = floatingip_pool
        self.ip_version	= ip_version
        self.ssh_user = ssh_user
        self.ssh_port = ssh_port
        self.active_timeout	= active_timeout


class RackspaceDriverConfig(DriverConfig):
    def __init__(self, username=None, api_key=None, region=None, endpoint_type=None, image_id=None, flavor_id=None,
                 ssh_user=None, ssh_port=None,docker_install=None):
        super(RackspaceDriverConfig, self).__init__('rackspace', [('username', username, 'OS_USERNAME'), ('api_key', api_key, 'OS_API_KEY'),
                                                                  ('region', region, 'OS_REGION_NAME')])

        # Required
        self.username = username
        self.api_key = api_key
        self.region = region

        # Optional
        self.endpoint_type = endpoint_type
        self.image_id = image_id
        self.flavor_id = flavor_id
        self.ssh_user = ssh_user
        self.ssh_port = ssh_port
        self.docker_install = docker_install


class SoftlayerDriverConfig(DriverConfig):
    def __init__(self, user=None, api_key=None, domain=None, memory=None, disk_size=None, region=None, cpu=None,
                 hostname=None, api_endpoint=None, hourly_billing=None, local_disk=None, private_net_only=None,
                 image=None, public_vlan_id=None, private_vlan_id=None):
        super(SoftlayerDriverConfig, self).__init__('softlayer', [('user', user, 'SOFTLAYER_USER'),
                                                                  ('api_key', api_key, 'SOFTLAYER_API_KEY'),
                                                                  ('domain', domain, 'SOFTLAYER_DOMAIN')])

        # Required
        self.user = user
        self.api_key = api_key
        self.domain = domain

        # Optional
        self.memory = memory
        self.disk_size = disk_size
        self.region = region
        self.cpu = cpu
        self.hostname = hostname
        self.api_endpoint = api_endpoint
        self.hourly_billing = hourly_billing
        self.local_disk = local_disk
        self.private_net_only = private_net_only
        self.image = image
        self.public_vlan_id = public_vlan_id
        self.private_vlan_id = private_vlan_id



class VirtualboxDriverConfig(DriverConfig):
    def __init__(self, memory=None, cpu_count=None, disk_size=None, boot2docker_url=None, import_boot2docker_vm=None,
                 hostonly_cidr=None, hostonly_nictype=None, hostonly_nicpromisc=None, no_share=None):
        super(VirtualboxDriverConfig, self).__init__('virtualbox')

        # Optional
        self.memory = memory
        self.cpu_count = cpu_count
        self.disk_size = disk_size
        self.boot2docker_url = boot2docker_url
        self.import_boot2docker_vm = import_boot2docker_vm
        self.hostonly_cidr = hostonly_cidr
        self.hostonly_nictype = hostonly_nictype
        self.hostonly_nicpromisc = hostonly_nicpromisc
        self.no_share = no_share


class VmwarevcloudairDriverConfig(DriverConfig):
    def __init__(self, username=None, password=None, computeid=None, vdcid=None, orgvdcnetwork=None, edgegateway=None,
                 publicip=None, catalog=None, catalogitem=None, provision=None, cpu_count=None, memory_size=None,
                 ssh_port=None, docker_port=None):
        super(VmwarevcloudairDriverConfig, self).__init__('vmwarevcloudair', [('username', username, 'VCLOUDAIR_USERNAME'),
                                                                              ('password', password, 'VCLOUDAIR_PASSWORD')])

        # Required
        self.username = username
        self.password = password

        # Optional
        self.computeid = computeid
        self.vdcid = vdcid
        self.orgvdcnetwork = orgvdcnetwork
        self.edgegateway = edgegateway
        self.publicip = publicip
        self.catalog = catalog
        self.catalogitem = catalogitem
        self.provision = provision
        self.cpu_count = cpu_count
        self.memory_size = memory_size
        self.ssh_port = ssh_port
        self.docker_port = docker_port


class VmwarefusionDriverConfig(DriverConfig):
    def __init__(self, boot2docker_url=None, cpu_count=None, disk_size=None, memory_size=None):

        super(VmwarefusionDriverConfig, self).__init__('vmwarefusion')

        # Optional
        self.boot2docker_url = boot2docker_url
        self.cpu_count = cpu_count
        self.disk_size = disk_size
        self.memory_size = memory_size


class VmwarevsphereDriverConfig(DriverConfig):
    def __init__(self, username=None, password=None, cpu_count=None, memory_size=None, disk_size=None,
                 boot2docker_url=None, vcenter=None, network=None, datastore=None, datacenter=None, pool=None,
                 compute_ip=None):
        super(VmwarevsphereDriverConfig, self).__init__('vmwarevsphere', [('username', username, 'VSPHERE_USERNAME'),
                                                                          ('password', password, 'VSPHERE_PASSWORD')])

        # Required
        self.username = username
        self.password = password

        # Optional
        self.cpu_count = cpu_count
        self.memory_size = memory_size
        self.disk_size = disk_size
        self.boot2docker_url = boot2docker_url
        self.vcenter = vcenter
        self.network = network
        self.datastore = datastore
        self.datacenter = datacenter
        self.pool = pool
        self.compute_ip = compute_ip


def create_config_from_dict(driver, dictionary):
    if driver is None or driver.lower() == 'none' or driver.strip() == '':
        return NoneDriverConfig(**dictionary)
    elif driver == 'amazonec2':
        return Amazonec2DriverConfig(**dictionary)
    elif driver == 'azure':
        return AzureDriverConfig(**dictionary)
    elif driver == 'digitalocean':
        return DigitaloceanDriverConfig(**dictionary)
    elif driver == 'exoscale':
        return ExoscaleDriverConfig(**dictionary)
    elif driver == 'google':
        return GoogleDriverConfig(**dictionary)
    elif driver == 'generic':
        return GenericDriverConfig(**dictionary)
    elif driver == 'hyperv':
        return HypervDriverConfig(**dictionary)
    elif driver == 'openstack':
        return OpenstackDriverConfig(**dictionary)
    elif driver == 'rackspace':
        return RackspaceDriverConfig(**dictionary)
    elif driver == 'softlayer':
        return SoftlayerDriverConfig(**dictionary)
    elif driver == 'virtualbox':
        return VirtualboxDriverConfig(**dictionary)
    elif driver == 'vmwarevcloudair':
        return VmwarevcloudairDriverConfig(**dictionary)
    elif driver == 'vmwarefusion':
        return VmwarefusionDriverConfig(**dictionary)
    elif driver == 'vmwarevsphere':
        return VmwarevsphereDriverConfig(**dictionary)

    raise errors.UnknownDriverException


def list_supported_drivers():
    return ['amazonec2', 'azure', 'digitalocean', 'exoscale', 'google', 'generic', 'hyperv', 'openstack', 'rackspace',
            'softlayer', 'virtualbox', 'vmwarevcloudair', 'vmwarefusion', 'vmwarevsphere']