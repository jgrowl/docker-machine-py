# Client CLI

To instantiate a `Client` class that will allow you to communicate with a
Docker Machine, simply do:

```python
>>> from docker_machine import Client
>>> cli = Client(storage_path='~/.docker/machine')
```


**Params**:

* storage_path (str): Configures storage path [$MACHINE_STORAGE_PATH]
* tls_ca_cert (str): CA to verify remotes against [$MACHINE_TLS_CA_CERT]
* tls_ca_key (str): Private key to generate certificates [$MACHINE_TLS_CA_KEY]
* tls_client_cert (str): Client cert to use for TLS [$MACHINE_TLS_CLIENT_CERT]
* tls_client_key (str): Private key used in client TLS auth [$MACHINE_TLS_CLIENT_KEY]
* github_api_token (str): Token to use for requests to the Github API [$MACHINE_GITHUB_API_TOKEN]
* native_ssh (str): Use the native (Go-based) SSH implementation. [$MACHINE_NATIVE_SSH]
* bugsnag_api_token (str): BugSnag API token for crash reporting [$MACHINE_BUGSNAG_API_TOKEN]

****

## active

Print which machine is active

**Params**:

* machine_name (str): The machine name 

**Returns** (str): The name of the active machine 

## config

Print the connection config for machine

**Params**:

* machine_name (str): The machine name 
* swarm (bool): Display the Swarm config instead of the Docker daemon

**Returns** (str): ???

## create

Create a machine

**Params**:

* machine_name (str): The machine name 
* driver (str): The docker-machine driver

**Returns** (ClientOutput): 

## env

Display the commands to set up the environment for the Docker client

**Params**:

* machine_name (str): The machine name 
* swarm (bool): Display the Swarm config instead of the Docker daemon
* shell (str): Force environment to be configured for a specified shell: [fish, cmd, powershell], default is sh/bash
* unset (bool): Unset variables instead of setting them
* no_proxy (bool): Add machine IP to NO_PROXY environment variable

**Returns** (ClientOutput): 

## inspect

Inspect information about a machine

**Params**:

* machine_name (str): The machine name 
* format: Format the output using the given go template.
* snake_case Converts the dictionary keys to snake_case instead of leaving them CamelCase
* named_tuple Converts the dictionary into nested namedtuples so you can use dot operator to access elements

**Returns** (ClientOutput): 

## ip

Get the IP address of a machine

**Params**:

* machine_name (str): The machine name 

**Returns** (ClientOutput): 

## kill

Kill a machine

**Params**:

* machine_name (list): The machine names

**Returns** (ClientOutput): 

## regenerate_certs

Regenerate TLS Certificates for a machine

**Params**:

* machine_name (list): The machine names
* force (bool):

**Returns** (ClientOutput): 

## restart

Restart machines

**Params**:

* machine_name (list): The machine names

**Returns** (ClientOutput): 

## rm

Removes machines

**Params**:

* machine_name (list): The machine names

**Returns** (ClientOutput): 



## ssh

Log into or run a command on a machine with SSH.

**Params**:

* machine_name (str): The machine name
* command (str): The command to run

**Returns** (ClientOutput): 

## scp

Copy files between machines

**Params**:

* machine_name (str): The machine name
* src (str):
* dest (str):
* recursive (bool)

**Returns** (ClientOutput): 

## stop

Stop a machine

**Params**:

* machine_names (list): The machine name

**Returns** (ClientOutput): 

## start

Start a machine

**Params**:

* machine_names (list): The machine name

**Returns** (ClientOutput): 

## status

Get the status of a machine

**Params**:

* machine_name (str): The machine name

**Returns** (ClientOutput): 

## upgrade

Upgrade a machine to the latest version of Docker

**Params**:

* machine_name (list): The machine name

**Returns** (ClientOutput): 

## url

Get the URL of a machine

**Params**:

* machine_name (list): The machine name

**Returns** (ClientOutput): 

## version

Show the Docker Machine version or a machine docker version

**Params**:

**Returns** (ClientOutput): 

## help

Shows a list of commands or help for one command

**Params**:

* command (str): The command name

**Returns** (ClientOutput): 
