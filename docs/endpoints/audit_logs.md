# AuditLogs

- **Access:** `tines.audit_logs`
- **Import:** `from tapi.audit_logs import AuditLogs`

The audit log of the changes made in the tenant.

Every method returns a [`Response`](../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the audit logs, optionally filtered by time, user, team or operation. | `GET /api/v1/audit_logs` |

## Methods breakdown

### `list`

`GET /api/v1/audit_logs`

List the audit logs, optionally filtered by time, user, team or operation.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `before` | `datetime \| str` | no | ISO 8601 string, or `datetime` | Only logs created before this time: a `datetime` or an ISO 8601 string. |
| `after` | `datetime \| str` | no | ISO 8601 string, or `datetime` | Only logs created after this time. |
| `user_ids` | `Sequence[int]` | no | — | Only logs from these users. |
| `operation_names` | `Sequence[str]` | no | — | Only logs of these operations, such as `StoryItemsCreation`. |
| `team_ids` | `Sequence[int]` | no | — | Only logs from these teams. |
| `per_page` | `int` | no | 1 to 500 | The number of results per page, at most 500. |
| `page` | `int` | no | Positive integer | The page to return, from 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` has `audit_logs` and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | The key has no access to audit logs. |
| 422 | `before` or `after` cannot be read. |
| 429 | The rate limit was reached. `Retry-After` is in `headers`. |
