FROM ubuntu:16.04
FROM python:3.6.10-buster
FROM mongo

RUN mkdir twitter

COPY /. /twitter/.

RUN	apt-get update && \
    apt-get install emacs -y && \
    apt-get install lsof -y && \
    apt-get update && \
    apt-get install -y build-essential && \
    apt-get install -y python3-pip && \
    apt-get install -y git-core && \
    apt-get install -y parallel && \
    apt-get install -y openssh-server && \
    apt-get install -y nodejs && \
    apt-get install -y npm && \
    npm install -g mongo-express && \
    cp /usr/local/lib/node_modules/mongo-express/config.default.js /usr/local/lib/node_modules/mongo-express/config.js && \
    python3.6 -m pip install --upgrade && \
    python3.6 -m pip install wheel && \
    pip3 install -r requirements.txt
