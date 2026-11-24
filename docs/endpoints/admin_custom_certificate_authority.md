# Admin: custom certificate authority

A custom certificate authority that all the IMAP and HTTP Request actions of the tenant use. It is a
sub-area of [`admin`](admin.md), available as `tines.admin.custom_certificate_authority`, and the class is
`tapi.admin.CustomCertificateAuthority`. The method returns a [`Response`](../responses.md).

**Be careful with writes.** `set` changes which certificates the actions of the whole tenant trust.

| Method                      | HTTP route                                         |
| --------------------------- | -------------------------------------------------- |
| `set(certificate=...)`      | `PATCH /api/v1/admin/custom_certificate_authority` |

There is no operation to read or to remove an authority in the Tines docs or in the OpenAPI document.

## `set()`

| Parameter     | Type  | Meaning                                                                          |
| ------------- | ----- | -------------------------------------------------------------------------------- |
| `certificate` | `str` | The PEM encoded X.509 public certificate, or certificate chain, of the authority. Required. |
| `name`        | `str` | The name of the authority. Tines defaults to `default`.                          |

The reply has a `200` status and no data. The Tines docs show the operation as `PUT`, and the OpenAPI
document lists `PUT` and `PATCH`. The Tines docs say that a request that fails answers `422`, and the
OpenAPI document lists no error.

## Not tried

`set` was not run, because it changes what the actions of the tenant trust and there is no route to
undo it. Nothing about it comes from a reply of Tines: it follows the Tines docs and the OpenAPI
document.
