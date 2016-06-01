# docker-machine-py
A simple python wrapper for docker-machine

This is currently a really simple wrapper layer over the docker-machine command. We are simply making subprocess
calls. There is no fancy daemon to interact with like in the docker-py project. docker-py was used as a project
skeleton.

## Usage

    name = 'my_digitalocean_machine'
    
    driver_config_dict = dict(
        access_token='ACCESS_TOKEN'
        image='ubuntu-15-10-x64'
        region='nyc3'
        size='512mb'
        ipv6=False
        private_networking=False
        backups=False
        userdata=None
    )

    client = docker_machine.Client()
    driver_config = create_config_from_dict('digital_ocean', driver_config_dict)

    if not client.machine_name_exists(name):
        client.create_machine(name, self.driver_config)
        
    if client.machine_name_exists(name):
        client.remove_machine(name, force=True)

