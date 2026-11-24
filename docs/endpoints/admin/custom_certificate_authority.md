# CustomCertificateAuthority

- **Access:** `tines.admin.custom_certificate_authority`
- **Import:** `from tapi.admin import CustomCertificateAuthority`
- **Part of:** [Admin](admin.md)

Set the custom certificate authority that all the IMAP and HTTP Request actions of the tenant use. There is no method to read or remove it.

> **Careful:** `set` changes which certificates the actions of the whole tenant trust.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`set`](#set) | Set the certificate authority. | `PATCH /api/v1/admin/custom_certificate_authority` |

## Methods breakdown

### `set`

`PATCH /api/v1/admin/custom_certificate_authority`

Set the certificate authority.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `certificate` | `str` | yes | PEM encoded X.509 certificate, or certificate chain | The public certificate, or certificate chain, of the authority. |
| `name` | `str` | no | — | The name of the authority. Tines defaults to `default`. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | The authority is set. No data. |
| 422 | The request failed. |
