FROM alpine:3.22

RUN apk add --no-cache python3 py3-netifaces py3-prometheus-client

COPY multicast-relay.py /

ENTRYPOINT [ "python3", "multicast-relay.py", "--foreground" ]
