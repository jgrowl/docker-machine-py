FROM python:2.7
MAINTAINER Jonathan Rowlands <jonrowlands83@gmail.com>

RUN apt-get update -y && apt-get install -y unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN curl -L https://github.com/docker/machine/releases/download/v0.5.3/docker-machine_linux-amd64 > /usr/local/bin/docker-machine && \
    chmod +x /usr/local/bin/docker-machine

RUN mkdir /home/docker-machine-py
WORKDIR /home/docker-machine-py

ADD requirements.txt /home/docker-machine-py/requirements.txt
RUN pip install -r requirements.txt

ADD test-requirements.txt /home/docker-machine-py/test-requirements.txt
RUN pip install -r test-requirements.txt

ADD . /home/docker-machine-py
RUN pip install .