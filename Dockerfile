FROM python:3.6-buster
SHELL ["/bin/bash", "-c"]
COPY . /crossmod
WORKDIR /crossmod
RUN apt-get update
RUN mkdir -p /data/databases
RUN apt-get install -y python3-pip build-essential libssl-dev libffi-dev python3-dev python3-venv ruby-foreman redis-server
RUN service redis-server start
RUN cd /crossmod
RUN source crossmod_credentials.sh
RUN python3 -m venv env
RUN source env/bin/activate
RUN pip install -e .
CMD foreman start
