# Info

Information about your tenant: its stack, its web server and its workers. The methods are
available as `tines.info`, and the class is `tapi.info.Info`. None of them takes an argument, and
each returns a [`Response`](../responses.md).

| Method           | HTTP route                      | Availability according to the Tines docs                          |
| ---------------- | ------------------------------- | ----------------------------------------------------------------- |
| `get()`          | `GET /api/v1/info`              | No restriction stated                                             |
| `web_stats()`    | `GET /api/v1/info/web_stats`    | Self-hosted customers only                                        |
| `worker_stats()` | `GET /api/v1/info/worker_stats` | Self-hosted customers and customers on dedicated cloud stacks     |

## `get()`

Basic information about your tenant's stack. `data` is an object with one key, `stack`:

| Field        | Meaning                                                              |
| ------------ | -------------------------------------------------------------------- |
| `name`       | The name assigned to the stack.                                      |
| `type`       | Whether the stack is dedicated or shared.                            |
| `region`     | The AWS region the stack is hosted in.                               |
| `egress_ips` | The origin IPs used for any request that originates from your tenant. |

```python
response = tines.info.get()
response.data["stack"]["region"]
```

## `web_stats()`

Operational information about your web server. `data` is the status of the Puma web server. The
documented sample contains `started_at`, `backlog`, `running`, `pool_capacity`, `busy_threads`,
`max_threads`, `requests_count` and `versions`; see the
[Puma documentation](https://puma.io/puma/file.stats.html) for what they mean.

If you run several `tines-web` containers, the statistics only reflect the container that handled
the request. Behind a load balancer that is an arbitrary container.

## `worker_stats()`

Essential information about worker statistics. `data` holds:

| Field             | Meaning                                |
| ----------------- | -------------------------------------- |
| `current_workers` | The number of active workers.          |
| `max_workers`     | The maximum number of workers allowed. |
| `queue_count`     | The number of items in the queue.      |
| `queue_latency`   | The latency of the default queue.      |

The Tines docs do not state the unit of `queue_latency`.
