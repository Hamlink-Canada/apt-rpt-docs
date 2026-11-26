# Requirements and deployment

## Run the service

Choose a versioned image from `ghcr.io/hamlink-canada/register-dns_server` when a release
is available. To run this checkout before an image is published, follow the
[development image-build instructions](development.md#build-an-image) and use
`rpt-dnsserver:local` below.

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
