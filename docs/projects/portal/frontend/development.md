# Portal frontend development

The frontend is a Vue and Vuetify application. It owns its components, uses
Vue Router for bookmarkable sections, and supports English and French message
catalogs.

## Set up and run

Use Node.js 22 or newer to match the production build image, install the
locked dependencies, then start Vite:

```sh
npm ci
npm run dev
```

Set the Vite variables in [Configuration](configuration.md#vite-development-settings)
for the chosen identity provider and backend. Vite proxies `/api` to
`VITE_API_PROXY_TARGET`, which defaults to `http://127.0.0.1:5000`.

## Development preview

For a frontend-only preview, set `VITE_PORTAL_DEV_MODE=true`; the mock identity
and preview watermark are enabled only under Vite. To use the real local
backend preview instead, also set `VITE_PORTAL_BACKEND_PREVIEW=true` and start
the backend using its [local preview instructions](../backend/development.md#local-preview).
The backend preview is guarded separately and uses disposable in-memory data.

## Build

Create the static production bundle with `npm run build`. The output contains
the main application and `silent-renew.html`; the Docker image serves the
bundle with Nginx. Runtime values are injected when the container starts, so a
single production bundle can be configured for different deployments.
