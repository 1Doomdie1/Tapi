# Smtp

- **Access:** `tines.admin.smtp`
- **Import:** `from tapi.admin import Smtp`
- **Part of:** [Admin](admin.md)

Read, replace and delete the SMTP configuration that a self-hosted tenant uses to send email. The routes exist only on self-hosted tenants.

> **Careful:** `update` replaces the whole configuration, and a wrong one stops the tenant from sending email.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`get`](#get) | Get the SMTP configuration. | `GET /api/v1/admin/smtp` |
| [`update`](#update) | Create the configuration or replace all of it. | `PATCH /api/v1/admin/smtp` |
| [`delete`](#delete) | Delete the configuration that was saved through the API. | `DELETE /api/v1/admin/smtp` |

## Methods breakdown

### `get`

`GET /api/v1/admin/smtp`

Get the SMTP configuration. The password is never returned: `password_set` says whether one is saved.

**Arguments**

None.

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with the configuration: `address`, `port`, `domain`, `user_name`, `auth_type`, `encryption_mode`, `verify_ssl_certificate`, `ca_path`, `ca_file`, `open_timeout`, `read_timeout`, `source` and `password_set`, and `warnings` when there are any. |
| 403 | The tenant is not self-hosted. |

### `update`

`PATCH /api/v1/admin/smtp`

Create the configuration or replace all of it. A field that is left out is cleared, except the two timeouts.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `address` | `str` | yes | Up to 255 characters | The address of the SMTP server. |
| `port` | `int` | yes | 1 to 65535 | The port of the server. |
| `encryption_mode` | `SmtpEncryptionMode` | yes | `none`, `tls`, `starttls_auto`, `starttls_strict` | How the connection to the server is encrypted. |
| `verify_ssl_certificate` | `bool` | yes | `True`, `False` | Whether Tines verifies the certificate of the server. |
| `domain` | `str` | no | Up to 255 characters | The domain sent in the SMTP greeting. |
| `user_name` | `str` | no | Up to 255 characters | The user name for the server. Needed when `auth_type` is set. |
| `password` | `str` | no | Up to 1024 characters | The password for the server. Needed when `auth_type` is set. Tines never returns it, so send it every time. |
| `auth_type` | `SmtpAuthType` | no | `plain`, `login`, `cram_md5` | How Tines authenticates to the server. Left out, Tines does not authenticate. |
| `ca_path` | `str` | no | Up to 4096 characters | A directory of CA certificates, or a PEM file, on the installation. `ca_file` takes precedence. |
| `ca_file` | `str` | no | Up to 4096 characters | A CA certificate file on the installation. |
| `open_timeout` | `int` | no | 1 to 120 seconds | Seconds to wait for the connection to open. Tines defaults to 30. |
| `read_timeout` | `int` | no | 1 to 120 seconds | Seconds to wait for a read. Tines defaults to 30. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is `None`, or an object with `warnings`. |
| 403 | The tenant is not self-hosted. |
| 422 | The configuration is not valid. `data` has `errors`, keyed by field. |

### `delete`

`DELETE /api/v1/admin/smtp`

Delete the configuration that was saved through the API. The tenant then uses the SMTP settings of its environment.

**Arguments**

None.

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | The configuration is deleted. No data. |
| 403 | The tenant is not self-hosted. |
