# IpAccessControlRules

- **Access:** `tines.admin.ip_access_control_rules`
- **Import:** `from tapi.admin import IpAccessControlRules`
- **Part of:** [Admin](admin.md)

Manage the IP addresses and ranges that may access the tenant. Tines applies the rules only when IP access control is enabled for the tenant.

> **Careful:** A wrong rule can lock you out of your own tenant, and a request from the address that is locked out cannot undo it. List the rules before you change any.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the rules, optionally only those that match an address. | `GET /api/v1/admin/ip_access_control_rules` |
| [`get`](#get) | Get a rule. | `GET /api/v1/admin/ip_access_control_rules/{rule_id}` |
| [`create`](#create) | Create a rule. | `POST /api/v1/admin/ip_access_control_rules` |
| [`update`](#update) | Change a rule. | `PATCH /api/v1/admin/ip_access_control_rules/{rule_id}` |
| [`delete`](#delete) | Delete a rule. | `DELETE /api/v1/admin/ip_access_control_rules/{rule_id}` |

## Methods breakdown

### `list`

`GET /api/v1/admin/ip_access_control_rules`

List the rules, optionally only those that match an address.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `matching_ip` | `str` | no | IP address or CIDR range | Only the rules that match this address or range. |
| `per_page` | `int` | no | 1 to 500 | Results per page. Tines defaults to 20. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `admin/ip_access_control_rules`, the rules of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 500 | `matching_ip` is not an address. |

### `get`

`GET /api/v1/admin/ip_access_control_rules/{rule_id}`

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

`POST /api/v1/admin/ip_access_control_rules`

Create a rule.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `ip` | `str` | yes | IP address or CIDR range, such as `192.168.1.1` or `10.0.0.0/8` | The address or range that the rule covers. |
| `description` | `str` | no | — | A description of the rule. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is the created rule. |

### `update`

`PATCH /api/v1/admin/ip_access_control_rules/{rule_id}`

Change a rule.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `rule_id` | `int` | yes | — | The ID of the rule. |
| `ip` | `str` | no | IP address or CIDR range | A new address or range. |
| `description` | `str` | no | — | A new description. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the updated rule. |

### `delete`

`DELETE /api/v1/admin/ip_access_control_rules/{rule_id}`

Delete a rule.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `rule_id` | `int` | yes | — | The ID of the rule. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | The rule is deleted. No data. |
