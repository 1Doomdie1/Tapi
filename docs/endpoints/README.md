# Endpoints

One page for each module that tapi offers. A module is a Tines API area. It is available as an
attribute of `Tines`, such as `tines.tags`, and its class can also be used on its own with a
`Transport`. Every method returns a [`Response`](../responses.md).

A page maps each method to its HTTP route, lists the parameters and what `data` holds, and notes the
errors that the server answers with. The docstring of the method has the full description of each
parameter.

## Modules

| Module         | Attribute            | Page                                  | Covers                                                  |
| -------------- | -------------------- | ------------------------------------- | ------------------------------------------------------- |
| `ai`           | `tines.ai`           | [AI](ai.md)                           | AI providers and AI usage.                              |
| `apps`         | `tines.apps`         | [Apps](apps.md)                       | Apps built inside Tines.                                |
| `audit_logs`   | `tines.audit_logs`   | [Audit logs](audit_logs.md)           | The audit log of the changes made in the tenant.        |
| `cases`        | `tines.cases`        | [Cases](cases.md)                     | Cases and their sub-areas, from the current v2 API.     |
| `change_requests` | `tines.change_requests` | [Change requests](change_requests.md) | Listing and reading change requests across stories. The operations on one story are in `stories.change_control`. |
| `credentials`  | `tines.credentials`  | [Credentials](credentials.md)         | The secrets that actions use.                           |
| `folders`      | `tines.folders`      | [Folders](folders.md)                 | Folders that organize stories, credentials and resources. |
| `info`         | `tines.info`         | [Info](info.md)                       | Information about the tenant: its stack, web server and workers. |
| `resources`    | `tines.resources`    | [Resources](resources.md)             | Named values such as text, JSON and files.              |
| `stories`      | `tines.stories`      | [Stories](stories.md), [Stories: actions](stories_actions.md) | The automations built in Tines, with their sub-areas.   |
| `tags`         | `tines.tags`         | [Tags](tags.md)                       | Tags that classify content.                             |
| `teams`        | `tines.teams`        | [Teams](teams.md)                     | Teams and, as a sub-area, their members.                |

## Sub-areas

A sub-area is an attribute of its module, for example `tines.stories.versions` and
`tines.cases.comments`. Each is a class of its own in the package of the module. It is documented on
the page of its module, except for the actions of a story.

| Module    | Sub-areas                                                                                          |
| --------- | -------------------------------------------------------------------------------------------------- |
| `ai`      | `providers` and `usage`.                                                                           |
| `cases`   | `activities`, `assignees`, `comments`, `notes`, `tasks`, `field_values`, `metadata`, `files`, `blocks`, `linked_cases`, `records`, `subscribers`, `actions`, `fields`, `statuses`, `templates` and `webhooks`. |
| `stories` | `actions`, `events`, `links`, `notes`, `drafts`, `owners`, `recipients`, `runs`, `groups`, `versions` and `change_control`. |
| `teams`   | `members`.                                                                                         |

## Not covered yet

These Tines API areas have no methods and no page yet: `admin`, `dashboards`, `records`,
`reporting`, `scim`, `skills` and `workbench`. A page is added when its module is built.
