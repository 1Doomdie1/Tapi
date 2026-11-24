# Tunnels

- **Access:** `tines.admin.tunnels`
- **Import:** `from tapi.admin import Tunnels`
- **Part of:** [Admin](admin.md)

Read the health of the tunnels of the tenant. It needs a tenant-level API key.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`health`](#health) | Get the health of a tunnel. | `GET /api/v1/admin/tunnel/{tunnel_name}/health` |

## Methods breakdown

### `health`

`GET /api/v1/admin/tunnel/{tunnel_name}/health`

Get the health of a tunnel.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `tunnel_name` | `str` | yes | — | The name of the tunnel. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `health`: `Down`, `Healthy`, `Inactive` or `Degraded`. |
| 404 | The tunnel does not exist. `data` is an object with `error`. |
