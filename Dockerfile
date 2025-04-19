FROM python:3.11-slim

WORKDIR /usr/src/app
COPY config/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Optional: copy scripts if you want to run anything directly
COPY src/ src/
