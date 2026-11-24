# Admin: SMTP configuration

The SMTP configuration that a self-hosted tenant uses to send email. It is a sub-area of
[`admin`](admin.md), available as `tines.admin.smtp`, and the class is `tapi.admin.Smtp`. Every method
returns a [`Response`](../responses.md). The routes exist only on self-hosted tenants, and the Tines
docs say that a Tines cloud tenant answers `403`.

**Be careful with writes.** `update` replaces the whole configuration, and a wrong one stops the tenant
from sending email.

| Method                                                                        | HTTP route                  |
| ----------------------------------------------------------------------------- | --------------------------- |
| `get()`                                                                       | `GET /api/v1/admin/smtp`    |
| `update(address=..., port=..., encryption_mode=..., verify_ssl_certificate=...)` | `PATCH /api/v1/admin/smtp` |
| `delete()`                                                                    | `DELETE /api/v1/admin/smtp` |

## The configuration

`get` returns an object with these fields.

| Field                                   | Meaning                                                                   |
| --------------------------------------- | ------------------------------------------------------------------------- |
| `address`, `port`                       | The SMTP server.                                                          |
| `domain`, `user_name`                   | Strings, or `null`.                                                       |
| `auth_type`                             | `plain`, `login` or `cram_md5`, or `null` when Tines does not authenticate. |
| `encryption_mode`                       | `none`, `tls`, `starttls_auto` or `starttls_strict`.                      |
| `verify_ssl_certificate`                | Whether Tines verifies the certificate of the server.                     |
| `ca_path`, `ca_file`                    | Paths on the installation, or `null`.                                     |
| `open_timeout`, `read_timeout`          | Seconds.                                                                  |
| `source`                                | `database` for the configuration saved through the API, `environment` when none was saved and the settings of the tenant environment are used. |
| `password_set`                          | Whether a password is saved. The password is never returned.              |
| `warnings`                              | An object keyed by field, when the saved configuration has warnings.      |

`SmtpAuthType` and `SmtpEncryptionMode` are `tapi.admin.SmtpAuthType` and
`tapi.admin.SmtpEncryptionMode`.

## `update()`

| Parameter                | Type                 | Meaning                                                           |
| ------------------------ | -------------------- | ----------------------------------------------------------------- |
| `address`                | `str`                | The address of the server, at most 255 characters. Required.      |
| `port`                   | `int`                | From 1 to 65535. Required.                                        |
| `encryption_mode`        | `SmtpEncryptionMode` | `none`, `tls`, `starttls_auto` or `starttls_strict`. Required.    |
| `verify_ssl_certificate` | `bool`               | Whether Tines verifies the certificate of the server. Required.   |
| `domain`                 | `str`                | The domain sent in the SMTP greeting, at most 255 characters.     |
| `user_name`              | `str`                | At most 255 characters. Required when `auth_type` is set.         |
| `password`               | `str`                | At most 1024 characters. Required when `auth_type` is set.        |
| `auth_type`              | `SmtpAuthType`       | `plain`, `login` or `cram_md5`. Left out, Tines does not authenticate. |
| `ca_path`                | `str`                | A directory of CA certificates, or a PEM file, at most 4096 characters. `ca_file` takes precedence. |
| `ca_file`                | `str`                | A CA certificate file, at most 4096 characters.                   |
| `open_timeout`           | `int`                | Seconds, from 1 to 120. Tines defaults to 30.                     |
| `read_timeout`           | `int`                | Seconds, from 1 to 120. Tines defaults to 30.                     |

The request creates the configuration or replaces all of it, so a field that is left out is cleared,
except the two timeouts. The password is never returned and the old one is not kept, so send it every
time that `auth_type` is set. `data` is `None`, or an object with `warnings`. The Tines docs show the
operation as `PUT`, and the OpenAPI document lists `PUT` and `PATCH`.

## `delete()`

Removes only the configuration saved through the API, with a `204` status, also when there was none.
The tenant then uses the SMTP settings of its environment, which are not changed.

## Errors

| Status | When                                                                                          |
| ------ | --------------------------------------------------------------------------------------------- |
| `403`  | The tenant is not self-hosted (`get` answered `{"error": "This endpoint is only available on self-hosted installations"}`). |
| `422`  | `update` with a configuration that is not valid, according to the Tines docs, with `errors`, an object of arrays keyed by field. |

## Not tried

The tenant used to check this module is not self-hosted, so `get` answered `403` and nothing else was
run. The shapes of the configuration, of the warnings and of the `422` come from the Tines docs and
the OpenAPI document, which do not list the same status codes.
