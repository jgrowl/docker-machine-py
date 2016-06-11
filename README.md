# docker-machine-py

[![Build Status](https://travis-ci.org/jgrowl/docker-machine-py.svg?branch=master)](https://travis-ci.org/jgrowl/docker-machine-py)

A Python library for the Docker Machine CLI. It does everything the docker-machine command does, but from within Python 
– create machines, check status, get ip, run ssh commands, regenerate certificates, etc.

## Installation

The latest stable version is always available on PyPi.

    pip install docker-py

## Usage

    import docker_machine
    machine = Machine('my_digitalocean_machine')
    if not machine.exists():
        machine.create('digitalocean', access_token='my_digitalocean_access_token')
        
    status = machine.status()
    machine.rm(force=True)
    
### Customizing the client
    
    docker_machine.CLIENT = docker_machine.cli.client.Client(storage_path=None, storage_path=None, tls_ca_cert=None, 
        tls_ca_key=None, tls_client_cert=None, tls_client_key=None, github_api_token=None, native_ssh=False, 
        bugsnag_api_token=None)
    
## Using the lower level wrapper 
    
If you need more control or wish to interact with docker-machine exactly as you would from cli you can use the client
directly.
    
    import docker_machine
    client = Client()
    
