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

COPY ./requirements.txt /root/
RUN pip install -r /root/requirements.txt

COPY . /src/game_theory
RUN cd /src/game_theory && pip install -e . && python setup.py install

RUN cd /src/game_theory/game_theory/tests && pytest test_model.py
