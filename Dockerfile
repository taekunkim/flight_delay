FROM python:3.11-slim

WORKDIR /usr/src/app

# install python dependencies
COPY config/requirements.txt requirements.txt
RUN \
    apt-get update && \
    apt-get -y install libpq-dev gcc && \
    pip install --no-cache-dir -r requirements.txt

# Optional: copy scripts if you want to run anything directly
COPY src/ src/