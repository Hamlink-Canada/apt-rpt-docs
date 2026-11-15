Failed to create stream fd: Operation not permitted
Failed to create stream fd: Operation not permitted
Failed to create stream fd: Operation not permitted
# Portal frontend

The Portal frontend is the browser-based management interface. It is a separate
Vue application that owns its components and calls the Portal backend API through
the management site's `/api` route. Public product home pages are static sites
and are deployed separately from the management application.

## Deployment configuration

Set the display name with `VITE_MANAGEMENT_DISPLAY_NAME`. Configure the selected
OpenID Connect provider with `VITE_OIDC_AUTHORITY` and `VITE_OIDC_CLIENT_ID`; add
the application root and `silent-renew.html` as redirect URIs for a public
browser client. Include the API audience in issued access tokens.

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
