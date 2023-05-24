FROM python:3.9-slim-buster AS builder

RUN python -m pip install --no-cache-dir --upgrade pip \
    && pip install pipenv

    ### for confluent-kafka
RUN apt-get update && apt-get install -y \ 
        librdkafka-dev \
    #
    ## Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* 