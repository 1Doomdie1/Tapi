# Admin: license

The license of a self-hosted tenant. It is a sub-area of [`admin`](admin.md), available as
`tines.admin.license`, and the class is `tapi.admin.License`. Every method returns a
[`Response`](../responses.md). The routes exist only on self-hosted tenants.

**Be careful with writes.** `create` and `update` apply a license to the tenant.

| Method                    | HTTP route                      |
| ------------------------- | ------------------------------- |
| `get()`                   | `GET /api/v1/admin/license`     |
| `create(license=...)`     | `POST /api/v1/admin/license`    |
| `update(license=...)`     | `PATCH /api/v1/admin/license`   |

## The license

| Field                                                                          | Meaning                                                                  |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------ |
| `customer_name`, `unique_identifier`, `environment`                            | Strings that identify the license.                                       |
| `created_at`, `expires_at`                                                     | Timestamps. `expires_at` can be `null` in the OpenAPI document.          |
| `pricing_model`                                                                | A string such as `story_units`.                                          |
| `users`, `builders`, `teams`, `stories`, `story_units`, `actions`, `tunnels`, `daily_story_events`, `daily_tenant_events` | The limits of the license, as integers. |
| `features`                                                                     | A list of names, such as `AUDIT_LOGS`, `CHANGE_CONTROL` and `SSO`.        |

## Methods

| Method     | Parameter | Type  | Meaning                                                      |
| ---------- | --------- | ----- | ------------------------------------------------------------ |
| `create()` | `license` | `str` | The signed license string, such as `TINES-company_name-ENV::LICENSE_DATA`. Required. |
| `update()` | `license` | `str` | The signed license string. Required.                         |

`create` applies the first license and has a `201` status. It must not exist yet: use `update` to
replace it. `update` has a `200` status and needs a license to exist. Both return the applied
license in `data`. The Tines docs show `update` as `PUT`, and the OpenAPI document lists `PUT` and
`PATCH`.

## Errors

| Status | When                                                                                          |
| ------ | --------------------------------------------------------------------------------------------- |
| `403`  | The tenant is not self-hosted (`{"error": "This endpoint is only available on self-hosted installations"}`), or its IP access control rules or domain enforcement refuse the request. |
| `404`  | `get` or `update` on a tenant that has no license.                                            |
| `409`  | `create` on a tenant that has a license.                                                      |
| `422`  | `create` or `update` with a string that is not a valid signed license.                        |

## Not tried

The tenant used to check this module is not self-hosted, so `get` answered `403` and nothing else was
run. The shapes of the license and of the other errors come from the Tines docs and the OpenAPI
document.
