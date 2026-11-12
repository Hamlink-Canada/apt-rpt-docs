# Requirements and deployment

## Run the service

Choose a versioned image from `ghcr.io/hamlink-canada/register-dns_server` when a release
is available. To run this checkout before an image is published, follow
[Build an image](#build-an-image) and use `rpt-dnsserver:local` below.

Replace the broker address and node domain with your own:

```sh
IMAGE=rpt-dnsserver:local

docker run -d --name rpt-dns --restart unless-stopped \
  --publish 5054:5054/udp \
  --publish 5054:5054/tcp \
  --env RPT_KAFKA__BOOTSTRAP=kafka.example.org:9092 \
  --env RPT_KAFKA__TOPIC=rpt.registrations \
  --env RPT_DOMAIN=nodes.example.org \
  "$IMAGE"
```

The Kafka topic must contain compatible registration messages. The broker addresses
advertised by Kafka must also be reachable from the container.

The example listens on host port 5054 so you can try it without replacing an existing
DNS server. To serve standard DNS traffic, publish host port 53 to container port
5054 for both UDP and TCP. Configure your resolver to send queries for the chosen
node domain to this service.

## Build an image

From the service repository checkout, with Docker Buildx and Python 3.13+ installed:

```sh
PROTOBUF_REV=$(python3 scripts/dependency.py)
docker buildx build --load \
  --build-context "rpt_protobuf=https://github.com/Hamlink-Canada/rpt_protobuf.git#${PROTOBUF_REV}" \
  --tag rpt-dnsserver:local .
```

This fetches the public protobuf dependency from its `main` branch. CI resolves that
branch once per run and uses the same revision for its test and image jobs.
The image runs as UID/GID 10001 and starts `rpt-dns`. Configuration files mounted into
the container must be readable by that user.
