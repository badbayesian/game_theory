FROM ubuntu:16.04
LABEL maintainer "badbayesian@gmail.com"

RUN DEBIAN_FRONTEND=noninteractive apt-get update -y && \
    apt-get install -y \
        python3-all \
        python3-dev \
        python3-pip \
        libopenblas-dev \
        libatlas-dev \
        libblas-dev \
        liblapack-dev \
        libglpk-dev

RUN ln -nsf /usr/bin/python3 /usr/bin/python
RUN ln -s /usr/bin/pip3 /usr/bin/pip
