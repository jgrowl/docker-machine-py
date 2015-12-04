import os

class DriverConfig(object):
    def __init__(self, driver):
        self.driver = driver

    def args(self):
        arg_dictionary = dict(map(lambda (k,v): (self._format_key(k), self._format_val(v)), vars(self).iteritems()))
        no_none_values = {k: v for k, v in arg_dictionary.items() if v is not None}
        return [item for k in no_none_values for item in (k, no_none_values[k])]

    # @staticmethod
    def _format_key(self, arg):
        return '--{}-{}'.format(self.driver, arg.replace("_", "-"))

    # @staticmethod
    def _format_val(self, arg):
        if (isinstance(arg, bool)):
            return 'true' if arg else 'false'
        return arg

    # @staticmethod
    def _lookup_arg(self, arg, env_var=None, default=None):
        if arg is not None:
            return arg

        return default if env_var is None else os.environ.get(env_var, default)


# self. = self._lookup_arg(, '', '')


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

# class DigitaloceanDriverConfig(DriverConfig):
#     def __init__(self):
#         super(DigitaloceanDriverConfig, self).__init__('exoscale')
#
#         # Required
#
#         # Optional
