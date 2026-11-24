# Links

- **Access:** `tines.stories.links`
- **Import:** `from tapi.stories import Links`
- **Part of:** [Stories](stories.md)

The links between the actions of a story.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`delete`](#delete) | Delete links between actions. | `DELETE /api/v1/links` |

## Methods breakdown

### `delete`

`DELETE /api/v1/links`

Delete links between actions.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `links` | [`Sequence[Link]`](#link) | yes | — | The links to delete. All of them must belong to the same story. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 500 | `links` is an empty list. |

## Types

### `Link`

A link between two actions: the `source_id` and the `receiver_id`.

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `source_id` | `int` | yes | — | The ID of the action that emits. |
| `receiver_id` | `int` | yes | — | The ID of the action that receives. |
