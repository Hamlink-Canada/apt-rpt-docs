# Requirements and deployment

## Prepare node credentials

Create a CSV file containing a generated password for each node:

```csv
node_id,password
1234,YOUR_GENERATED_PASSWORD
```

The file requires the `node_id,password` header. IDs must be numeric and unique;
passwords must be 1–79 printable ASCII characters without whitespace. Generated
32-character base64url passwords are suitable for client configuration. The service
loads and validates the file at startup, so restart it after making changes.
Never commit a real credential file.

The container runs as UID/GID 10001. Set the host file's ownership and permissions
so that this user can read it while access by other users is restricted.

## Run the service

Choose a versioned image from `ghcr.io/hamlink-canada/rpt-iax-register` when a release
is available. Before an image is published, [build this checkout](#build-an-image)
and use `rpt-iax-register:local`.

This Linux example uses host networking to preserve the client's source address.
With `credentials.csv` in the current directory, replace the broker address below:

```sh
IMAGE=rpt-iax-register:local

docker run -d --name rpt-iax --restart unless-stopped \
  --network host \
  --mount "type=bind,src=$(pwd)/credentials.csv,dst=/run/secrets/credentials.csv,readonly" \
  --env RPT_AUTH__BACKEND=file \
  --env RPT_AUTH__FILE=/run/secrets/credentials.csv \
  --env RPT_KAFKA__BOOTSTRAP=kafka.example.org:9092 \
  --env RPT_KAFKA__TOPIC=rpt.registrations \
  --env RPT_SERVER_ID=iax-1 \
  "$IMAGE"
```

Allow incoming UDP 4569 through the host firewall. Host networking uses the host's
port directly, so another IAX service cannot occupy the same address and port.
Kafka's advertised broker addresses must also be reachable from the container.

You can use another networking arrangement if it preserves the original source
address and UDP port. Verify those values in the resulting registration before
using it for a public endpoint. See [IAX behavior](protocol.md) for protocol and
networking details.

## Build an image

From the service repository checkout, with Docker Buildx and Python 3.13+ installed:

```sh
PROTOBUF_REV=$(python3 scripts/dependency.py)
docker buildx build --load \
  --build-context "rpt_protobuf=https://github.com/Hamlink-Canada/rpt_protobuf.git#${PROTOBUF_REV}" \
  --tag rpt-iax-register:local .
```

The build fetches the public protobuf library from its `main` branch. CI resolves
that branch once per run and uses the same revision for its test and image jobs.
The image starts `rpt-iax`.
