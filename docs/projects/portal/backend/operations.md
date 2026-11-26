# Portal backend operations

## Health and availability

`GET /api/v1/health` returns `{"status":"ok"}` when the API process responds.
It is a process availability check and does not verify database connectivity
or OIDC provider availability. Protect other API routes through the configured
OIDC bearer-token validation.

## Database changes

Apply `pyCommon` migrations before Portal migrations. Schedule schema changes
with a migration-capable database identity; the application runtime does not
create tables. Keep a backup and recovery plan for the shared database,
including the credentials that registration systems use.

## Site IDs and Site Codes

The backend loads Site Codes from its bundled mapping unless
`PORTAL_SITE_CODES_FILE` points to a deployment-managed replacement. Site ID
and Site Code are separate values: a system administrator may assign any valid,
unreserved five-digit Site ID, and its first two digits do not change the
Site's country or Site Code. Reservations remain allocated after Site deletion.
An operator can release a reservation only after removing or moving the Site's
Repeaters:

```sh
portal-admin clear-site-id 12345
```

The command requires `PORTAL_DATABASE_URL` and accepts a five-digit Site ID.
It is a direct database maintenance action; restrict who can run it and record
the change.

## Registration freshness

Portal stores the latest registration observation rather than a history. The
planned Repeater Metadata Updater consumes registration events and updates
those fields. Until that updater is deployed, do not assume the latest-status
fields are populated by the registration services. Freshness derives from
the observation time and `PORTAL_REGISTRATION_LIFETIME_SECONDS`; repeater
administrative enablement remains a separate setting.

## API reference

Generate the OpenAPI file from the registered routes and schemas after API
changes:

```sh
mkdir -p api
uv run flask --app portal_backend.app:create_app openapi write --format=json api/openapi.json
```

The app does not serve the generated document by default. Review and publish it
through the deployment's chosen documentation path.
