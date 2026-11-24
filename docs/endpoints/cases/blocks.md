# Blocks

- **Access:** `tines.cases.blocks`
- **Import:** `from tapi.cases import Blocks`
- **Part of:** [Cases](cases.md)

The blocks of a case: notes, files, linked cases, metadata, closure conditions, action buttons and groups of blocks. Each block holds elements.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the blocks of a case, optionally of one type or one group. | `GET /api/v2/cases/{case_id}/blocks` |
| [`get`](#get) | Get a block. | `GET /api/v2/cases/{case_id}/blocks/{block_id}` |
| [`create`](#create) | Add a block to a case. | `POST /api/v2/cases/{case_id}/blocks` |
| [`update`](#update) | Change a block. | `PATCH /api/v2/cases/{case_id}/blocks/{block_id}` |
| [`delete`](#delete) | Delete a block. | `DELETE /api/v2/cases/{case_id}/blocks/{block_id}` |
| [`get_element`](#get_element) | Get an element of a block. | `GET /api/v2/cases/{case_id}/blocks/{block_id}/elements/{element_id}` |
| [`update_element`](#update_element) | Change the content or the annotation of an element of a block. | `PATCH /api/v2/cases/{case_id}/blocks/{block_id}/elements/{element_id}` |
| [`append_element_content`](#append_element_content) | Add text to a note element of a block. | `POST /api/v2/cases/{case_id}/blocks/{block_id}/elements/{element_id}/content` |

## Methods breakdown

### `list`

`GET /api/v2/cases/{case_id}/blocks`

List the blocks of a case, optionally of one type or one group.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `block_type` | `BlockType` | no | `note`<br>`file`<br>`linked_cases`<br>`metadata`<br>`closure_conditions`<br>`case_action`<br>`block_group`<br>`html` | Only blocks of this type. |
| `block_group_id` | `int \| str` | no | ID or slug | Only blocks inside this block group. |
| `per_page` | `int` | no | Positive integer | Results per page. Tines defaults to 20. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `blocks`, the blocks of the page, and `meta`. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | The case does not exist or is not visible to the key. |

### `get`

`GET /api/v2/cases/{case_id}/blocks/{block_id}`

Get a block.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `block_id` | `int \| str` | yes | ID or slug | The ID or the slug of the block. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `block`. |
| 404 | The case or the block does not exist or is not visible to the key. |

### `create`

`POST /api/v2/cases/{case_id}/blocks`

Add a block to a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `title` | `str` | yes | — | The title of the block. |
| `block_type` | `BlockType` | yes | `note`<br>`file`<br>`linked_cases`<br>`metadata`<br>`closure_conditions`<br>`case_action`<br>`block_group`<br>`html` | The type of the block. |
| `color` | `BlockColor` | no | `primary`<br>`white`<br>`gold`<br>`magenta`<br>`green`<br>`blue`<br>`red`<br>`mint`<br>`indigo` | The color. Only note, file, block group and HTML blocks have one. |
| `elements` | [`Sequence[NoteElement \| FileElement]`](#noteelement) | no | — | The elements to put in the block: note elements or file elements. |
| `position` | `int` | no | — | The zero-based position of the block in the case. A number past the end puts the block last. |
| `hidden` | `bool` | no | `True`, `False` | Whether the block is hidden. |
| `default_collapsed` | `bool` | no | `True`, `False` | Whether the block is collapsed by default. |
| `block_group_id` | `int \| str` | no | ID or slug | The block group that holds the block. |
| `author_email` | `str` | no | — | The email address of the author of the block. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is an object with `block`. |
| 404 | The case does not exist or is not visible to the key. |

### `update`

`PATCH /api/v2/cases/{case_id}/blocks/{block_id}`

Change a block.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `block_id` | `int \| str` | yes | ID or slug | The ID or the slug of the block. |
| `title` | `str` | no | — | A new title. |
| `color` | `BlockColor` | no | `primary`<br>`white`<br>`gold`<br>`magenta`<br>`green`<br>`blue`<br>`red`<br>`mint`<br>`indigo` | A new color. |
| `position` | `int` | no | — | A new zero-based position in the case. |
| `hidden` | `bool` | no | `True`, `False` | Whether the block is hidden. |
| `default_collapsed` | `bool` | no | `True`, `False` | Whether the block is collapsed by default. |
| `block_group_id` | `int \| str` | no | ID or slug | The block group to move the block into. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `block`. |
| 404 | The case or the block does not exist or is not visible to the key. |

### `delete`

`DELETE /api/v2/cases/{case_id}/blocks/{block_id}`

Delete a block.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `block_id` | `int \| str` | yes | ID or slug | The ID or the slug of the block. |
| `include_children` | `bool` | no | `True`, `False` | For a block group: whether to delete the blocks inside it too. Without it they stay and leave the group. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The case or the block does not exist or is not visible to the key. |

### `get_element`

`GET /api/v2/cases/{case_id}/blocks/{block_id}/elements/{element_id}`

Get an element of a block.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `block_id` | `int` | yes | — | The ID of the block. |
| `element_id` | `int` | yes | — | The `element_id` of the element, not its `id`. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the element. |
| 404 | The case, the block or the element does not exist or is not visible to the key. |

### `update_element`

`PATCH /api/v2/cases/{case_id}/blocks/{block_id}/elements/{element_id}`

Change the content or the annotation of an element of a block.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `block_id` | `int` | yes | — | The ID of the block. |
| `element_id` | `int` | yes | — | The `element_id` of the element, not its `id`. |
| `content` | `str` | no | — | New content for a note element, as Markdown. |
| `author_email` | `str` | no | — | The email address of the author of a note element. |
| `annotation` | `str` | no | — | A new annotation for a file element. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the updated element. |
| 404 | The case, the block or the element does not exist or is not visible to the key. |

### `append_element_content`

`POST /api/v2/cases/{case_id}/blocks/{block_id}/elements/{element_id}/content`

Add text to a note element of a block.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `block_id` | `int` | yes | — | The ID of the block. |
| `element_id` | `int` | yes | — | The `element_id` of the element, not its `id`. |
| `content` | `str` | yes | — | The text to add, as Markdown. |
| `author_email` | `str` | no | — | The email address of the author of the note. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the updated element. |
| 404 | The case, the block or the element does not exist or is not visible to the key. |
| 422 | The element is a file element, which cannot be appended to. |

## Types

### `NoteElement`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `content` | `str` | yes | — | The content of the note. |
| `note_type` | `NoteType` | yes | `html`, `text` | The format of the content. |
| `color` | `NoteColor` | no | `white`<br>`gold`<br>`magenta`<br>`green`<br>`blue`<br>`red`<br>`mint`<br>`indigo` | The color of the note. |
| `sensitive` | `bool` | no | `True`, `False` | Whether to leave the note out of exports. |

### `FileElement`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `filename` | `str` | yes | — | The name of the file. |
| `file_contents` | `str` | yes | — | The contents of the file, Base64 encoded. |
| `annotation` | `str` | no | — | A note about the file. |
