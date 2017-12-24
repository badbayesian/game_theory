FROM ubuntu:16.04

RUN DEBIAN_FRONTEND=noninteractive apt-get update -y && \
    apt-get install -y \
        python3-all \
        python3-dev \
        python3-pip \
        libopenblas-dev \
        libatlas-dev \
        libblas-dev \
        liblapack-dev

RUN ln -nsf /usr/bin/python3 /usr/bin/python
RUN ln -s /usr/bin/pip3 /usr/bin/pip

RUN pip install --upgrade pip
RUN pip install -U "numpy==1.14.0rc1"
RUN pip install -U "pandas==0.18.1"
RUN pip install -U "cvxopt==1.1.6"

COPY . /src/game_theory
RUN cd /src/game_theory && python setup.py install
