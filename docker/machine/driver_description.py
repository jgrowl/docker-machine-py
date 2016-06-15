DRIVER_DESCRIPTIONS = {
    'none': {'non_driver_keys': ['url']},
    'digitalocean': {'required': [('access_token', 'DIGITALOCEAN_ACCESS_TOKEN')]},
    'amazonec2': {'required': [
        ('access_key', 'AWS_ACCESS_KEY_ID'),
        ('secret_key', 'AWS_SECRET_ACCESS_KEY'),
        ('vpc_id', 'AWS_VPC_ID')]},
    'azure': {'required': [('subscription_id', 'AZURE_SUBSCRIPTION_ID'), ('subscription_cert', 'AZURE_SUBSCRIPTION_CERT')]},
    'exoscale': {'required': [('api_key', 'EXOSCALE_API_KEY'), ('api_secret_key', 'EXOSCALE_API_SECRET')]},
    'google': {'required': [('project', 'GOOGLE_PROJECT')]},
    'generic': {'required': [('ip_address', None)]},
    'hyperv': {},
    'openstack': {},
    'rackspace': {'required': [
        ('username', 'OS_USERNAME'),
        ('api_key', 'OS_API_KEY'),
        ('region', 'OS_REGION_NAME')]},
    'softlayer': {'required': [
        ('user', 'SOFTLAYER_USER'),
        ('api_key', 'SOFTLAYER_API_KEY'),
        ('domain', 'SOFTLAYER_DOMAIN')]},
    'virtualbox': {},
    'vmwarevcloudair': {'required': [
        ('username', 'VCLOUDAIR_USERNAME'),
        ('password', 'VCLOUDAIR_PASSWORD')]},
    'vmwarefusion': {},
    'vmwarevsphere': {'required': [
        ('username', 'VSPHERE_USERNAME'),
        ('password', 'VSPHERE_PASSWORD')]}
}
