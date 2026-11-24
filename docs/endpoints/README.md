# Endpoints

One page for each module that tapi offers. A module is a Tines API area. It is available as an
attribute of `Tines`, such as `tines.tags`, and its class can also be used on its own with a
`Transport`. Every method returns a [`Response`](../responses.md).

A page lists the methods of a class with their HTTP route, then breaks each one down: its arguments
and the response codes. In an argument table, Required says whether the argument must be passed (an
optional one is not sent unless it is given), and Values lists what the argument accepts. A module
that has sub-endpoints has a folder with a page for the module and one for each sub-endpoint, as
`admin/` does.

## Modules

| Module         | Attribute            | Page                                  | Covers                                                  |
| -------------- | -------------------- | ------------------------------------- | ------------------------------------------------------- |
| `admin`        | `tines.admin`        | [Admin](admin/admin.md)               | Administration of the tenant: users, roles, templates, tunnels, IP access control rules, action egress control rules, sync destinations, jobs, the license, SMTP, and the custom certificate authority. |
| `ai`           | `tines.ai`           | [AI](ai/ai.md)                        | AI providers and AI usage.                              |
| `apps`         | `tines.apps`         | [Apps](apps.md)                       | Apps built inside Tines.                                |
| `audit_logs`   | `tines.audit_logs`   | [Audit logs](audit_logs.md)           | The audit log of the changes made in the tenant.        |
| `cases`        | `tines.cases`        | [Cases](cases/cases.md)               | Cases and their sub-areas, from the current v2 API.     |
| `change_requests` | `tines.change_requests` | [Change requests](change_requests.md) | Listing and reading change requests across stories. The operations on one story are in `stories.change_control`. |
| `credentials`  | `tines.credentials`  | [Credentials](credentials.md)         | The secrets that actions use.                           |
| `dashboards`   | `tines.dashboards`   | [Dashboards](dashboards.md)           | Listing, exporting, importing and deleting dashboards.  |
| `folders`      | `tines.folders`      | [Folders](folders.md)                 | Folders that organize stories, credentials and resources. |
| `info`         | `tines.info`         | [Info](info.md)                       | Information about the tenant: its stack, web server and workers. |
| `records`      | `tines.records`      | [Records](records/records.md)         | Records, their types, their views, their fields and their artifacts. |
| `reporting`    | `tines.reporting`    | [Reporting](reporting.md)             | Flow usage by team and the time saved.                  |
| `resources`    | `tines.resources`    | [Resources](resources.md)             | Named values such as text, JSON and files.              |
| `skills`       | `tines.skills`       | [Skills](skills.md)                   | Skills that AI agents can load, found by name and team. |
| `stories`      | `tines.stories`      | [Stories](stories/stories.md)         | The automations built in Tines, with their sub-areas.   |
| `tags`         | `tines.tags`         | [Tags](tags.md)                       | Tags that classify content.                             |
| `teams`        | `tines.teams`        | [Teams](teams/teams.md)               | Teams and, as a sub-area, their members.                |
| `workbench`    | `tines.workbench`    | [Workbench](workbench.md)             | Workbench and other AI conversations, read only.        |

## Sub-areas

A sub-area is an attribute of its module, for example `tines.stories.versions` and
`tines.cases.comments`. Each is a class of its own in the package of the module, and has its own page
in the folder of its module. The page of the module lists them.

| Module    | Sub-areas                                                                                          |
| --------- | -------------------------------------------------------------------------------------------------- |
| `admin`   | `users`, `roles`, `templates`, `tunnels`, `ip_access_control_rules`, `action_egress_control_rules`, `sync_destinations`, `jobs`, `license`, `smtp` and `custom_certificate_authority`. |
| `ai`      | `providers` and `usage`.                                                                           |
| `cases`   | `actions`, `activities`, `assignees`, `blocks`, `comments`, `field_values`, `fields`, `files`, `linked_cases`, `metadata`, `notes`, `records`, `statuses`, `subscribers`, `tasks`, `templates` and `webhooks`. |
| `records` | `artifacts`, `fields`, `record_types` and `record_views`.                                          |
| `stories` | `actions`, `events`, `links`, `notes`, `drafts`, `owners`, `recipients`, `runs`, `groups`, `versions` and `change_control`. |
| `teams`   | `members`.                                                                                         |
