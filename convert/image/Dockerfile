FROM r.forgingsocial.com/python:3.8.15-alpine3.16
RUN apk update && \
    apk add chromium-chromedriver
COPY ./requirements.txt /tmp/
RUN python3 -m pip install --upgrade pip setuptools wheel && \
    python3 -m pip install -r /tmp/requirements.txt