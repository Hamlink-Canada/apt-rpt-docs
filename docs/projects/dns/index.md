# Repeater DNS directory

This service lets clients find a registered repeater node through DNS. It reads
registration updates from Kafka and answers A, TXT, and IAX SRV queries for the node
domain you configure. Only IPv4 registrations are supported.

You need Docker, a reachable Kafka broker, and a registrar publishing to the same
Kafka topic. Each DNS instance reads the full topic and keeps its own directory in
memory. After a restart, it rebuilds that directory from Kafka and ignores expired
registrations.


## Pages

- [Requirements and deployment](deployment.md)
- [Configuration](configuration.md)
- [Operation and troubleshooting](operations.md)
- [Development](development.md)

Source: [dnsserver](https://github.com/Hamlink-Canada/dnsserver).
