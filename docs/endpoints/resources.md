# Resources

- **Access:** `tines.resources`
- **Import:** `from tapi.resources import Resources`

Named values that stories can share: text, JSON and files. Create, read, update, delete and lock them, and change the elements of a JSON resource.

Every method returns a [`Response`](../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the resources, optionally of a team or a folder. | `GET /api/v1/global_resources` |
| [`get`](#get) | Get a resource. | `GET /api/v1/global_resources/{resource_id}` |
| [`create`](#create) | Create a resource. | `POST /api/v1/global_resources` |
| [`update`](#update) | Update a resource. | `PATCH /api/v1/global_resources/{resource_id}` |
| [`delete`](#delete) | Delete a resource. | `DELETE /api/v1/global_resources/{resource_id}` |
| [`append`](#append) | Append to a resource. | `POST /api/v1/global_resources/{resource_id}/append` |
| [`remove`](#remove) | Remove an element from a resource. | `POST /api/v1/global_resources/{resource_id}/remove` |
| [`replace`](#replace) | Replace an element of a resource. | `POST /api/v1/global_resources/{resource_id}/replace` |
| [`set_locked`](#set_locked) | Lock or unlock a resource. | `PUT /api/v1/global_resources/{resource_id}/locked` |

## Methods breakdown

### `list`

`GET /api/v1/global_resources`

List the resources, optionally of a team or a folder.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | no | — | Only resources of this team. |
| `folder_id` | `int` | no | — | Only resources in this folder. |
| `filter` | `ResourceFilter` | no | `UNUSED_IN_ACTIONS` | `UNUSED_IN_ACTIONS` keeps only the resources that no action uses. |
| `include_referencing_action_ids` | `bool` | no | `True`, `False` | Whether each resource has `referencing_action_ids`. |
| `include_value` | `bool` | no | `True`, `False` | Whether each resource has `value` and `test_resource.value`. |
| `typed_value` | `bool` | no | `True`, `False` | When true, `value` is a boolean, a number, an array or an object where it holds one, instead of a string. |
| `per_page` | `int` | no | 1 to 500 | Results per page. Tines defaults to 20 and caps it at 500. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `global_resources`, the resources of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 422 | `filter` is not a valid value. |

### `get`

`GET /api/v1/global_resources/{resource_id}`

Get a resource.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `resource_id` | `int` | yes | — | The ID of the live resource to retrieve. |
| `include_referencing_action_ids` | `bool` | no | `True`, `False` | Whether the resource has `referencing_action_ids`. Tines defaults to true. |
| `typed_value` | `bool` | no | `True`, `False` | When true, `value` is a boolean, a number, an array or an object where it holds one, instead of a string. Tines defaults to false. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the resource. |
| 404 | The resource does not exist or the key has no access to it. |

### `create`

`POST /api/v1/global_resources`

Create a resource.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `name` | `str` | yes | — | The name of the resource. |
| `value` | [`ResourceValue`](#resourcevalue) | yes | A `str` (text), a `dict` or `list` (JSON), or, for a file, a `dict` with `name`, `contents` (Base64) and optionally `type` (MIME type) | The contents of the resource. |
| `team_id` | `int` | yes | — | The ID of the team the resource is created in. |
| `folder_id` | `int` | no | — | The ID of the folder to put the resource in. |
| `read_access` | `ReadAccess` | no | `TEAM`, `GLOBAL`, `SPECIFIC_TEAMS` | Where the resource can be used. `SPECIFIC_TEAMS` is a premium feature. |
| `shared_team_slugs` | `Sequence[str]` | no | — | The slugs of the teams that can use the resource. Needed to set `read_access` to `SPECIFIC_TEAMS`. |
| `description` | `str` | no | — | A description of the resource. |
| `live_resource_id` | `int` | no | — | For a test resource used in the TEST mode of change control, the ID of the live resource it corresponds to. The other optional values then default to those of the live resource. |
| `include_referencing_action_ids` | `bool` | no | `True`, `False` | Whether the reply has `referencing_action_ids`. |
| `typed_value` | `bool` | no | `True`, `False` | When true, `value` in the reply is a boolean, a number, an array or an object where it holds one, instead of a string. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is the created resource. |
| 400 | `team_id` is missing and no default team can be chosen. |
| 422 | A value is not valid. |

### `update`

`PATCH /api/v1/global_resources/{resource_id}`

Update a resource.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `resource_id` | `int` | yes | — | The ID of the live resource to update. |
| `value` | [`ResourceValue`](#resourcevalue) | yes | — | The new contents of the resource. |
| `name` | `str` | no | — | The new name of the resource. |
| `folder_id` | `int` | no | — | The ID of the folder to move the resource to. |
| `read_access` | `ReadAccess` | no | `TEAM`, `GLOBAL`, `SPECIFIC_TEAMS` | Where the resource can be used. `SPECIFIC_TEAMS` is a premium feature. |
| `shared_team_slugs` | `Sequence[str]` | no | — | The slugs of the teams that can use the resource. Needed to set `read_access` to `SPECIFIC_TEAMS`. |
| `description` | `str` | no | — | The new description of the resource. |
| `test_resource_enabled` | `bool` | no | `True`, `False` | Whether the resource is enabled for using a test resource. |
| `is_test` | `bool` | no | `True`, `False` | Whether the test resource is the one to update. It requires `test_resource_enabled` to be true and a test resource to exist. |
| `include_referencing_action_ids` | `bool` | no | `True`, `False` | Whether the reply has `referencing_action_ids`. |
| `typed_value` | `bool` | no | `True`, `False` | When true, `value` in the reply is a boolean, a number, an array or an object where it holds one, instead of a string. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the updated resource. |
| 404 | The resource does not exist or the key has no access to it. |
| 422 | `value` is missing, or the resource is locked. |

### `delete`

`DELETE /api/v1/global_resources/{resource_id}`

Delete a resource.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `resource_id` | `int` | yes | — | The ID of the live resource to delete. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The resource does not exist or the key has no access to it. |

### `append`

`POST /api/v1/global_resources/{resource_id}/append`

Append to a resource.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `resource_id` | `int` | yes | — | The ID of the live resource. |
| `value` | [`ResourceValue`](#resourcevalue) | yes | — | The string or array to append. |
| `is_test` | `bool` | no | `True`, `False` | Whether the test resource is the one to modify. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the updated value of the resource. |
| 404 | The resource does not exist or the key has no access to it. |
| 422 | The value is an object, or the resource is locked. |

### `remove`

`POST /api/v1/global_resources/{resource_id}/remove`

Remove an element from a resource.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `resource_id` | `int` | yes | — | The ID of the live resource. |
| `key` | `str` | no | — | The key to remove, for an object resource. |
| `index` | `int` | no | — | The index of the element to remove, for an array resource, counting from 0. When omitted, the last element is removed. |
| `if_value` | [`ResourceValue`](#resourcevalue) | no | — | Only remove the element if its current value matches this. |
| `is_test` | `bool` | no | `True`, `False` | Whether the test resource is the one to modify. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the removed item, or `None` when there was nothing to remove, such as a key that does not exist. |
| 404 | The resource does not exist or the key has no access to it. |
| 422 | The index is out of bounds, `if_value` does not match, or the resource is locked. |

### `replace`

`POST /api/v1/global_resources/{resource_id}/replace`

Replace an element of a resource.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `resource_id` | `int` | yes | — | The ID of the live resource. |
| `value` | [`ResourceValue`](#resourcevalue) | yes | — | The new value of the element. |
| `key` | `str` | no | — | The key to replace, for an object resource. |
| `index` | `int` | no | — | The index of the element to replace, for an array resource, counting from 0. |
| `if_value` | [`ResourceValue`](#resourcevalue) | no | — | Only replace the element if its current value matches this. |
| `is_test` | `bool` | no | `True`, `False` | Whether the test resource is the one to modify. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the updated value of the resource. |
| 404 | The resource does not exist or the key has no access to it. |
| 422 | The index is out of bounds, `if_value` does not match, or the resource is locked. |

### `set_locked`

`PUT /api/v1/global_resources/{resource_id}/locked`

Lock or unlock a resource.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `resource_id` | `int` | yes | — | The ID of the resource. |
| `locked` | `bool` | yes | `True`, `False` | True to lock the resource, false to unlock it. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with the `id` of the resource and its `locked` status. |
| 404 | The resource does not exist or the key has no access to it. |

## Types

### `ResourceValue`

One of: `str`, `int`, `float`, `bool`, `dict[str, Any]`, `list[Any]`.
