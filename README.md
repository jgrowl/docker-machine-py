# docker-machine-py
A simple python wrapper for docker-machine

This is currently a really simple wrapper layer over the docker-machine command. We are simply making subprocess
calls. There is no fancy daemon to interact with like in the docker-py project. docker-py was used as a project
skeleton.

I'm not sure if anyone would really want to use this library. I am working on it because I wanted to write a
docker_machine ansible module.
