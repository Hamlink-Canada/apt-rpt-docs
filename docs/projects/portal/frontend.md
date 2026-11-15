# Portal frontend

The Portal frontend is the browser-based management interface. It is a separate
Vue application that owns its components and calls the Portal backend API through
the management site's `/api` route. Public product home pages are static sites
and are deployed separately from the management application.

## Deployment configuration

The production Docker image is generic. At startup, it merges built-in defaults,
an optional JSON file mounted at `/etc/portal/config.json`, then environment
variables. Environment variables override matching file fields. The frontend
fetches `/config.json` before starting, and that endpoint prevents browser
caching.

| Environment variable | JSON field | Required | Default |
| --- | --- | --- | --- |
| `PORTAL_MANAGEMENT_DISPLAY_NAME` | `managementDisplayName` | No | `Portal` |
| `PORTAL_OIDC_AUTHORITY` | `oidcAuthority` | Yes | — |
| `PORTAL_OIDC_CLIENT_ID` | `oidcClientId` | Yes | — |
| `PORTAL_ACCOUNT_MANAGEMENT_URL` | `accountManagementUrl` | No | Derived from the OIDC authority when empty |
| `PORTAL_API_BASE_URL` | `apiBaseUrl` | No | `/api` |

The optional JSON file accepts the same fields with string values. `PORTAL_CONFIG_FILE`
can point to a different mounted path. Invalid JSON, unknown fields, missing OIDC
values, and an empty API path prevent the container from starting. These settings
are public browser configuration; never place secrets in them. Hostnames belong
in deployment and DNS settings.

Build from the `Portal-Frontend` directory using `docker build -t portal-frontend .`.
The image serves static files as a non-root user on port 8080. It supports browser
history fallback and does not proxy `/api`. Route `/api` to the backend at the
management origin, and configure the selected OpenID Connect provider with the
application root and `silent-renew.html` as redirect URIs for a public browser
client. Include the API audience in issued access tokens. Restart the container
to apply changes to environment values or the mounted config file.

For local Vite development, `VITE_MANAGEMENT_DISPLAY_NAME`, `VITE_OIDC_AUTHORITY`,
`VITE_OIDC_CLIENT_ID`, `VITE_ACCOUNT_MANAGEMENT_URL`, and `VITE_API_BASE_URL` remain
available. `VITE_API_PROXY_TARGET` is only used by the development server.

On the management origin, route `/api` to the backend and configure the web
server to fall back to `index.html` for client-side routes such as `/sites` and
`/profile`. Keep hostnames and display names in deployment configuration rather
than the reusable frontend source.

## User experience and language

The interface supports English and French. It manages Sites, Entities, and
Repeaters, including repeater enablement and registration-password rotation.
Passwords are revealed only when created or rotated. Admin-controlled enabled
status is separate from live registration freshness.

The frontend uses OpenID Connect Authorization Code with PKCE. Tokens stay in
memory and are sent as bearer tokens to the API. A development-only mock sign-in
is available for preview; it is gated to the Vite development server and does
not send requests to the backend.
