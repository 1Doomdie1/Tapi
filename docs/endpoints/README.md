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
| `admin`        | `tines.admin`        | [Admin](admin.md)                     | Administration of the tenant: users, roles, templates, tunnels, IP access control rules, action egress control rules, sync destinations, jobs, the license, SMTP, and the custom certificate authority. |
| `ai`           | `tines.ai`           | [AI](ai.md)                           | AI providers and AI usage.                              |
| `apps`         | `tines.apps`         | [Apps](apps.md)                       | Apps built inside Tines.                                |
| `audit_logs`   | `tines.audit_logs`   | [Audit logs](audit_logs.md)           | The audit log of the changes made in the tenant.        |
| `cases`        | `tines.cases`        | [Cases](cases.md)                     | Cases and their sub-areas, from the current v2 API.     |
| `change_requests` | `tines.change_requests` | [Change requests](change_requests.md) | Listing and reading change requests across stories. The operations on one story are in `stories.change_control`. |
| `credentials`  | `tines.credentials`  | [Credentials](credentials.md)         | The secrets that actions use.                           |
| `dashboards`   | `tines.dashboards`   | [Dashboards](dashboards.md)           | Listing, exporting, importing and deleting dashboards.  |
| `folders`      | `tines.folders`      | [Folders](folders.md)                 | Folders that organize stories, credentials and resources. |
| `info`         | `tines.info`         | [Info](info.md)                       | Information about the tenant: its stack, web server and workers. |
| `records`      | `tines.records`      | [Records](records.md), [Records: record types](records_record_types.md), [Records: record views](records_record_views.md) | Records, their types and their views. |
| `reporting`    | `tines.reporting`    | [Reporting](reporting.md)             | Flow usage by team and the time saved.                  |
| `resources`    | `tines.resources`    | [Resources](resources.md)             | Named values such as text, JSON and files.              |
| `skills`       | `tines.skills`       | [Skills](skills.md)                   | Skills that AI agents can load, found by name and team. |
| `stories`      | `tines.stories`      | [Stories](stories.md), [Stories: actions](stories_actions.md) | The automations built in Tines, with their sub-areas.   |
| `tags`         | `tines.tags`         | [Tags](tags.md)                       | Tags that classify content.                             |
| `teams`        | `tines.teams`        | [Teams](teams.md)                     | Teams and, as a sub-area, their members.                |
| `workbench`    | `tines.workbench`    | [Workbench](workbench.md)             | Workbench and other AI conversations, read only.        |

## Sub-areas

A sub-area is an attribute of its module, for example `tines.stories.versions` and
`tines.cases.comments`. Each is a class of its own in the package of the module. It is documented on
the page of its module, except for the actions of a story.

| Module    | Sub-areas                                                                                          |
| --------- | -------------------------------------------------------------------------------------------------- |
| `admin`   | `users`, `roles`, `templates`, `tunnels`, `ip_access_control_rules`, `action_egress_control_rules`, `sync_destinations`, `jobs`, `license`, `smtp`, `custom_certificate_authority`, each on its own page, listed on [the admin page](admin.md). |
| `ai`      | `providers` and `usage`.                                                                           |
| `cases`   | `activities`, `assignees`, `comments`, `notes`, `tasks`, `field_values`, `metadata`, `files`, `blocks`, `linked_cases`, `records`, `subscribers`, `actions`, `fields`, `statuses`, `templates` and `webhooks`. |
| `records` | `artifacts`, `fields`, `record_types` and `record_views`. The last two are on pages of their own.  |
| `stories` | `actions`, `events`, `links`, `notes`, `drafts`, `owners`, `recipients`, `runs`, `groups`, `versions` and `change_control`. |
| `teams`   | `members`.                                                                                         |
