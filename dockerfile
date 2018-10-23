FROM ubuntu:18.04

RUN apt-get update
RUN apt install -y python3-minimal
RUN apt-get install -y python3-pip
RUN apt-get install -y maven

COPY . /root
WORKDIR /root

RUN pip3 install -r requirements.txt