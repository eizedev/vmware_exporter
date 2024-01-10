FROM python:3.8-alpine

LABEL MAINTAINER="Daniel Pryor <daniel@pryorda.net>"
LABEL NAME=vmware_exporter
LABEL VERSION=0.19.0

# Install custom CA certificates, if any are given
COPY certs/* /usr/local/share/ca-certificates/
RUN update-ca-certificates

WORKDIR /opt/vmware_exporter/
COPY . /opt/vmware_exporter/

ARG buildDeps="gcc python3-dev musl-dev libffi-dev openssl openssl-dev rust cargo"

RUN set -x \
    && apk add --no-cache --update $buildDeps \
    && pip install -r requirements.txt . \
    && apk del $buildDeps

EXPOSE 9272

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["/usr/local/bin/vmware_exporter"]
