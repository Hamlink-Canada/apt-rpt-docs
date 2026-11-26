# Portal frontend deployment

The frontend repository builds a generic static application into an Nginx
container. Configure identity and API locations at deployment time so the same
image can serve different Portal deployments.

## Image and network

Use the Portal frontend image built from the `Portal-Frontend` project. Image
build instructions are in [Development](development.md#production-image).
The container serves the SPA on port `8080` as UID 101. It includes `/healthz`
for a basic web-server check, serves `/config.json` without browser caching,
and falls back to `index.html` for application routes. It does not proxy `/api`.
Configure TLS and route the management origin's `/api` path to the Portal
backend through the deployment ingress or reverse proxy. The public product
home page is a separate static website.

## Identity provider

Register the frontend as a public browser client with OIDC Authorization Code
and PKCE. Configure the management application root and `silent-renew.html` as
redirect URIs according to the identity provider's client configuration.
Include the backend API audience in issued access tokens. The browser keeps
tokens in memory and sends them as bearer tokens to the API.

## Runtime configuration

Set the `PORTAL_*` runtime variables or mount a JSON config file; see
[Configuration](configuration.md). The container merges built-in defaults,
the optional config file, then explicitly provided environment variables. It
validates required OIDC and API values at startup and exits if they are
invalid. Configuration is public and must not contain secrets.

Replace environment variables or the mounted config file and restart the
container to apply changes. The frontend fetches `/config.json` with caching
disabled when a page loads.
