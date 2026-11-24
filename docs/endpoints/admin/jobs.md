# Jobs

- **Access:** `tines.admin.jobs`
- **Import:** `from tapi.admin import Jobs`
- **Part of:** [Admin](admin.md)

Read and delete the background jobs. The routes exist only on dedicated tenants.

> **Careful:** The `delete_*` methods remove jobs for good, and the three `delete_all_*` methods remove them for the whole tenant.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list_dead`](#list_dead) | List the dead jobs. | `GET /api/v1/admin/dead_jobs` |
| [`list_in_progress`](#list_in_progress) | List the jobs that are in progress. | `GET /api/v1/admin/in_progress_jobs` |
| [`list_queued`](#list_queued) | List the queued jobs, a snapshot of the queue at the moment of the request. | `GET /api/v1/admin/queued_jobs` |
| [`list_retry`](#list_retry) | List the jobs that wait for a retry. | `GET /api/v1/admin/retry_jobs` |
| [`delete_all_dead`](#delete_all_dead) | Delete all the dead jobs of the tenant. | `DELETE /api/v1/admin/delete_all_dead_jobs` |
| [`delete_all_queued`](#delete_all_queued) | Delete all the queued jobs of the tenant. | `DELETE /api/v1/admin/delete_all_queued_jobs` |
| [`delete_all_retry`](#delete_all_retry) | Delete all the retry jobs of the tenant. | `DELETE /api/v1/admin/delete_all_retry_jobs` |
| [`delete_dead_by_action`](#delete_dead_by_action) | Delete all the dead jobs of one action. | `DELETE /api/v1/admin/actions/{action_id}/delete_all_dead_jobs` |
| [`delete_queued_by_action`](#delete_queued_by_action) | Delete all the queued jobs of one action. | `DELETE /api/v1/admin/actions/{action_id}/delete_all_queued_jobs` |
| [`delete_retry_by_action`](#delete_retry_by_action) | Delete all the retry jobs of one action. | `DELETE /api/v1/admin/actions/{action_id}/delete_all_retry_jobs` |

## Methods breakdown

### `list_dead`

`GET /api/v1/admin/dead_jobs`

List the dead jobs.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `per_page` | `int` | no | Positive integer | Results per page. Tines defaults to 20. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` holds the jobs of the page under `admin/dead_jobs`, and `meta`, the pagination details. |
| 403 | The tenant is not dedicated. |

### `list_in_progress`

`GET /api/v1/admin/in_progress_jobs`

List the jobs that are in progress.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `per_page` | `int` | no | Positive integer | Results per page. Tines defaults to 20. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` holds the jobs of the page under `admin/in_progress_jobs`, and `meta`. |
| 403 | The tenant is not dedicated. |

### `list_queued`

`GET /api/v1/admin/queued_jobs`

List the queued jobs, a snapshot of the queue at the moment of the request.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `per_page` | `int` | no | Positive integer | Results per page. Tines defaults to 20. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` holds the jobs of the page under `admin/queued_jobs`, and `meta`. |
| 403 | The tenant is not dedicated. |

### `list_retry`

`GET /api/v1/admin/retry_jobs`

List the jobs that wait for a retry.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `per_page` | `int` | no | Positive integer | Results per page. Tines defaults to 20. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` holds the jobs of the page under `admin/retry_jobs`, and `meta`. |
| 403 | The tenant is not dedicated. |

### `delete_all_dead`

`DELETE /api/v1/admin/delete_all_dead_jobs`

Delete all the dead jobs of the tenant.

**Arguments**

None.

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | The jobs are deleted. No data. |

### `delete_all_queued`

`DELETE /api/v1/admin/delete_all_queued_jobs`

Delete all the queued jobs of the tenant.

**Arguments**

None.

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | The jobs are deleted. No data. |

### `delete_all_retry`

`DELETE /api/v1/admin/delete_all_retry_jobs`

Delete all the retry jobs of the tenant.

**Arguments**

None.

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | The jobs are deleted. No data. |

### `delete_dead_by_action`

`DELETE /api/v1/admin/actions/{action_id}/delete_all_dead_jobs`

Delete all the dead jobs of one action.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `action_id` | `int` | yes | — | The ID of the action. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | The jobs are deleted. No data. |

### `delete_queued_by_action`

`DELETE /api/v1/admin/actions/{action_id}/delete_all_queued_jobs`

Delete all the queued jobs of one action.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `action_id` | `int` | yes | — | The ID of the action. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | The jobs are deleted. No data. |

### `delete_retry_by_action`

`DELETE /api/v1/admin/actions/{action_id}/delete_all_retry_jobs`

Delete all the retry jobs of one action.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `action_id` | `int` | yes | — | The ID of the action. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | The jobs are deleted. No data. |
