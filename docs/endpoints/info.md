# Info

- **Access:** `tines.info`
- **Import:** `from tapi.info import Info`

Information about the tenant: its stack, its web server and its workers.

Every method returns a [`Response`](../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`get`](#get) | Get basic information about the stack of the tenant. | `GET /api/v1/info` |
| [`web_stats`](#web_stats) | Get operational information about the web server. | `GET /api/v1/info/web_stats` |
| [`worker_stats`](#worker_stats) | Get statistics about the workers. | `GET /api/v1/info/worker_stats` |

## Methods breakdown

### `get`

`GET /api/v1/info`

Get basic information about the stack of the tenant.

**Arguments**

None.

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with one key, `stack`. |

### `web_stats`

`GET /api/v1/info/web_stats`

Get operational information about the web server.

**Arguments**

None.

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the status of the Puma web server, for example `started_at`, `backlog`, `running`, `pool_capacity`, `busy_threads`, `max_threads`, `requests_count` and `versions`. |

### `worker_stats`

`GET /api/v1/info/worker_stats`

Get statistics about the workers.

**Arguments**

None.

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` holds `current_workers` (the number of active workers), `max_workers` (the maximum number of workers allowed), `queue_count` (the number of items in the queue) and `queue_latency` (the latency of the default queue). |
