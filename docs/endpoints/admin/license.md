# License

- **Access:** `tines.admin.license`
- **Import:** `from tapi.admin import License`
- **Part of:** [Admin](admin.md)

Read, apply and replace the license of a self-hosted tenant. The routes exist only on self-hosted tenants.

> **Careful:** `create` and `update` apply a license to the tenant.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`get`](#get) | Get the license of the tenant. | `GET /api/v1/admin/license` |
| [`create`](#create) | Apply the first license. | `POST /api/v1/admin/license` |
| [`update`](#update) | Replace the license. | `PATCH /api/v1/admin/license` |

## Methods breakdown

### `get`

`GET /api/v1/admin/license`

Get the license of the tenant.

**Arguments**

None.

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the license. |
| 403 | The tenant is not self-hosted. |
| 404 | The tenant has no license. |

### `create`

`POST /api/v1/admin/license`

Apply the first license. A license must not exist yet: use `update` to replace one.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `license` | `str` | yes | Signed license string, such as `TINES-company_name-ENV::LICENSE_DATA` | The license to apply. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is the applied license. |
| 403 | The tenant is not self-hosted. |
| 409 | The tenant already has a license. |
| 422 | The string is not a valid signed license. |

### `update`

`PATCH /api/v1/admin/license`

Replace the license. A license must exist already: use `create` to apply the first one.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `license` | `str` | yes | Signed license string, such as `TINES-company_name-ENV::LICENSE_DATA` | The license that replaces the current one. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the applied license. |
| 403 | The tenant is not self-hosted. |
| 404 | The tenant has no license. |
| 422 | The string is not a valid signed license. |
