# Notes

- **Access:** `tines.cases.notes`
- **Import:** `from tapi.cases import Notes`
- **Part of:** [Cases](cases.md)

The notes of a case.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the notes of a case, including the hidden ones. | `GET /api/v2/cases/{case_id}/notes` |
| [`get`](#get) | Get a note. | `GET /api/v2/cases/{case_id}/notes/{note_id}` |
| [`create`](#create) | Add a note to a case. | `POST /api/v2/cases/{case_id}/notes` |
| [`update`](#update) | Change a note. | `PATCH /api/v2/cases/{case_id}/notes/{note_id}` |
| [`delete`](#delete) | Delete a note. | `DELETE /api/v2/cases/{case_id}/notes/{note_id}` |
| [`append_content`](#append_content) | Add text to a note. | `POST /api/v2/cases/{case_id}/notes/{note_id}/content` |

## Methods breakdown

### `list`

`GET /api/v2/cases/{case_id}/notes`

List the notes of a case, including the hidden ones.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `per_page` | `int` | no | Positive integer | Results per page. Tines defaults to 20. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. Tines defaults to 1. |
| `resolve_mentions` | `bool` | no | `True`, `False` | Replaces user mentions with display names. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `case_id`, `notes`, the notes of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | The case does not exist or is not visible to the key. |

### `get`

`GET /api/v2/cases/{case_id}/notes/{note_id}`

Get a note.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `note_id` | `int` | yes | — | The ID of the note. |
| `resolve_mentions` | `bool` | no | `True`, `False` | Replaces user mentions with display names. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the note, with `case_id` added. |
| 404 | The case or the note does not exist or is not visible to the key. |

### `create`

`POST /api/v2/cases/{case_id}/notes`

Add a note to a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `title` | `str` | yes | — | The title of the note. |
| `content` | `str` | no | — | The content of the note, as Markdown. |
| `color` | `NoteColor` | no | `white`<br>`gold`<br>`magenta`<br>`green`<br>`blue`<br>`red`<br>`mint`<br>`indigo` | The color. Tines defaults to `white`. |
| `position` | `int` | no | — | The zero-based position of the note in the case. |
| `sensitive` | `bool` | no | `True`, `False` | Whether to leave the note out of exports. |
| `hidden` | `bool` | no | `True`, `False` | Whether the note is hidden. |
| `author_email` | `str` | no | — | The email address of the author of the note. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is the created note. |
| 404 | The case does not exist or is not visible to the key. |

### `update`

`PATCH /api/v2/cases/{case_id}/notes/{note_id}`

Change a note.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `note_id` | `int` | yes | — | The ID of the note. |
| `title` | `str` | no | — | A new title. |
| `content` | `str` | no | — | New content, as Markdown. To add to it, use `append_content`. |
| `color` | `NoteColor` | no | `white`<br>`gold`<br>`magenta`<br>`green`<br>`blue`<br>`red`<br>`mint`<br>`indigo` | A new color. |
| `position` | `int` | no | — | A new zero-based position in the case. |
| `sensitive` | `bool` | no | `True`, `False` | Whether to leave the note out of exports. |
| `hidden` | `bool` | no | `True`, `False` | Whether the note is hidden. |
| `author_email` | `str` | no | — | The email address of the author of the note. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the updated note. |
| 404 | The case or the note does not exist or is not visible to the key. |

### `delete`

`DELETE /api/v2/cases/{case_id}/notes/{note_id}`

Delete a note.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `note_id` | `int` | yes | — | The ID of the note. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The case or the note does not exist or is not visible to the key. |

### `append_content`

`POST /api/v2/cases/{case_id}/notes/{note_id}/content`

Add text to a note.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `note_id` | `int` | yes | — | The ID of the note. |
| `content` | `str` | yes | — | The text to add, as Markdown. |
| `author_email` | `str` | no | — | The email address of the author of the note. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the updated note. |
| 404 | The case or the note does not exist or is not visible to the key. |
