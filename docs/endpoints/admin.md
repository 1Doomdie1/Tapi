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
| IP access control rules | `tines.admin.ip_access_control_rules`  | [Admin: IP access control rules](admin_ip_access_control_rules.md) | Built, writes not tried |
| Action egress control rules | `tines.admin.action_egress_control_rules` | [Admin: action egress control rules](admin_action_egress_control_rules.md) | Built, writes not tried |
| Story sync destinations | `tines.admin.sync_destinations`        | [Admin: sync destinations](admin_sync_destinations.md) | Built, writes not tried |
| Jobs                    | `tines.admin.jobs`                     | [Admin: jobs](admin_jobs.md)              | Built, not tried (dedicated tenants) |
| License                 | `tines.admin.license`                  | [Admin: license](admin_license.md)        | Built, not tried (self-hosted tenants) |
| SMTP configuration      | `tines.admin.smtp`                     | [Admin: SMTP configuration](admin_smtp.md) | Built, not tried (self-hosted tenants) |
| Custom certificate authority | `tines.admin.custom_certificate_authority` | [Admin: custom certificate authority](admin_custom_certificate_authority.md) | Built, not tried |
| User provisioning       | `tines.admin.user_provisioning`        | [Admin: user provisioning](admin_user_provisioning.md) | Built, not tried |

"Not tried" means that the routes were built from the Tines docs and the OpenAPI document and the tenant
used to check them could not run them, or they were not run on purpose. Each page says what was and
was not seen.

The run script environments are not part of this module: the OpenAPI document tags them separately and
the Tines docs have no page for them. The routes of `/api/v1/admin/scim_user_group_mapping` are not
offered, because the OpenAPI document deprecates them in favor of the user provisioning route: tapi
offers no deprecated routes.

## Access

- A key that has no access to a route gets a `404`. The Tines docs say that the health of a tunnel
  needs a tenant-level API key, and the other pages do not say which key a route needs.
- Some routes work only on some tenants. The license and SMTP routes are for self-hosted tenants, and
  the jobs routes are for dedicated tenants. Other tenants get a `403` with an object whose `error`
  says that the endpoint is not available.

## Update routes

The Tines docs show the updates of users, templates, the license, SMTP and the custom certificate
authority as `PUT`. The OpenAPI document lists them under `PUT` and `PATCH`, and tapi sends `PATCH`.
