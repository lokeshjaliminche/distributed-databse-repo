FROM python:3.5-alpine
MAINTAINER Lokesh Jaliminche <ljalimin@ucsc.edu>

ADD . /app/
WORKDIR /app

RUN python setup.py install

EXPOSE 5254
CMD ["raftd", "-c", "/app/raft.conf"]
