# Admin

Administration of the tenant. The module is available as `tines.admin`, and the class is
`tapi.admin.Admin`. It has no methods of its own: each area of the administration is a sub-area,
available as an attribute and described on its own page. Every method returns a
[`Response`](../responses.md).

## Sub-areas

| Sub-area                | Attribute                              | Page                                      | State             |
| ----------------------- | -------------------------------------- | ----------------------------------------- | ----------------- |
| Users                   | `tines.admin.users`                    | [Admin: users](admin_users.md)            | Built             |
| Roles                   | `tines.admin.roles`                    | [Admin: roles](admin_roles.md)            | Built             |
| Templates               | `tines.admin.templates`                | [Admin: templates](admin_templates.md)    | Built             |
| Tunnels                 | `tines.admin.tunnels`                  | [Admin: tunnels](admin_tunnels.md)        | Built             |
| IP access control rules | `tines.admin.ip_access_control_rules`  |                                           | Not built yet     |
| Action egress control rules | `tines.admin.action_egress_control_rules` |                                    | Not built yet     |
| Story sync destinations | `tines.admin.sync_destinations`        |                                           | Not built yet     |
| Jobs                    | `tines.admin.jobs`                     |                                           | Not built yet     |
| License                 | `tines.admin.license`                  |                                           | Not built yet     |
| SMTP configuration      | `tines.admin.smtp`                     |                                           | Not built yet     |
| Custom certificate authority | `tines.admin.custom_certificate_authority` |                                  | Not built yet     |
| SCIM user group mapping | `tines.admin.scim_user_group_mapping`  |                                           | Not built yet     |

A page is added when its sub-area is built. The run script environments are not part of this
module: the OpenAPI document tags them separately and the Tines docs have no page for them.

## Access

- A key that has no access to a route gets a `404`. The Tines docs say that the health of a tunnel
  needs a tenant-level API key, and the other pages do not say which key a route needs.
- Some routes work only on some tenants. The license and SMTP routes are for self-hosted tenants,
  and the jobs routes are for dedicated tenants. Their sub-areas are among those not built yet.

## Update routes

The Tines docs show the updates of users and templates as `PUT`. The OpenAPI document lists them
under `PUT` and `PATCH`, and tapi sends `PATCH`.
