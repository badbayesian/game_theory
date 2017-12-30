FROM ubuntu:16.04
LABEL maintainer "badbayesian@gmail.com"

# Init container
RUN DEBIAN_FRONTEND=noninteractive apt-get update -y

# Install dev-requirements
COPY ./dev-requirements.txt /root/
RUN xargs -a /root/dev-requirements.txt apt-get install -y

RUN ln -nsf /usr/bin/python3 /usr/bin/python
RUN ln -s /usr/bin/pip3 /usr/bin/pip

# Install python packages
COPY ./requirements.txt /root/
RUN pip install -r /root/requirements.txt

# Install local packages
COPY . /src/game_theory
RUN cd /src/game_theory && pip install -e . && python setup.py install

# Pytest
RUN cd /src/game_theory/game_theory/tests && pytest
