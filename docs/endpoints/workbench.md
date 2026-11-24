# Workbench

Workbench conversations are chats with Tines AI. The module reads them across every surface that
has them: Workbench itself, AI agents and story authoring. It is available as `tines.workbench`, and
the class is `tapi.workbench.Workbench`. Every method returns a [`Response`](../responses.md).

The module only reads conversations.

| Method                            | HTTP route                                 |
| --------------------------------- | ------------------------------------------ |
| `list(...)`                       | `GET /api/v1/workbench`                    |
| `get(conversation_id=...)`        | `GET /api/v1/workbench/{conversation_id}`  |

## `list()`

Lists conversations. The endpoint is paginated, and one call returns one page; see
[Pagination](../pagination.md).

All parameters are optional and keyword-only. Parameters left as `None` are not sent.

| Parameter           | Type                    | Meaning                                                                          |
| ------------------- | ----------------------- | -------------------------------------------------------------------------------- |
| `search`            | `str`                   | Only conversations whose title matches this text.                                |
| `favorited`         | `bool`                  | Only favorited conversations (`True`) or only the others (`False`). `False` is sent. |
| `creator_id`        | `int`                   | Only conversations created by the user with this ID.                             |
| `conversation_type` | `ConversationType`      | Only conversations of this type.                                                 |
| `created_after`     | `datetime` or `str`     | Only conversations created at or after this time.                                |
| `created_before`    | `datetime` or `str`     | Only conversations created at or before this time.                               |
| `per_page`          | `int`                   | The number of results per page. Tines defaults to 20 and caps it at 500.         |
| `page`              | `int`                   | The page to return, starting at 1. Tines defaults to 1.                          |

`ConversationType` is `tapi.workbench.ConversationType`: `workbench`, `task_agent`, `chat_agent` or
`workbench_storyboard`. `created_after` and `created_before` take a `datetime` or an ISO 8601 string
with a time, such as `2026-11-01T00:00:00Z`. A datetime without a timezone is treated as UTC. Tines
refuses a date without a time, such as `2020-01-01`, and `created_after` must be before
`created_before`.

```python
from datetime import UTC, datetime, timedelta

response = tines.workbench.list(
    conversation_type="workbench",
    created_after=datetime.now(UTC) - timedelta(days=7),
)
```

## `get()`

Gets one conversation with its metadata, its aggregate AI usage and its full transcript.

| Parameter         | Type  | Meaning                                                                               |
| ----------------- | ----- | ------------------------------------------------------------------------------------- |
| `conversation_id` | `str` | The GUID of the conversation: the `guid` of an item that `list` returns. The Tines docs name this path parameter `guid`. |

## The reply

`list` returns an object with `conversations`, the conversations of the page, and `meta`, the
pagination details. `get` returns the conversation itself. A conversation has:

| Field             | Meaning                                                                                     |
| ----------------- | ------------------------------------------------------------------------------------------- |
| `guid`            | The identifier of the conversation.                                                         |
| `title`           | Its title.                                                                                  |
| `source`          | Where it came from, such as `tines` or `slack`.                                             |
| `conversation_type` | `workbench`, `task_agent`, `chat_agent` or `workbench_storyboard`.                        |
| `source_type`     | The type of the resource it is linked to, such as `Story`, or `null`.                       |
| `source_id`       | The ID of that resource, or `null`.                                                         |
| `favorited`       | Whether it is favorited.                                                                    |
| `creator_id`      | The ID of the user or agent that created it.                                                |
| `creator_type`    | `User` or `Agent`.                                                                          |
| `created_at`      | An ISO 8601 timestamp.                                                                      |
| `updated_at`      | An ISO 8601 timestamp.                                                                      |
| `tool_uses_count` | The number of tool calls made during the conversation.                                      |
| `credits_used`    | The number of Tines AI credits that it used.                                                |
| `billed_cost`     | An object with `currency`, such as `usd`, and `amount`, a string with two decimals.         |

`get` adds three fields:

| Field    | Meaning                                                                                              |
| -------- | ---------------------------------------------------------------------------------------------------- |
| `status` | `in_progress`, `complete`, `cancelled` or `failed`.                                                  |
| `usage`  | The aggregate model usage: `input_tokens`, `output_tokens`, `cached_read_input_tokens` and `cached_write_input_tokens` (integers) and `model_ids`, a list of strings. |
| `steps`  | The messages of the conversation, described below.                                                   |

A message in `steps` has a `role` of `user`, `assistant` or `tool`:

- A `user` or `assistant` message has `contents`, a list of objects with a `type`. `text` has `text`.
  `reasoning`, from the assistant, has `text`, `started_at` and `completed_at`. `message_context`,
  from the user, has a `message_context` object with a `url`.
- A `tool` message has `name`, `inputs` and `output`. The keys of `output` depend on the tool. The
  Tines docs show `body`, `meta`, `status` and `headers`, which the tools seen on the tenant did not
  return.

A transcript holds whatever was asked and whatever the tools returned, including details of stories
and actions, so handle it with care.

`meta` holds `current_page`, `previous_page` and `next_page` (links), `next_page_number`, `per_page`,
`pages` and `count`. See [Pagination](../pagination.md).

## Errors

| Status | When                                                                                          |
| ------ | --------------------------------------------------------------------------------------------- |
| `400`  | `list` with a `conversation_type` that is not supported (`['conversation_type is not a valid value']`), a timestamp that is not valid (`['created_after must be an ISO8601 timestamp']`), a `created_after` that is not before `created_before` (`['created_after must be before created_before']`), and a `per_page` or `page` that is not a positive integer (`['Invalid per_page: 0. per_page must be a positive integer.']`). |
| `404`  | `get` with a GUID that does not exist, or that is not a GUID at all (`['Conversation not found']`). |

## Not tried

Everything above was tried on 2026-11-23 against a tenant that had three conversations, all of the
type `workbench_storyboard`, created by users, from `tines`, and with the status `in_progress`. These
were not seen:

- conversations of the types `workbench`, `task_agent` and `chat_agent`, a favorited conversation,
  a `source` other than `tines`, and a `creator_type` of `Agent`;
- the statuses `complete`, `cancelled` and `failed`, and a message with a role other than `user`,
  `assistant` and `tool`;
- `creator_id` of a user who has conversations.
