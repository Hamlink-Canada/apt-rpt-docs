# Portal backend troubleshooting

Diagnose the API independently from the browser and reverse proxy. The
`GET /api/v1/health` endpoint confirms that the API process responds; it does
not check the database or OIDC provider.

## API will not start or returns database errors

1. Check application logs for the first configuration, connection, or schema
   error.
2. Confirm `PORTAL_DATABASE_URL` points to the intended database and that the
   service can resolve and reach its host and port.
3. Confirm the shared `pyCommon` migrations ran before the Portal migrations.
   The runtime account does not create or migrate tables.
4. Check that its database grants allow Portal's own tables and the shared
   `node_credentials` table to be read or changed as required.

A successful health response only proves the process is up. A missing table or
connection failure can still break API requests.

## Requests return 401 or 403

- **401 Unauthorized:** Check that the request includes a valid OIDC access
  token, the issuer exactly matches `PORTAL_OIDC_ISSUER`, and the token has the
  configured `PORTAL_API_AUDIENCE`. Check provider metadata/JWKS reachability
  and token expiry if signature validation fails.
- **403 Forbidden:** Authentication succeeded, but the account may lack the
  required resource ownership or role. Verify the user's Organisation
  membership, resource ownership, and the requested operation.
- **System Super Admin access is missing:** Check
  `PORTAL_SYSTEM_SUPER_ADMIN_CLAIM_PATH` and its expected value against the
  actual access-token claims. Do not infer the claim path from an ID token.

Never paste bearer tokens into shared logs or issue reports.

## Site IDs or Site Codes behave unexpectedly

- A Site ID remains reserved after deleting its Site. Move or remove the
  attached Repeaters before releasing the reservation with
  `portal-admin clear-site-id <site-id>`.
- If a Site Code is absent or incorrect, check whether
  `PORTAL_SITE_CODES_FILE` points to the intended mapping. An unset value uses
  the mapping bundled with the backend.
- Check the input Site ID format and the mapping contents before repeating a
  maintenance command; reservation release is a direct database change.

## Registration status is empty or stale

Portal stores only the latest registration observation. The planned Repeater
Metadata Updater is responsible for consuming registration events and
populating it. Check whether that updater is deployed and processing events
before treating an empty status as a registrar failure. Freshness is derived
from the observation time and `PORTAL_REGISTRATION_LIFETIME_SECONDS`; it is
separate from the Repeater's administrative enabled state.

For symptoms outside the API, see [Portal frontend troubleshooting](../frontend/troubleshooting.md)
and [backend operations](operations.md).
