# Portal frontend operations

## Health and routing

Use `GET /healthz` to check whether Nginx is serving requests. It does not test
backend, database, or identity-provider availability. Confirm that the
management origin serves the application and `/config.json`, that SPA routes
fall back to `index.html`, and that `/api` reaches the backend.

## Configuration updates

The entrypoint writes the merged runtime configuration to a temporary file and
exits if configuration validation fails. To change runtime settings, update
the container environment or mounted file and restart the container. A browser
page load fetches `/config.json` with `no-store` caching to pick up the
container's current values.

## Sign-in and API access

If sign-in fails, check the OIDC authority, public client ID, redirect URIs,
and provider reachability from the user's browser. If API calls return
unauthorized responses, confirm that the frontend's access token is issued for
the backend's configured API audience and that `/api` is routed to the correct
backend. Frontend configuration must not contain client secrets.

## Product flows

The main sections are Overview, Organisations, Sites, Repeaters, and Profile.
Organisation types are Club, Association, Society, League, Union, Federation,
and Other. The form describes a Club as a common label for a local or
special-interest group, and an Association as a regional, umbrella, or
representative body. It notes that naming varies by country and offers Other
when no label fits. Call signs distinguish Primary and Alternate; a primary
call sign is required before alternates. Portal Organisation members have
Staff or Viewer roles.

Sites represent physical locations and include Site Code, coordinates, and
short or extended Node ID ranges. A Maidenhead locator can be refined with an
optional point inside its grid square. Repeaters have a call sign, frequency,
tone, Node ID, and registration credential. The credential is shown on creation
or rotation only. Administrative enablement is distinct from registration
freshness.
