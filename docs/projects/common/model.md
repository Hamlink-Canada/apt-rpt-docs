# Credential model

`rpt_common.models.credentials.NodeCredential` maps to `node_credentials`. `node_id` is an
explicit positive signed-64-bit primary key, `password` is required, and `enabled`
defaults to false. Only an enabled credential may be returned. A password is 1–79
printable ASCII characters without whitespace. There is one current credential per
node within a deployment's network, without accounts or registration history.

Python field validation rejects invalid IDs/passwords. Database constraints enforce
identity and password length; readers still validate returned passwords because
external SQL can bypass Python validation. Model representations do not include
password fields. Do not serialize models or SQL parameters into diagnostics.

Registrar service identities and tokens are separate from node credentials and are
not stored in this table. All authenticated registrars can retrieve all nodes in the
network. Separate deployments/databases isolate overlapping network node IDs.

The library imports without creating connections, loading application settings,
creating tables, or running migrations. Consumers own their sessions and connection
policies. Shared definitions and migration history remain here.
