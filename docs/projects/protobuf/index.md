# Repeater protobuf definitions

This library defines the messages used by the repeater DNS directory and registration
services. Service images include the bindings they need, so operators do not need
to install or run this project separately. There is no runtime container or PyPI
release for this library.

If you are deploying a service, start with its own instructions:

- [DNS directory](https://github.com/Hamlink-Canada/dnsserver): serve node lookups.
- [HTTP registrar](https://github.com/Hamlink-Canada/pyHTTP-Register): accept HTTP registrations.
- [IAX registrar](https://github.com/Hamlink-Canada/pyIAX-Register): accept IAX registrations.


## Pages

- [Requirements and deployment](deployment.md)
- [Configuration](configuration.md)
- [Operation and troubleshooting](operations.md)
- [Development](development.md)

Source: [rpt_protobuf](https://github.com/Hamlink-Canada/rpt_protobuf).
