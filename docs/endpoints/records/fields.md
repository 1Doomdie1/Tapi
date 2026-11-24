# Fields

- **Access:** `tines.records.fields`
- **Import:** `from tapi.records import Fields`
- **Part of:** [Records](records.md)

The large fields of a record: `JSON` and `ARTIFACT` fields, read one at a time.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`get`](#get) | Read the content of a `JSON` or `ARTIFACT` field of a record. | `GET /api/v2/records/{record_id}/fields/{field}` |

## Methods breakdown

### `get`

`GET /api/v2/records/{record_id}/fields/{field}`

Read the content of a `JSON` or `ARTIFACT` field of a record.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `record_id` | `int` | yes | — | The ID of the record. |
| `field` | `int \| str` | yes | ID, name or slug of the field | The ID, the name or the slug of the field. |
| `format` | `FieldFormat` | no | `json`, `text`, `txt`, `plain` | How to return the field. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the content of the field, without an envelope: the parsed JSON for `json`, and a `str` for `text`. |
| 400 | The field is not stored as an artifact. |
| 404 | The record or the field does not exist, or the field has no value. |
