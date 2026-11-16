# Portal frontend overview

The Portal frontend is the browser-based management interface for a Portal
deployment. It is a Vue application with Vuetify components, English and French
messages, and OIDC Authorization Code authentication with PKCE. It calls the
separate Portal backend API; the public product home page is a separate static
website.

The interface manages Organisations, physical Sites, Repeaters, and a user's
profile. Organisation profiles include membership and call signs. Sites use
Site IDs and may belong to an Organisation or user. Repeaters use Node IDs and
have administrative enablement separate from registration freshness.

## Guides

- [Deployment](deployment.md)
- [Configuration](configuration.md)
- [Operations](operations.md)
- [Development](development.md)

## Interaction patterns

Keep comparable management flows consistent across product frontends where
their needs allow it: align section navigation, list and filter behavior,
detail and edit forms, unsaved-change handling, and status language by policy.
Each frontend owns its Vue and Vuetify components; there is no shared Vuetify
package.
