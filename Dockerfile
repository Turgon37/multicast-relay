FROM alpine:3.24

RUN apk add --no-cache python3 py3-netifaces py3-prometheus-client tzdata

COPY multicast-relay.py /
COPY ssdpDiscover.py /usr/local/bin/ssdp-discover
RUN chmod 0755 /usr/local/bin/ssdp-discover

ENTRYPOINT [ "python3", "multicast-relay.py", "--foreground" ]
