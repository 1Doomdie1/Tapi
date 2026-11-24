# Artifacts

- **Access:** `tines.records.artifacts`
- **Import:** `from tapi.records import Artifacts`
- **Part of:** [Records](records.md)

The artifacts of a record: the text that an `ARTIFACT` field stores.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`get`](#get) | Get an artifact by ID. | `GET /api/v1/records/{record_id}/artifacts/{artifact_id}` |

## Methods breakdown

### `get`

`GET /api/v1/records/{record_id}/artifacts/{artifact_id}`

Get an artifact by ID.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `record_id` | `int` | yes | — | The ID of the record. |
| `artifact_id` | `int` | yes | — | The ID of the artifact. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `id`, `value` (the text), `record_field` (an object with the `id` and the `name` of the field), `created_at` and `updated_at`. |
| 404 | The record or the artifact does not exist, or the key cannot see it. |
