# Admin: action egress control rules

A rule restricts the outbound traffic of actions: it names an IP address, a range or a domain name,
and the types of action that may send traffic to it. Tines applies the rules only if action egress
control is enabled for the tenant, which this module cannot do. The rules are a sub-area of
[`admin`](admin.md), available as `tines.admin.action_egress_control_rules`, and the class is
`tapi.admin.ActionEgressControlRules`. Every method returns a [`Response`](../responses.md).

**Be careful with writes.** Once action egress control is enabled, a rule that is wrong can stop the
actions of your stories from reaching the services they call. Read the rules with `list` before you
change anything.

| Method                                                | HTTP route                                                |
| ----------------------------------------------------- | --------------------------------------------------------- |
| `list(...)`                                           | `GET /api/v1/admin/action_egress_control_rules`           |
| `get(rule_id=...)`                                    | `GET /api/v1/admin/action_egress_control_rules/{rule_id}` |
| `create(description=..., allowed_action_types=...)`   | `POST /api/v1/admin/action_egress_control_rules`          |
| `update(rule_id=..., description=..., allowed_action_types=...)` | `PATCH /api/v1/admin/action_egress_control_rules/{rule_id}` |
| `delete(rule_id=...)`                                 | `DELETE /api/v1/admin/action_egress_control_rules/{rule_id}` |

## The rule

| Field                  | Meaning                                                                       |
| ---------------------- | ----------------------------------------------------------------------------- |
| `id`                   | The ID of the rule.                                                           |
| `ip`                   | An IP address or a CIDR range, or `null`.                                     |
| `fqdn`                 | A fully qualified domain name, or `null`. A rule has one of `ip` and `fqdn`.  |
| `description`          | A description.                                                                |
| `allowed_action_types` | A list with `http-request`, `send-email` or both.                             |
| `created_at`           | An ISO 8601 timestamp.                                                        |
| `updated_at`           | An ISO 8601 timestamp.                                                        |

## `list()`

The endpoint is paginated, and one call returns one page; see [Pagination](../pagination.md).

| Parameter  | Type  | Meaning                                                                  |
| ---------- | ----- | ------------------------------------------------------------------------ |
| `per_page` | `int` | The number of results per page. Tines defaults to 20 and caps it at 500. |
| `page`     | `int` | The page to return, starting at 1. Tines defaults to 1.                  |

`data` is an object with `admin/action_egress_control_rules`, the rules of the page, and `meta`, the
pagination details.

## `create()` and `update()`

| Parameter              | Type                       | Meaning                                                   |
| ---------------------- | -------------------------- | --------------------------------------------------------- |
| `description`          | `str`                      | A description of the rule. Required.                      |
| `allowed_action_types` | sequence of `EgressActionType` | `http-request`, `send-email` or both. Required. `send-email` is for a domain name only, and Tines refuses any other value. |
| `ip`                   | `str`                      | An IP address or a CIDR range.                            |
| `fqdn`                 | `str`                      | A fully qualified domain name. Send `ip` or `fqdn`, not both. |

`EgressActionType` is `tapi.admin.EgressActionType`. `update` also takes `rule_id`, and `create` has
a `201` status. The Tines docs show `update` as `PUT`, and the OpenAPI document lists `PUT` and
`PATCH`. The docs say that both replace the whole rule, so `update` takes `description` and
`allowed_action_types` every time, with `ip` or `fqdn`, even when a value is unchanged.

`get(rule_id=...)` returns a rule, and `delete(rule_id=...)` has a `204` status.

## Errors

| Status | When                                                                                          |
| ------ | --------------------------------------------------------------------------------------------- |
| `400`  | `list` with a `per_page` or `page` that is not a positive integer (`['Invalid per_page: 0. per_page must be a positive integer.']`). |
| `404`  | `get` with a rule that does not exist (`['Rule not found']`).                                  |

## Not tried

Everything above was read from a tenant that had no egress rules, so no rule has been seen. Creating,
changing and deleting a rule were not run, because a rule can stop actions from working once action
egress control is enabled. The shape of a rule, the statuses of `create` and `update`, and the
messages of a refused rule come from the Tines docs and the OpenAPI document.
