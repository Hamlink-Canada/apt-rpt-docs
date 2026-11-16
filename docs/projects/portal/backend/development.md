# Portal backend development

The backend requires Python 3.13 or newer and `uv`. During local development,
the `uv` source override in `pyproject.toml` points `rpt-common` at the sibling
`../pyCommon` checkout.

## Set up and run

```sh
uv sync
export PORTAL_DATABASE_URL='sqlite:///portal.db'
uv run python -m portal_backend
```

The local module entry point runs Flask at `PORTAL_BIND_HOST` and
`PORTAL_BIND_PORT`. Apply shared and Portal migrations before using a persistent
database. The local `.env.example` is a reference only; export values or use
Dynaconf TOML files because dotenv loading is disabled.

## Local preview

The mock OIDC preview requires both
`PORTAL_ENVIRONMENT=development` and `PORTAL_DEV_MODE=true`. The module entry
point enables Flask debug mode for this setting; the app factory refuses to
enable preview in a non-debug, non-test app. Preview forces an in-memory SQLite
database, applies current migrations, and seeds disposable records. Its mock
identity issues short-lived tokens signed with an ephemeral process key. All
preview data is discarded when the process exits. Never enable these settings
in deployment.

The frontend can connect its `VITE_PORTAL_BACKEND_PREVIEW` mode to this local
API while both applications are being developed.

## Tests and API schema

Run the backend's focused test suite with `uv run pytest`. For the generated
OpenAPI document, use the command in [Operations](operations.md#api-reference).
The API route modules and Marshmallow schemas define the API contract.
