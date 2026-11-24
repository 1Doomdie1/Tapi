# Admin: IP access control rules

A rule names an IP address, or a range of addresses, that may access the tenant. Tines applies the
rules only if IP access control is enabled for the tenant, which this module cannot do. The rules are a
sub-area of [`admin`](admin.md), available as `tines.admin.ip_access_control_rules`, and the class is
`tapi.admin.IpAccessControlRules`. Every method returns a [`Response`](../responses.md).

**Be careful with writes.** A rule that is wrong can keep you out of your own tenant, and a request
from the address that is locked out cannot undo it. Read the rules with `list` before you change
anything.

| Method                    | HTTP route                                           |
| ------------------------- | ---------------------------------------------------- |
| `list(...)`               | `GET /api/v1/admin/ip_access_control_rules`          |
| `get(rule_id=...)`        | `GET /api/v1/admin/ip_access_control_rules/{rule_id}` |
| `create(ip=...)`          | `POST /api/v1/admin/ip_access_control_rules`         |
| `update(rule_id=...)`     | `PATCH /api/v1/admin/ip_access_control_rules/{rule_id}` |
| `delete(rule_id=...)`     | `DELETE /api/v1/admin/ip_access_control_rules/{rule_id}` |

## The rule

| Field         | Meaning                                                              |
| ------------- | -------------------------------------------------------------------- |
| `id`          | The ID of the rule.                                                  |
| `ip`          | An IP address or a CIDR range.                                       |
| `description` | A description, or `null`.                                            |
| `created_at`  | An ISO 8601 timestamp.                                               |
| `updated_at`  | An ISO 8601 timestamp.                                               |

## `list()`

The endpoint is paginated, and one call returns one page; see [Pagination](../pagination.md).

| Parameter     | Type  | Meaning                                                                  |
| ------------- | ----- | ------------------------------------------------------------------------ |
| `matching_ip` | `str` | An address or a CIDR range: only the rules that match it are returned.   |
| `per_page`    | `int` | The number of results per page. Tines defaults to 20 and caps it at 500. |
| `page`        | `int` | The page to return, starting at 1. Tines defaults to 1.                  |

`data` is an object with `admin/ip_access_control_rules`, the rules of the page, and `meta`, the
pagination details. A `matching_ip` that is not an address is a `500`, with a database error as its
message.

## `create()`, `update()`, `get()` and `delete()`

| Parameter     | Type  | Meaning                                                                      |
| ------------- | ----- | ---------------------------------------------------------------------------- |
| `ip`          | `str` | An IP address or a CIDR range, such as `192.168.1.1` or `10.0.0.0/8`. Required by `create`. |
| `description` | `str` | A description.                                                               |

`update` also takes `rule_id`, with `ip` and `description` optional. The Tines docs show it as `PUT`,
and the OpenAPI document lists `PUT` and `PATCH`. `create` has a `201` status and returns the rule.
`delete` has a `204` status.

## Errors

| Status | When                                                                                          |
| ------ | --------------------------------------------------------------------------------------------- |
| `400`  | `list` with a `per_page` or `page` that is not a positive integer (`['Invalid per_page: 0. per_page must be a positive integer.']`). |
| `404`  | `get` with a rule that does not exist (`['Rule not found']`).                                  |
| `500`  | `list` with a `matching_ip` that is not an address.                                            |

## Not tried

Everything above was read from a tenant that had no IP access control rules, so no rule has been seen.
Creating, changing and deleting a rule were not run, because a rule can lock out the key that sends
the request. These shapes come from the Tines docs and the OpenAPI document: the rule itself, the
status of `create` and `update`, and what Tines does with a `ip` that is not valid.
