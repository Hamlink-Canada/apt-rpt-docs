# Portal frontend troubleshooting

Separate browser configuration and sign-in problems from API or deployment
problems. Check the browser console and Network panel for the failing request,
then inspect the frontend container and reverse-proxy logs.

## Page does not load or deep links return 404

- Confirm Nginx is serving the frontend container and `GET /healthz` succeeds.
- Check the management host's routing and TLS certificate.
- Ensure the web server falls back to `index.html` for Vue Router paths, while
  static assets and `/config.json` are served from their expected paths.
- If the site loads but assets fail, check the browser Network panel for the
  requested asset URL and any stale cached bundle.

`/healthz` checks Nginx only. It does not establish that the API, database, or
identity provider is reachable.

## Runtime configuration is rejected or incorrect

The container writes the merged `/config.json` at startup. If startup exits,
check the container logs for invalid JSON, unknown fields, or missing required
OIDC authority/client ID values. Confirm the mounted file is at the path named
by `PORTAL_CONFIG_FILE` and that environment overrides are spelled correctly.
Restart the container after changing its file or environment.

The browser fetches `/config.json` without caching on page load. Inspect that
response in the Network panel to see the values actually served. Runtime config
is public browser data and must not contain client secrets.

## Sign-in loops or OIDC errors

- Confirm `PORTAL_OIDC_AUTHORITY` and `PORTAL_OIDC_CLIENT_ID` identify the
  expected provider and public client.
- Check the exact issuer used by the backend and the provider's registered
  redirect URI for this management origin.
- Confirm the browser can reach the provider's discovery and authorization
  endpoints, and that the local system clock is correct.
- Check the browser console for callback or PKCE errors. Verify that the
  requested callback path is served by the SPA fallback.

## API calls fail

- **404 or network error:** Check `/api` proxy routing, the backend address,
  and `VITE_API_PROXY_TARGET` when developing locally.
- **401:** Check the frontend authority/client ID and the backend's issuer and
  audience configuration. The frontend may have obtained a token for a
  different API.
- **CORS or mixed-content error:** The browser is reaching a different origin
  or protocol than expected. Route `/api` through the management origin or
  configure the deployment's allowed origins and HTTPS consistently.
- **API process is unavailable:** Check
  [Portal backend troubleshooting](../backend/troubleshooting.md).

## Local mock preview is not active

The frontend mock requires `VITE_PORTAL_DEV_MODE=true` under Vite. Backend
preview additionally requires `VITE_PORTAL_BACKEND_PREVIEW=true` and the
backend's separately guarded development preview. Production builds ignore
these preview flags. See [frontend development](development.md) and
[backend development](../backend/development.md).
