# Requirements and deployment

## Prepare node credentials

The default authentication backend reads a CSV file when the service starts:

```csv
node_id,password
1234,YOUR_GENERATED_PASSWORD
```

Give each node its own generated password. Use printable ASCII without whitespace;
32-character base64url passwords fit the client configuration. The file requires the
`node_id,password` header and rejects duplicate IDs. Restart the service after editing
it. Never commit a real credential file.

The container runs as UID/GID 10001. That user must be able to read the mounted file;
restrict other access using the file ownership and permissions on your host.

## Run the service

Choose a versioned image from `ghcr.io/hamlink-canada/register-pyhttp` when a release
is available. Before an image is published, [build this checkout](#build-an-image)
and use `rpt-http-register:local`.

With `credentials.csv` in the current directory, replace the broker address below:

```sh
IMAGE=rpt-http-register:local

docker run -d --name rpt-http --restart unless-stopped \
  --publish 127.0.0.1:5000:5000 \
  --mount "type=bind,src=$(pwd)/credentials.csv,dst=/run/secrets/credentials.csv,readonly" \
  --env RPT_AUTH__BACKEND=file \
  --env RPT_AUTH__FILE=/run/secrets/credentials.csv \
  --env RPT_KAFKA__BOOTSTRAP=kafka.example.org:9092 \
  --env RPT_KAFKA__TOPIC=rpt.registrations \
  --env RPT_SERVER_ID=http-1 \
  "$IMAGE"
```

This example exposes HTTP only on the host's loopback address for a host-based
reverse proxy. Point the proxy's HTTPS endpoint at `127.0.0.1:5000`. If your proxy
runs in another container, use a shared Docker network and configure its upstream
address accordingly. Kafka's advertised broker addresses must be reachable from
the registration container.

The node address comes from the HTTP connection. If the proxy supplies that address
through `X-Forwarded-For`, explicitly configure `HTTP.TRUSTED_PROXIES` with the proxy
addresses as seen by the container and `HTTP.PROXY_HOPS` with the trusted hop count.
The proxy must overwrite client-supplied forwarding headers. Forwarded addresses are
ignored by default; incorrect proxy configuration can publish the proxy's address
as the node address. For example, in `settings.toml`:

```toml
[http]
trusted_proxies = ["192.0.2.10/32"]
proxy_hops = 1
```

Replace the example CIDR with your proxy's actual address. See
[HTTP compatibility](protocol.md) for the client contract.

## Build an image

From the service repository checkout, with Docker Buildx and Python 3.13+ installed:

```sh
PROTOBUF_REV=$(python3 scripts/dependency.py)
docker buildx build --load \
  --build-context "rpt_protobuf=https://github.com/Hamlink-Canada/rpt_protobuf.git#${PROTOBUF_REV}" \
  --tag rpt-http-register:local .
```

The build uses the public protobuf library from its `main` branch. CI resolves that
branch once per run and uses the same revision for its test and image jobs.
The image starts the production WSGI server through `rpt-http`.
