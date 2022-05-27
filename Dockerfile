FROM ubuntu:focal
USER 0
SHELL ["/bin/bash", "-c"]
ENV SHELL /bin/bash
WORKDIR /app
COPY pyenv_bashrc.cat /app
COPY s3util.py /app

RUN apt-get update
RUN apt-get -y install \
  apt-utils \
  curl \
  net-tools \
  iputils-ping \
  telnet \
  git \
  gcc \
  vim \
  python3-dev \
  python3-pip \
  python-is-python3

RUN pip install --upgrade pip
RUN pip install pyyaml boto3
RUN curl https://pyenv.run | bash
RUN cat /app/pyenv_bashrc.cat >> $HOME/.bashrc
