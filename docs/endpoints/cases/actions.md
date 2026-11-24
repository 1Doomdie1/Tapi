# Actions

- **Access:** `tines.cases.actions`
- **Import:** `from tapi.cases import Actions`
- **Part of:** [Cases](cases.md)

The action buttons of a case: links that open a page or call a webhook.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the actions of a case. | `GET /api/v2/cases/{case_id}/actions` |
| [`get`](#get) | Get an action of a case. | `GET /api/v2/cases/{case_id}/actions/{action_id}` |
| [`create`](#create) | Add an action to a case. | `POST /api/v2/cases/{case_id}/actions` |
| [`update`](#update) | Change an action of a case. | `PATCH /api/v2/cases/{case_id}/actions/{action_id}` |
| [`delete`](#delete) | Delete an action of a case. | `DELETE /api/v2/cases/{case_id}/actions/{action_id}` |
| [`batch_update`](#batch_update) | Replace all the actions of a case. | `PUT /api/v2/cases/{case_id}/actions/batch` |

## Methods breakdown

### `list`

`GET /api/v2/cases/{case_id}/actions`

List the actions of a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `per_page` | `int` | no | — | The number of results per page. Tines defaults to 20. |
| `page` | `int` | no | — | The page to return, starting at 1. Tines defaults to 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `case_id`, `actions`, the actions of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | The case does not exist or is not visible to the key. |

### `get`

`GET /api/v2/cases/{case_id}/actions/{action_id}`

Get an action of a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `action_id` | `int` | yes | — | The ID of the action. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the action. |
| 404 | The case or the action does not exist or is not visible to the key. |

### `create`

`POST /api/v2/cases/{case_id}/actions`

Add an action to a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `url` | `str` | yes | — | The address that the action opens or calls. |
| `label` | `str` | yes | — | The name that identifies the action. |
| `action_type` | `CaseActionType` | yes | `webhook`<br>`page`<br>`chat`<br>`story`<br>`app` | The type of the action. |
| `action_text` | `str` | no | — | The text of the button. |
| `query_params` | `Mapping[str, str]` | no | — | Key-value pairs that are added to the address as a query string. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is the created action. |
| 404 | The case does not exist or is not visible to the key. |

### `update`

`PATCH /api/v2/cases/{case_id}/actions/{action_id}`

Change an action of a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `action_id` | `int` | yes | — | The ID of the action. |
| `url` | `str` | no | — | A new address. |
| `label` | `str` | no | — | A new name. |
| `action_type` | `CaseActionType` | no | `webhook`<br>`page`<br>`chat`<br>`story`<br>`app` | A new type. |
| `action_text` | `str` | no | — | New text for the button. |
| `query_params` | `Mapping[str, str]` | no | — | New key-value pairs for the query string. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the updated action. |
| 404 | The case or the action does not exist or is not visible to the key. |

### `delete`

`DELETE /api/v2/cases/{case_id}/actions/{action_id}`

Delete an action of a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `action_id` | `int` | yes | — | The ID of the action. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The case or the action does not exist or is not visible to the key. |

### `batch_update`

`PUT /api/v2/cases/{case_id}/actions/batch`

Replace all the actions of a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `actions` | [`Sequence[CaseActionInput]`](#caseactioninput) | yes | — | The new actions. They replace the actions of the case. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `case_id` and `actions`. |
| 404 | The case does not exist or is not visible to the key. |

## Types

### `CaseActionInput`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `url` | `str` | yes | — | The address that the action opens or calls. |
| `label` | `str` | yes | — | The name that identifies the action. |
| `action_type` | `CaseActionType` | yes | `webhook`<br>`page`<br>`chat`<br>`story`<br>`app` | The type of the action. |
| `action_text` | `str` | no | — | The text of the button. |
| `query_params` | `Mapping[str, str]` | no | — | Key-value pairs that are added to the address as a query string. |
