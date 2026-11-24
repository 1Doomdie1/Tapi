# Assignees

- **Access:** `tines.cases.assignees`
- **Import:** `from tapi.cases import Assignees`
- **Part of:** [Cases](cases.md)

The users assigned to a case.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the assignees of a case. | `GET /api/v2/cases/{case_id}/assignees` |

## Methods breakdown

### `list`

`GET /api/v2/cases/{case_id}/assignees`

List the assignees of a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `per_page` | `int` | no | Positive integer | Results per page. Tines defaults to 20. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. Tines defaults to 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `case_id`, `assignees`, the users of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | The case does not exist or is not visible to the key. |
