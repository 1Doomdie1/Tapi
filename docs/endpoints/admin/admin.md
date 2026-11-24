# Admin

- **Access:** `tines.admin`
- **Import:** `from tapi.admin import Admin`

Administration of the tenant: users, roles, templates, tunnels, access and egress rules, story sync destinations, background jobs, the license, SMTP and the custom certificate authority.

## Sub-endpoints

| Class | Access | Description |
| --- | --- | --- |
| [`Users`](users.md) | `tines.admin.users` | The users of the tenant. |
| [`Roles`](roles.md) | `tines.admin.roles` | The default and custom roles. |
| [`Templates`](templates.md) | `tines.admin.templates` | The private templates. |
| [`Tunnels`](tunnels.md) | `tines.admin.tunnels` | The health of the tunnels. |
| [`IpAccessControlRules`](ip_access_control_rules.md) | `tines.admin.ip_access_control_rules` | The rules for who may access the tenant. |
| [`ActionEgressControlRules`](action_egress_control_rules.md) | `tines.admin.action_egress_control_rules` | The rules for the outbound traffic of actions. |
| [`SyncDestinations`](sync_destinations.md) | `tines.admin.sync_destinations` | The story sync destinations. |
| [`Jobs`](jobs.md) | `tines.admin.jobs` | The background jobs. Dedicated tenants only. |
| [`License`](license.md) | `tines.admin.license` | The license. Self-hosted tenants only. |
| [`Smtp`](smtp.md) | `tines.admin.smtp` | The SMTP configuration. Self-hosted tenants only. |
| [`CustomCertificateAuthority`](custom_certificate_authority.md) | `tines.admin.custom_certificate_authority` | The certificate authority of the IMAP and HTTP Request actions. |

## Methods

`Admin` has no methods of its own: each area is a sub-endpoint, reached as an attribute of `tines.admin`.
