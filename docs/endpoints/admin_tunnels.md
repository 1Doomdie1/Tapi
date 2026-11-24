# Admin: tunnels

The tunnels of the tenant are a sub-area of [`admin`](admin.md), available as
`tines.admin.tunnels`, and the class is `tapi.admin.Tunnels`. The method returns a
[`Response`](../responses.md).

| Method                           | HTTP route                                       |
| -------------------------------- | ------------------------------------------------ |
| `health(tunnel_name=...)`        | `GET /api/v1/admin/tunnel/{tunnel_name}/health`  |

The route has `tunnel` in the singular. The Tines docs say that a tenant-level API key is needed.
They also list `per_page` and `page` for the route, which the OpenAPI document does not list and a
health reply has no use for, so tapi does not offer them.

## `health()`

| Parameter     | Type  | Meaning                    |
| ------------- | ----- | -------------------------- |
| `tunnel_name` | `str` | The name of the tunnel.    |

`data` is an object with `health`: `Down`, `Healthy`, `Inactive` or `Degraded`.

## Errors

| Status | When                                                                                           |
| ------ | ---------------------------------------------------------------------------------------------- |
| `404`  | The tunnel does not exist. `data` is an object with `error`, such as `Tunnel named x not found`, not a list of messages. |

## Not tried

The tenant had no tunnel, so a reply for a tunnel that exists was not read.
