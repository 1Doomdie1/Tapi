# ActionEgressControlRules

- **Access:** `tines.admin.action_egress_control_rules`
- **Import:** `from tapi.admin import ActionEgressControlRules`
- **Part of:** [Admin](admin.md)

Manage the rules that restrict the outbound traffic of actions. A rule names an IP address, a range or a domain name, and the types of action that may send traffic to it. Tines applies the rules only when action egress control is enabled for the tenant.

> **Careful:** Once action egress control is enabled, a wrong rule can stop the actions of your stories from reaching the services they call. List the rules before you change any.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the rules. | `GET /api/v1/admin/action_egress_control_rules` |
| [`get`](#get) | Get a rule. | `GET /api/v1/admin/action_egress_control_rules/{rule_id}` |
| [`create`](#create) | Create a rule. | `POST /api/v1/admin/action_egress_control_rules` |
| [`update`](#update) | Replace a rule. | `PATCH /api/v1/admin/action_egress_control_rules/{rule_id}` |
| [`delete`](#delete) | Delete a rule. | `DELETE /api/v1/admin/action_egress_control_rules/{rule_id}` |

## Methods breakdown

### `list`

`GET /api/v1/admin/action_egress_control_rules`

List the rules.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `per_page` | `int` | no | 1 to 500 | Results per page. Tines defaults to 20. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `admin/action_egress_control_rules`, the rules of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |

### `get`

`GET /api/v1/admin/action_egress_control_rules/{rule_id}`

Get a rule.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `rule_id` | `int` | yes | — | The ID of the rule. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the rule. |
| 404 | The rule does not exist. |

### `create`

`POST /api/v1/admin/action_egress_control_rules`

Create a rule.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `description` | `str` | yes | — | A description of the rule. |
| `allowed_action_types` | `Sequence[EgressActionType]` | yes | `http-request`, `send-email` | The types of action that may send traffic, one or both. `send-email` is for a domain name only. |
| `ip` | `str` | no | IP address or CIDR range | The address or range that the rule covers. Send `ip` or `fqdn`, not both. |
| `fqdn` | `str` | no | Fully qualified domain name | The domain name that the rule covers. Send `ip` or `fqdn`, not both. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is the created rule. |

### `update`

`PATCH /api/v1/admin/action_egress_control_rules/{rule_id}`

Replace a rule. Send the description, the types and the `ip` or `fqdn` every time.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `rule_id` | `int` | yes | — | The ID of the rule. |
| `description` | `str` | yes | — | A description of the rule. |
| `allowed_action_types` | `Sequence[EgressActionType]` | yes | `http-request`, `send-email` | The types of action that may send traffic, one or both. `send-email` is for a domain name only. |
| `ip` | `str` | no | IP address or CIDR range | The address or range that the rule covers. Send `ip` or `fqdn`, not both. |
| `fqdn` | `str` | no | Fully qualified domain name | The domain name that the rule covers. Send `ip` or `fqdn`, not both. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the updated rule. |

### `delete`

`DELETE /api/v1/admin/action_egress_control_rules/{rule_id}`

Delete a rule.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `rule_id` | `int` | yes | — | The ID of the rule. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | The rule is deleted. No data. |
