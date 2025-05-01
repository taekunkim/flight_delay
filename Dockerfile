FROM python:3.11-slim

WORKDIR /usr/src/app

# install python dependencies
COPY ./src /usr/src/app/src
COPY ./config /usr/src/app/config

RUN \
    apt-get update && \
    apt-get -y install libpq-dev gcc && \
    pip install --no-cache-dir -r /usr/src/app/config/requirements.txt
