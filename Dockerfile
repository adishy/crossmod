FROM python:3.6-buster
LABEL maintainer="Aditya Shylesh <adishy@umich.edu>"
SHELL ["/bin/bash", "-c"]
ADD . /crossmod
WORKDIR /crossmod
RUN mkdir -p /data/databases
RUN apt-get update
RUN apt-get install -y python3-pip build-essential libssl-dev libffi-dev python3-dev python3-venv ruby-foreman
RUN cd /crossmod
RUN pip install -e .
CMD foreman start