import os

class DriverConfig(object):
    def __init__(self, driver):
        self.driver = driver

    def args(self):
        arg_dictionary = dict(map(lambda (k,v): (self._format_key(k), self._format_val(v)), vars(self).iteritems()))
        no_none_values = {k: v for k, v in arg_dictionary.items() if v is not None}
        return [item for k in no_none_values for item in (k, no_none_values[k])]

    def _format_key(self, arg):
        return '--{}-{}'.format(self.driver, arg.replace("_", "-"))

    def _format_val(self, arg):
        if (isinstance(arg, bool)):
            return 'true' if arg else 'false'
        return arg

    def _lookup_arg(self, arg, env_var=None, default=None):
        if arg is not None:
            return arg

        return default if env_var is None else os.environ.get(env_var, default)


class Amazonec2DriverConfig(DriverConfig):
    def __init__(self, access_key=None, secret_key=None, vpc_id=None, session_token=None, ami=None, region=None,
                 zone=None, subnet_id=None, security_group=None, instance_type=None, root_size=None,
                 iam_instance_profile=None, ssh_user=None, request_spot_instance=None, spot_price=None,
                 private_address_only=None, monitoring=None):
        super(Amazonec2DriverConfig, self).__init__('amazonec2')

        # Required
        self.access_key = self._lookup_arg(access_key, 'AWS_ACCESS_KEY_ID')
        self.secret_key = self._lookup_arg(secret_key, 'AWS_SECRET_ACCESS_KEY')
        self.vpc_id = self._lookup_arg(vpc_id, 'AWS_VPC_ID')

        # Optional
        self.session_token = self._lookup_arg(session_token, 'AWS_SESSION_TOKEN')
        self.ami = self._lookup_arg(ami, 'AWS_AMI')
        self.region = self._lookup_arg(region, 'AWS_DEFAULT_REGION')
        self.zone = self._lookup_arg(zone, 'AWS_ZONE')
        self.subnet_id = self._lookup_arg(subnet_id, 'AWS_SUBNET_ID')
        self.security_group = self._lookup_arg(security_group, 'AWS_SECURITY_GROUP')
        self.instance_type = self._lookup_arg(instance_type, 'AWS_INSTANCE_TYPE')
        self.root_size = self._lookup_arg(root_size, 'AWS_ROOT_SIZE')
        self.iam_instance_profile = self._lookup_arg(iam_instance_profile, 'AWS_INSTANCE_PROFILE')
        self.ssh_user = self._lookup_arg(ssh_user, 'AWS_SSH_USER')
        self.request_spot_instance = self._lookup_arg(request_spot_instance, None)
        self.spot_price = self._lookup_arg(spot_price, None)
        self.private_address_only = self._lookup_arg(private_address_only, None)
        self.monitoring = self._lookup_arg(monitoring, None)


class AzureDriverConfig(DriverConfig):
    def __init__(self, subscription_id=None, subscription_cert=None, docker_port=None, image=None, location=None,
                 password=None, publish_settings_file=None, size=None, ssh_port=None, username=None):
        super(Amazonec2DriverConfig, self).__init__('azure')

        # Required
        self.subscription_id = self._lookup_arg(subscription_id, 'AZURE_SUBSCRIPTION_ID')
        self.subscription_cert = self._lookup_arg(subscription_cert, 'AZURE_SUBSCRIPTION_CERT')

        # Optional
        self.docker_port = self._lookup_arg(docker_port, None)
        self.image = self._lookup_arg(image, 'AZURE_LOCATION')
        self.location = self._lookup_arg(location, 'AZURE_LOCATION')
        self.password = self._lookup_arg(password, None)
        self.publish_settings_file = self._lookup_arg(publish_settings_file, 'AZURE_PUBLISH_SETTINGS_FILE')
        self.size = self._lookup_arg(size, 'AZURE_SIZE')
        self.ssh_port = ssh_port
        self.username = username


class DigitaloceanDriverConfig(DriverConfig):
    def __init__(self, access_token=None, image=None, region=None, ipv6=None, private_networking=None, size=None,
                 backups=None):
        super(DigitaloceanDriverConfig, self).__init__('digitalocean')

        # Required
        self.access_token = self._lookup_arg(access_token, 'DIGITALOCEAN_ACCESS_TOKEN')

        # Optional
        self.image = self._lookup_arg(image, 'DIGITALOCEAN_IMAGE')
        self.ipv6 = self._lookup_arg(ipv6, 'DIGITALOCEAN_IPV6')
        self.region = self._lookup_arg(region, 'DIGITALOCEAN_REGION')
        self.private_networking = self._lookup_arg(private_networking, 'DIGITALOCEAN_PRIVATE_NETWORKING')
        self.size = self._lookup_arg(size, 'DIGITALOCEAN_SIZE')
        self.backups = self._lookup_arg(backups, 'DIGITALOCEAN_BACKUPS')


class ExoscaleDriverConfig(DriverConfig):
    def __init__(self, api_key=None, api_secret_key=None, url=None, instance_profile=None, disk_size=None, image=None,
                 security_group=None, availability_zone=None):
        super(ExoscaleDriverConfig, self).__init__('exoscale')

        # Required
        self.api_key = self._lookup_arg(api_key, 'EXOSCALE_API_KEY')
        self.api_secret_key = self._lookup_arg(api_secret_key, 'EXOSCALE_API_SECRET')

        # Optional
        self.url = self._lookup_arg(url, 'EXOSCALE_ENDPOINT')
        self.instance_profile = self._lookup_arg(instance_profile, 'EXOSCALE_INSTANCE_PROFILE')
        self.disk_size = self._lookup_arg(disk_size, 'EXOSCALE_DISK_SIZE')
        self.image = self._lookup_arg(image, 'EXOSCALE_IMAGE')
        self.security_group = self._lookup_arg(security_group, 'EXOSCALE_SECURITY_GROUP')
        self.availability_zone = self._lookup_arg(availability_zone, 'EXOSCALE_AVAILABILITY_ZONE')


class GoogleDriverConfig(DriverConfig):
    def __init__(self, project=None, zone=None, machine_type=None, machine_image=None, username=None, scopes=None,
                 disk_size=None, disk_type=None, address=None, preemptible=None, tags=None, use_internal_ip=None):
        super(DigitaloceanDriverConfig, self).__init__('google')

        # Required
        self.project = self._lookup_arg(project, 'GOOGLE_PROJECT')

        # Optional
        self.zone = self._lookup_arg(zone, 'GOOGLE_ZONE')
        self.machine_type = self._lookup_arg(machine_type, 'GOOGLE_MACHINE_TYPE')
        self.machine_image = self._lookup_arg(machine_image, 'GOOGLE_MACHINE_IMAGE')
        self.username = self._lookup_arg(username, 'GOOGLE_USERNAME')
        self.username = self._lookup_arg(zone, 'GOOGLE_USERNAME')
        self.scopes = self._lookup_arg(scopes, 'GOOGLE_SCOPES')
        self.disk_size = self._lookup_arg(disk_size, 'GOOGLE_DISK_SIZE')
        self.disk_type = self._lookup_arg(disk_type, 'GOOGLE_DISK_TYPE')
        self.address = self._lookup_arg(address, 'GOOGLE_ADDRESS')
        self.preemptible = self._lookup_arg(preemptible, 'GOOGLE_PREEMPTIBLE')
        self.tags = self._lookup_arg(tags, 'GOOGLE_TAGS')
        self.use_internal_ip = self._lookup_arg(use_internal_ip, 'GOOGLE_USE_INTERNAL_IP')


class GenericDriverConfig(DriverConfig):
    def __init__(self, ip_address=None, ssh_user=None, ssh_key=None, ssh_port=None):
        super(GenericDriverConfig, self).__init__('generic')

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
        super(RackspaceDriverConfig, self).__init__('rackspace')

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
        super(SoftlayerDriverConfig, self).__init__('softlayer')

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
        super(VmwarevcloudairDriverConfig, self).__init__('vmwarevcloudair')

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
        super(VmwarevsphereDriverConfig, self).__init__('vmwarevsphere')

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
