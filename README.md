# About Tapi
A simple Python wrapper for the Tines API.

## ⚙️Installation

```bash
pip install tapi
```

## 🔄 Usage

### ✨ Using the main `TenantAPI` class
This class provides access to all endpoints offered by the Tines API.

```python
from tapi import TenantAPI

def main():
    tenant = TenantAPI("<DOMAIN>", "<API_KEY>")
    teams = tenant.teams.list()
    cases = tenant.cases.list()
    stories = tenant.stories.list()

if __name__ == "__main__":
    main()
```

### 🔧 Using specific endpoint classes
While the main `TenantAPI` class is convenient, using specific endpoint classes may be preferable in certain scenarios. Each class requires `DOMAIN` and `API_KEY` to be passed explicitly.

```python
from tapi import CasesAPI, TeamsAPI, StoriesAPI

def main():
    DOMAIN = "MY_COOL_DOMAIN"
    API_KEY = "DO_NOT_PUT_THIS_ON_GITHUB"

    cases_api = CasesAPI(DOMAIN, API_KEY)
    teams_api = TeamsAPI(DOMAIN, API_KEY)
    stories_api = StoriesAPI(DOMAIN, API_KEY)

if __name__ == "__main__":
    main()
```

### Disabling SSL verification
There are cases when SSL verification can pose a problem in making a request to Tines REST API, fortunately
there is an easy way of disabling SSL verification in Tapi. Here is how:

```python
from tapi.utils.http import disable_ssl_verification

disable_ssl_verification()
```

### Star History

<div align="center">

<a href="https://www.star-history.com/#1Doomdie1/Tapi&type=timeline&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=1Doomdie1/Tapi&type=timeline&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=1Doomdie1/Tapi&type=timeline&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=1Doomdie1/Tapi&type=timeline&legend=top-left" />
 </picture>
</a>

<a href="https://github.com/1Doomdie1/tapi/stargazers">
  <img src="https://img.shields.io/github/stars/1Doomdie1/tapi?style=social" alt="GitHub Repo stars" />
</a>
<a href="https://pepy.tech/projects/tapi">
  <img src="https://static.pepy.tech/personalized-badge/tapi?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads" alt="Downloads" />
</a>

</div>



## Endpoint Classes

<details>
<summary>TenantAPI</summary>
This class is designed to be used as a "parent" class from which all other endpoints in tines can be accessed.

### Methods

| **Method**          | **Description**                                                            |
|---------------------|----------------------------------------------------------------------------|
| `info`              | Retries information about the tenant.                                      |
| `web_statistics`    | Retrieve operational information about your web server. (Self Hosted Only) |
| `trigger_webhook`   | Trigger a webhook from the tenant or external tenants.                     |
| `worker_statistics` | Retrieve essential information about worker statistics. (Self Hosted Only) |

### Subclasses

| **Path**                | **Class**        | **Description**                        |
|-------------------------|------------------|----------------------------------------|
| `TenantAPI.cases`       | `CasesAPI`       | Manage cases.                          |
| `TenantAPI.teams`       | `TeamsAPI`       | Manage teams.                          |
| `TenantAPI.admin`       | `AdminAPI`       | Manage tenant through admin endpoints. |
| `TenantAPI.events`      | `EventsAPI`      | Manage tenant-wide action events.      |
| `TenantAPI.stories`     | `StoriesAPI`     | Manage workflows.                      |
| `TenantAPI.folders`     | `FoldersAPI`     | Manage folders.                        |
| `TenantAPI.records`     | `RecordsAPI`     | Manage records.                        |
| `TenantAPI.resources`   | `ResourcesAPI`   | Manage resources.                      |
| `TenantAPI.reporting`   | `ReportingAPI`   | Pull action performance & time saved   |
| `TenantAPI.audit_logs`  | `AuditLogsAPI`   | Pull tenant logs.                      |
| `TenantAPI.credentials` | `CredentialsAPI` | Manage tenant credentials.             |


### Usage:
```python
from json import dumps
from tapi import TenantAPI

def main():
    DOMAIN  = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"
    
    tenant = TenantAPI(DOMAIN, API_KEY)
    
    tenant_info = tenant.info()
    
    print(dumps(tenant_info, indent = 4))
```
```json5
{
    "body": {
        "stack": {...}
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>StoriesAPI</summary>
Manage tines workflows.

### Methods

| **Method**     | **Description**                          |
|----------------|------------------------------------------|
| `create`       | Create story.                            |
| `get`          | Get story details.                       |
| `update`       | Update story details.                    |
| `list`         | List all stories in the tenant or team.  |
| `delete`       | Delete story.                            |
| `batch_delete` | Delete multiple stories.                 |
| `export`       | Export story.                            |
| `import_`      | Import story.                            |
| `disable`      | Update the disabled state of a story.    |

### Subclasses

| **Path**                           | **Class**          | **Description**              |
|------------------------------------|--------------------|------------------------------|
| `TenantAPI.stories.runs`           | `RunsAPI`          | Manage case runs.            |
| `TenantAPI.stories.notes`          | `NotesAPI`         | Manage case notes.           |
| `TenantAPI.stories.groups`         | `GroupsAPI`        | Pull action groups logs.     |
| `TenantAPI.stories.drafts`         | `DraftsAPI`        | Manage story drafts.         |
| `TenantAPI.stories.actions`        | `ActionsAPI`       | Manage case actions.         |
| `TenantAPI.stories.versions`       | `VersionsAPI`      | Manage case versions.        |
| `TenantAPI.stories.change_request` | `ChangeRequestAPI` | Manage case change requests. |

### Usage:

```python
from json import dumps
from tapi import StoriesAPI

def main():
    DOMAIN  = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"
    
    stories_api = StoriesAPI(DOMAIN, API_KEY)
    
    stories = stories_api.list()
    
    print(dumps(stories, indent = 4))
```
```json5
{
    "body": {
        "stories": [
            {
                "name": "Testing",
                "user_id": 1234,
                "description": null,
                "keep_events_for": 604800,
                "disabled": false,
                "priority": false
                //...[snip]...//
            }
        //...[snip]...//
        ]
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>RunsAPI</summary>
Manage workflows runs.

### Methods

| **Method** | **Description**                            |
|------------|--------------------------------------------|
| `events`   | Retrieve a list of events for a story run. |
| `list`     | Retrieve a list of story runs.             |

### Subclasses
- **None**

### Usage

```python
from json import dumps
from tapi import RunsAPI

def main():
    DOMAIN  = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"
    
    story_run_api = RunsAPI(DOMAIN, API_KEY)
    
    runs = story_run_api.list(
        story_id = 1234
    )
    
    print(dumps(runs, indent = 4))
```
```json5
{
    "body": {
        "story_runs": [
            {
                "guid": "1b3087a2-1589-4fb8-8259-d74d38fccfb2",
                "duration": 0,
                "story_id": 1234,
                "start_time": "2025-01-27T21:13:20Z",
                "end_time": "2025-01-27T21:13:20Z",
                "action_count": 1,
                "event_count": 1,
                "story_mode": "LIVE"
            },
            //...[snip]...//
        ]
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>VersionsAPI</summary>
Manage stories versions.

### Methods

| **Method** | **Description**                    |
|------------|------------------------------------|
| `create`   | Create a story version.            |
| `get`      | Retrieve a story version.          |
| `update`   | Update a story version.            |
| `list`     | Retrieve a list of story versions. |
| `delete`   | Delete a story version.            |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import VersionsAPI

def main():
    DOMAIN  = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"
    
    story_version_api = VersionsAPI(DOMAIN, API_KEY)
    
    versions = story_version_api.list(
        story_id = 1234
    )
    
    print(dumps(versions, indent = 4))
```
```json5
{
    "body": {
        "story_versions": [
            {
                "id": 69670,
                "name": "",
                "description": "",
                "timestamp": "2025-01-27T21:20:00Z"
            },
            //...[snip]...//
        ],
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>TeamsAPI</summary>
Manage tines teams.

### Methods

| **Method** | **Description**                       |
|------------|---------------------------------------|
| `create`   | Create a team in Tines.               |
| `get`      | Retrieve a single team or case group. |
| `update`   | Update a team.                        |
| `list`     | Retrieve a list of teams.             |
| `delete`   | Delete a team or case group.          |

### Subclasses

| **Path**                  | **Class**          | **Description**      |
|---------------------------|--------------------|----------------------|
| `TenantAPI.teams.members` | `MembersAPI`       | Manage team members. |

### Usage:

```python
from json import dumps
from tapi import TeamsAPI

def main():
    DOMAIN  = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"
    
    teams_api = TeamsAPI(DOMAIN, API_KEY)
    
    teams = teams_api.list()
    
    print(dumps(teams, indent = 4))
```
```json5
{
    "body": {
        "teams": [
            {
                "id": 12345,
                "name": "My Team",
                "groups": []
            },
            //...[snip]...//
        ],
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>MembersAPI</summary>
Manage teams members.

### Methods

| **Method**      | **Description**                     |
|-----------------|-------------------------------------|
| `list`          | Retrieve a list of team members.    |
| `remove`        | Remove a user from a team.          |
| `invite`        | Invite a user to join a team.       |
| `resend_invite` | Resend a team invitation to a user. |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import MembersAPI

def main():
    DOMAIN  = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"
    
    members_api = MembersAPI(DOMAIN, API_KEY)
    
    members = members_api.list(team_id = 1234)
    
    print(dumps(members, indent = 4))
```
```json5
{
    "body": {
        "members": [
            {
                "id": 1234,
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@doe.io",
                "is_admin": true,
                "created_at": "2025-01-27T17:33:33Z",
                "last_seen": "2025-02-03T18:42:23Z",
                "invitation_accepted": true,
                "role": "TEAM_ADMIN"
            },
            //...[snip]...//
        ],
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>CasesAPI</summary>
Manage tines cases.

### Methods

| **Method** | **Description**           |
|------------|---------------------------|
| `create`   | Create a case.            |
| `get`      | Retrieve a single case.   |
| `download` | Retrieve a PDF of a case. |
| `update`   | Update a case.            |
| `list`     | Retrieve a list of cases. |
| `delete`   | Delete a case.            |

### Subclasses

| **Path**                       | **Class**            | **Description**          |
|--------------------------------|----------------------|--------------------------|
| `TenantAPI.cases.files`        | `CaseFilesAPI`       | Manage case files.       |
| `TenantAPI.cases.notes`        | `CaseNotesAPI`       | Manage case notes.       |
| `TenantAPI.cases.tasks`        | `CaseTasksAPI`       | Manage case tasks.       |
| `TenantAPI.cases.inputs`       | `CaseInputsAPI`      | Manage case inputs.      |
| `TenantAPI.cases.fields`       | `CaseFieldsAPI`      | Manage case fields.      |
| `TenantAPI.cases.blocks`       | `CaseBlocksAPI`      | Manage case blocks.      |
| `TenantAPI.cases.linked_cases` | `LinkedCasesAPI`     | Manage linked cases.     |
| `TenantAPI.cases.actions`      | `CaseActionsAPI`     | Manage case actions.     |
| `TenantAPI.cases.records`      | `CaseRecordsAPI`     | Manage case records.     |
| `TenantAPI.cases.comments`     | `CaseCommentsAPI`    | Manage case comments.    |
| `TenantAPI.cases.metadata`     | `CaseMetadataAPI`    | Manage case metadata.    |
| `TenantAPI.cases.assignees`    | `CaseAssigneesAPI`   | Manage case assignees.   |
| `TenantAPI.cases.activities`   | `CaseActivitiesAPI`  | Manage case activities.  |
| `TenantAPI.cases.subscribers`  | `CaseSubscribersAPI` | Manage case subscribers. |

### Usage:

```python
from json import dumps
from tapi import CasesAPI

def main():
    DOMAIN  = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"
    
    case_api = CasesAPI(DOMAIN, API_KEY)
    
    cases = case_api.list()
    
    print(dumps(cases, indent = 4))
```
```json5
{
    "body": {
        "cases": [
            {
                "case_id": 1,
                "name": "My Case",
                "description": "",
                "status": "OPEN",
                "sub_status": {
                  "id": 38482,
                  "name": "To do"
                },
                //...[snip]...//
            },
        ],
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>CaseActionsAPI</summary>
Manage case actions.

### Methods

| **Method**     | **Description**                                      |
|----------------|------------------------------------------------------|
| `create`       | Create a new case action on a specified case.        |
| `get`          | Retrieve a specific case action.                     |
| `update`       | Update an action.                                    |
| `list`         | Retrieve a list of case actions for a specific case. |
| `delete`       | Delete an existing case action.                      |
| `batch_update` | Update the actions on a case                         |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import CaseActionsAPI

def main():
    DOMAIN  = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"
    
    case_actions_api = CaseActionsAPI(DOMAIN, API_KEY)
    
    actions = case_actions_api.list(case_id=1234)
    
    print(dumps(actions, indent = 4))
```
```json5
{
    "body": {
        "case_id": 1234,
        "actions": [
            {
                "id": 29907,
                "url": "https://example.tines.com",
                "label": "Complete request",
                "story_name": null,
                "page_emoji": null,
                "story_emoji": null,
                "action_type": "page",
                "action_text": "Open",
                "created_at": "2025-02-03T18:41:59Z",
                "updated_at": "2025-02-03T18:41:59Z"
            },
            //...[snip]...//
        ],
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>CaseActivitiesAPI</summary>
Manage case activities.

### Methods

| **Method** | **Description**                                |
|------------|------------------------------------------------|
| `get`      | Retrieve a single case activity.               |
| `list`     | Retrieve a list of case activities for a case. |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import CaseActivitiesAPI

def main():
    DOMAIN  = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"
    
    case_activities_api = CaseActivitiesAPI(DOMAIN, API_KEY)
    
    activities = case_activities_api.list(case_id=1234)
    
    print(dumps(activities, indent = 4))
```
```json5
{
    "body": {
        "case_id": 26,
        "activities": [
            {
                "id": 591299,
                "activity_type": "COMMENTED",
                "value": "Some random comment",
                "created_at": "2025-01-29T21:39:27Z",
                "user": {
                    "user_id": "6868",
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "john@doe.io",
                    "avatar_url": "",
                    "is_service_account": false
                },
                "reactions": []
            },
            //...[snip]...//
        ],
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>CaseAssigneesAPI</summary>
Manage case assignees.

### Methods

| **Method** | **Description**                         |
|------------|-----------------------------------------|
| `list`     | Retrieve a list of assignees of a case. |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import CaseAssigneesAPI

def main():
    DOMAIN  = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"
    
    case_assignees_api = CaseAssigneesAPI(DOMAIN, API_KEY)
    
    assignees = case_assignees_api.list(case_id=1234)
    
    print(dumps(assignees, indent = 4))
```
```json5
{
    "body": {
        "case_id": 1234,
        "assignees": [...],
        //...[snip]...//
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>CaseInputsAPI</summary>
Manage case inputs.

### Methods

| **Method** | **Description**                 |
|------------|---------------------------------|
| `create`   | Create a case input on a team.  |
| `get`      | Returns a case input.           |
| `list`     | Returns a list of case inputs.  |

### Subclasses

| **Path**                 | **Class**             | **Description**     |
|--------------------------|-----------------------|---------------------|
| `TenantAPI.cases.inputs` | `CaseInputsFieldsAPI` | Manage Case Inputs. |

### Usage:

```python
from json import dumps
from tapi import CaseInputsAPI

def main():
    DOMAIN  = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"
    
    case_inputs_api = CaseInputsAPI(DOMAIN, API_KEY)
    
    inputs = case_inputs_api.list()
    
    print(dumps(inputs, indent = 4))
```
```json5
{
    "body": {
        "case_inputs": [
            {
                "id": 412,
                "name": "Create Case Input Unit Test",
                "key": "create_case_input_unit_test",
                "input_type": "number",
                "validation_type": "none",
                "validation_options": {},
                "team": {
                    "id": 10445,
                    "name": "Collaboration Space"
                },
                "created_at": "2025-01-29T18:07:07Z",
                "updated_at": "2025-01-29T18:07:07Z"
            }
        ],
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>CaseInputsFieldsAPI</summary>
Manage case input fields.

### Methods

| **Method** | **Description**                            |
|------------|--------------------------------------------|
| `list`     | Retrieve a list of fields of a case input. |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import CaseInputsFieldsAPI

def main():
    DOMAIN  = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"
    
    case_input_fields_api = CaseInputsFieldsAPI(DOMAIN, API_KEY)
    
    input_fields = case_input_fields_api.list(case_input_id=1234)
    
    print(dumps(input_fields, indent = 4))
```
```json5
{
    "body": {
        "fields": [
            {
                "id": 65221,
                "value": "2",
                "case": {
                    "id": 26
                },
                "case_input": {
                    "id": 412,
                    "name": "Input Name"
                }
            }
        ],
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>CaseCommentsAPI</summary>
Manage case comments.

### Methods

| **Method** | **Description**                         |
|------------|-----------------------------------------|
| `create`   | Add a comment to a case.                |
| `get`      | Retrieve a single comment for a case.   |
| `update`   | Update an existing case comment.        |
| `list`     | Retrieve a list of comments for a case. |
| `delete`   | Delete a comment from a case.           |

### Subclasses

| **Path**                             | **Class**                  | **Description**                 |
|--------------------------------------|----------------------------|---------------------------------|
| `TenantAPI.cases.comments.reactions` | `CaseCommentsReactionsAPI` | Manage case comments reactions. |

### Usage:

```python
from json import dumps
from tapi import CaseCommentsAPI

def main():
    DOMAIN  = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"
    
    case_comments_api = CaseCommentsAPI(DOMAIN, API_KEY)
    
    comments = case_comments_api.list(case_id=1234)
    
    print(dumps(comments, indent = 4))
```
```json5
{
    "body": {
        "case_id": 1234,
        "comments": [
            {
                "id": 591299,
                "activity_type": "COMMENTED",
                "value": "Some Comment",
                "created_at": "2025-01-29T21:39:27Z",
                "user": {
                    "user_id": "6868",
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "john@doe.io",
                    "avatar_url": "",
                    "is_service_account": false
                },
                "reactions": []
            }
            //...[snip]...//
        ],
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>CaseCommentsReactionsAPI</summary>
Manage comments reactions.

### Methods

| **Method** | **Description**                   |
|------------|-----------------------------------|
| `add`      | Add a reaction to a comment.      |
| `remove`   | Remove a reaction from a comment. |


### Subclasses
- **None**

### Usage:

```python
from json             import dumps
from tapi.utils.types import ReactionType
from tapi             import CaseCommentsReactionsAPI


def main():
    DOMAIN = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"

    comments_reactions_api = CaseCommentsReactionsAPI(DOMAIN, API_KEY)

    reaction = comments_reactions_api.add(
        case_id=1234,
        comment_id=5678,
        value=ReactionType.PLUS_ONE
    )

    print(dumps(reaction, indent=4))
```
```json5
{
    "body": {
        "reactions": [
            {
                "emoji": ":+1:",
                "reactants": [
                    {
                        "user_id": 6866,
                        "user_name": "John Doe",
                        "reacted_at": "2025-02-04T03:40:14+00:00"
                    }
                ]
            }
        ],
    //...[snip]...//
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>CaseFieldsAPI</summary>
Manage case fields.

### Methods

| **Method** | **Description**                       |
|------------|---------------------------------------|
| `create`   | Add a field to a case.                |
| `get`      | Retrieve a single field for a case.   |
| `update`   | Update an existing case field.        |
| `list`     | Retrieve a list of fields for a case. |
| `delete`   | Delete a field from a case.           |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import CaseFieldsAPI

def main():
    DOMAIN  = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"
    
    case_fields_api = CaseFieldsAPI(DOMAIN, API_KEY)
    
    case_fields = case_fields_api.list(case_id=1234)
    
    print(dumps(case_fields, indent = 4))
```
```json5
{
    "body": {
        "case_id": 1234,
        "fields": [
            {
                "id": 65221,
                "value": "2",
                "case_input": {
                    "id": 412,
                    "key": "input_name",
                    "name": "Input Name"
                }
            },
            //...[snip]...//
        ],
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>CaseFilesAPI</summary>
Manage case files.

### Methods

| **Method** | **Description**                                                         |
|------------|-------------------------------------------------------------------------|
| `create`   | Attach a file to a case.                                                |
| `get`      | Retrieve details for a case file.                                       |
| `list`     | Retrieve a list of files for a case.                                    |
| `delete`   | Delete a file from a case.                                              |
| `download` | Retrieve a case file attachment.                                        |
| `info`     | Retrieve metadata for a case file attachment without the file contents. |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import CaseFilesAPI

def main():
    DOMAIN  = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"
    
    case_files_api = CaseFilesAPI(DOMAIN, API_KEY)
    
    files = case_files_api.list(case_id=1234)
    
    print(dumps(files, indent = 4))
```
```json5
{
    "body": {
        "files": [
            {
                "id": 592294,
                "activity_type": "FILE_ATTACHED_AND_COMMENTED",
                "value": "Testing comment",
                "file": {
                    "filename": "My File",
                    "url": "https://my-cool-domain-1234.tines.com/api/v2/cases/1234/files/592294/download"
                },
                "created_at": "2025-02-01T22:14:36Z",
                "user": {
                    "user_id": "6868",
                    "first_name": "john",
                    "last_name": "doe",
                    "email": "john@doe.io",
                    "avatar_url": "",
                    "is_service_account": false
                },
                "reactions": []
            },
            //...[snip]...//
        ],
        //...[snip]...//
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>LinkedCasesAPI</summary>
Manage linked cases.

### Methods

| **Method**     | **Description**                                        |
|----------------|--------------------------------------------------------|
| `create`       | Link two cases together by creating a new case link.   |
| `list`         | Retrieve the linked cases for a case.                  |
| `delete`       | Unlink two cases by deleting a case link.              |
| `batch_create` | Batch link cases together by creating a new case link. |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import LinkedCasesAPI

def main():
    DOMAIN  = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"
    
    link_case_api = LinkedCasesAPI(DOMAIN, API_KEY)
    
    linked_cases = link_case_api.list(case_id=1234)
    
    print(dumps(linked_cases, indent = 4))
```
```json5
{
    "body": {
        "case_id": 1234,
        "name": "Action Testing Case",
        "linked_cases": [
            {
                "case_id": 58,
                "name": "Case 2 link"
            }
        ],
        //...[snip]...//
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>CaseMetadataAPI</summary>
Manage case metadata.

### Methods

| **Method**     | **Description**                                                 |
|----------------|-----------------------------------------------------------------|
| `create`       | Create new metadata key-value pairs for a specified case.       |
| `get`          | Retrieve a specific key-value pair from the metadata of a case. |
| `update`       | Update metadata key-value pairs for a case.                     |
| `list`         | Retrieve the metadata from a case.                              |
| `delete`       | Delete existing metadata key-value pairs in a case.             |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import CaseMetadataAPI

def main():
    DOMAIN  = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"
    
    case_metadata_api = CaseMetadataAPI(DOMAIN, API_KEY)
    
    metadata = case_metadata_api.list(case_id=1234)
    
    print(dumps(metadata, indent = 4))
```
```json5
{
    "body": {
        "case_id": 1234,
        "metadata": {
            "name": "John Doe",
        }
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>CaseNotesAPI</summary>
Manage case notes.

### Methods

| **Method**     | **Description**                      |
|----------------|--------------------------------------|
| `create`       | Add a note to a case.                |
| `get`          | Retrieve a single note for a case.   |
| `update`       | Update an existing case note.        |
| `list`         | Retrieve a list of notes for a case. |
| `delete`       | Delete a note from a case.           |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import CaseNotesAPI

def main():
    DOMAIN  = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"
    
    case_notes_api = CaseNotesAPI(DOMAIN, API_KEY)
    
    notes = case_notes_api.list(case_id=1234)
    
    print(dumps(notes, indent = 4))
```
```json5
{
    "body": {
        "case_id": 1234,
        "notes": [
            {
                "id": 87,
                "title": "My Note",
                "content": "This is a very helpful note, as you can see",
                "color": "blue",
                "author": {
                    "user_id": "6868",
                    "first_name": "john",
                    "last_name": "doe",
                    "email": "john@doe.io",
                    "avatar_url": "",
                    "is_service_account": false
                },
                "created_at": "2025-02-02T20:58:53Z",
                "updated_at": "2025-02-02T20:58:53Z"
            },
            //...[snip]...//
        ],
        //...[snip]...//
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>CaseRecordsAPI</summary>
Manage case records.

### Methods

| **Method**     | **Description**                                |
|----------------|------------------------------------------------|
| `create`       | Add an existing record to a case.              |
| `get`          | Retrieve a single record attached to a case.   |
| `list`         | Retrieve a list of records attached to a case. |
| `delete`       | Remove a record from a case.                   |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import CaseRecordsAPI

def main():
    DOMAIN  = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"
    
    case_records_api = CaseRecordsAPI(DOMAIN, API_KEY)
    
    records = case_records_api.list(case_id=1234)
    
    print(dumps(records, indent = 4))
```
```json5
{
    "body": {
        "case_id": 1234,
        "records": [
            {
                "record_type_id": 1419,
                "record_type_name": "My Record Type",
                "record_type_record_results": [...]
            },
            //...[snip]...//
        ],
        //...[snip]...//
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>CaseSubscribersAPI</summary>
Manage case records.

### Methods

| **Method**     | **Description**                           |
|----------------|-------------------------------------------|
| `create`       | Subscribe to a case.                      |
| `list`         | Retrieve a list of subscribers of a case. |
| `delete`       | Unsubscribe from a case.                  |
| `batch_create` | Batch subscribe users to a case.          |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import CaseSubscribersAPI

def main():
    DOMAIN  = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"
    
    case_subs_api = CaseSubscribersAPI(DOMAIN, API_KEY)
    
    subscribers = case_subs_api.list(case_id=1234)
    
    print(dumps(subscribers, indent = 4))
```
```json5
{
    "body": {
        "case_id": 1234,
        "subscribers": [
            {
                "user_id": "6866",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@doe.io",
                "avatar_url": "https://www.gravatar.com/avatar/aaaabbbbccccddddeeeeffffgggghhhh",
                "id": 2231
            }
        ],
        //...[snip]...//
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>CaseTasksAPI</summary>
Manage case tasks.

### Methods

| **Method**     | **Description**                               |
|----------------|-----------------------------------------------|
| `create`       | Create a task for a specific case.            |
| `get`          | Retrieve a single task from a specific case.  |
| `update`       | Update a task for a specific case.            |
| `list`         | Retrieve a list of tasks for a specific case. |
| `delete`       | Delete a task.                                |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import CaseTasksAPI

def main():
    DOMAIN  = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"
    
    case_tasks_api = CaseTasksAPI(DOMAIN, API_KEY)
    
    tasks = case_tasks_api.list(case_id=1234)
    
    print(dumps(tasks, indent = 4))
```
```json5
{
    "body": {
        "tasks": [...]
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>CaseBlocksAPI</summary>
Manage case blocks.

### Methods

| **Method**     | **Description**                       |
|----------------|---------------------------------------|
| `create`       | Add a block to a case.                |
| `get`          | Retrieve a single block for a case.   |
| `update`       | Update an existing block.             |
| `list`         | Retrieve a list of blocks for a case. |
| `delete`       | Delete a block from a case.           |

### Subclasses

| **Path**                          | **Class**              | **Description**              |
|-----------------------------------|------------------------|------------------------------|
| `TenantAPI.cases.blocks.elements` | `CaseBlockElementsAPI` | Manage case blocks elements. |

### Usage:

```python
from json import dumps
from tapi import CaseBlocksAPI

def main():
    DOMAIN  = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"
    
    case_blocks_api = CaseBlocksAPI(DOMAIN, API_KEY)
    
    blocks = case_blocks_api.list(case_id = 1234)
    
    print(dumps(blocks, indent = 4))
```
```json5
{
    "body": {
        "blocks": [...],
        //...[snip]...//
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>CaseBlockElementsAPI</summary>
Manage case block elements.

### Methods

| **Method**     | **Description**                       |
|----------------|---------------------------------------|
| `get`          | Retrieve a single block for a case.   |
| `update`       | Update an existing block.             |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import CaseBlockElementsAPI

def main():
    DOMAIN  = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"
    
    case_blocks_elements_api = CaseBlockElementsAPI(DOMAIN, API_KEY)
    
    element = case_blocks_elements_api.get(
        case_id    = 123,
        block_id   = 456,
        element_id = 789
    )
    
    print(dumps(element, indent = 4))
```
```json5
{
    "body": {
        "element_id": 789,
        "id": 456,
        "element_type": "note",
        //...[snip]...//
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>ActionsAPI</summary>
Manage actions.

### Methods

| **Method**     | **Description**                        |
|----------------|----------------------------------------|
| `create`       | Create action.                         |
| `get`          | Retrieve details of a specific action. |
| `update`       | Update an action.                      |
| `list`         | Retrieve a list of actions.            |
| `delete`       | Delete a specific action.              |
| `clear_memory` | Clears action memory.                  |

### Subclasses

| **Path**                           | **Class**         | **Description**       |
|------------------------------------|-------------------|-----------------------|
| `TenantAPI.stories.actions.logs`   | `ActionLogsAPI`   | Manage action logs.   |
| `TenantAPI.stories.actions.events` | `ActionEventsAPI` | Manage action events. |


### Usage:

```python
from json import dumps
from tapi import ActionsAPI

def main():
    DOMAIN  = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"
    
    actions_api = ActionsAPI(DOMAIN, API_KEY)
    
    actions = actions_api.list(story_id=1234)
    
    print(dumps(actions, indent = 4))
```
```json5
{
    "body": {
        "agents": [
            {
                "id": 111111,
                "type": "Agents::EventTransformationAgent",
                "user_id": 6866,
                "options": {
                    "mode": "message_only",
                    "loop": false,
                    "payload": {
                        "message": "This is an automatically generated message from Tines"
                    }
                },
                "name": "My Action"
                //...[snip]...//
            }
        ],
        //...[snip]...//
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>ActionEventsAPI</summary>
Manage action events.

### Methods

| **Method**     | **Description**                                          |
|----------------|----------------------------------------------------------|
| `list`         | Retrieve a list of events emitted by a specified action. |
| `delete`       | Delete all events emitted by a specific action.          |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import ActionEventsAPI

def main():
    DOMAIN  = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"
    
    action_events_api = ActionEventsAPI(DOMAIN, API_KEY)
    
    events = action_events_api.list(action_id=1234)
    
    print(dumps(events, indent = 4))
```
```json5
{
    "body": {
        "agents":[...],
        //...[snip]...//
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>ActionLogsAPI</summary>
Manage action logs.

### Methods

| **Method**     | **Description**                               |
|----------------|-----------------------------------------------|
| `list`         | List all logs emitted by a specific action.   |
| `delete`       | Delete all logs emitted by a specific action. |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import ActionLogsAPI

def main():
    DOMAIN  = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"
    
    action_logs_api = ActionLogsAPI(DOMAIN, API_KEY)
    
    logs = action_logs_api.list(action_id=1234)
    
    print(dumps(logs, indent = 4))
```
```json5
{
    "body": {
        "action_logs":[...],
        //...[snip]...//
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>NotesAPI</summary>
Manage story notes.

### Methods

| **Method** | **Description**                  |
|------------|----------------------------------|
| `create`   | Create a note on the storyboard. |
| `get`      | Retrieve a note.                 |
| `update`   | Update a note.                   |
| `list`     | List notes.                      |
| `delete`   | Delete a note.                   |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import NotesAPI

def main():
    DOMAIN  = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"
    
    notes_api = NotesAPI(DOMAIN, API_KEY)
    
    notes = notes_api.list()
    
    print(dumps(notes, indent = 4))
```
```json5
{
    "body": {
        "annotations":[...],
        //...[snip]...//
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>AuditLogsAPI</summary>
Pull tenant audit logs.

### Methods

| **Method** | **Description**                                              |
|------------|--------------------------------------------------------------|
| `list`     | Returns a list of audit logs gathered from the Tines tenant. |

### Subclasses
- **None**

### Usage:

```python
from json             import dumps
from tapi             import AuditLogsAPI
from tapi.utils.types import AuditLogType


def main():
    DOMAIN = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"

    audit_logs_api = AuditLogsAPI(DOMAIN, API_KEY)

    logs = audit_logs_api.list(
        operation_name=[
            AuditLogType.STORY_CREATION
        ]
    )

    print(dumps(logs, indent=4))
```
```json5
{
    "body": {
        "audit_logs":[...],
        //...[snip]...//
    },
    "headers": {...},
    "status_code": ...
}
```

</details>


<details>
<summary>CredentialsAPI</summary>
Manage tenant credentials

### Methods

| **Method**             | **Description**                    |
|------------------------|------------------------------------|
| `get`                  | Retrieve a credential.             |
| `update`               | Update a credential.               |
| `list`                 | Retrieve a list of credentials.    |
| `delete`               | Delete a credential.               |
| `create_aws`           | Create a AWS credential.           |
| `create_http_request`  | Create a HTTP Request credential.  |
| `create_jwt`           | Create a JWT credential.           |
| `create_mtls`          | Create a MTLS credential.          |
| `create_multi_request` | Create a Multi Request credential. |
| `create_oauth`         | Create a OAUTH credential.         |
| `create_text`          | Create a TEXT credential.          |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import CredentialsAPI


def main():
    DOMAIN = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"

    credentials_api = CredentialsAPI(DOMAIN, API_KEY)

    creds = credentials_api.list()

    print(dumps(creds, indent=4))
```
```json5
{
    "body": {
        "user_credentials":[...],
        //...[snip]...//
    },
    "headers": {...},
    "status_code": ...
}
```

</details>


<details>
<summary>EventsAPI</summary>
Manage tenant-wide action events

### Methods

| **Method** | **Description**            |
|------------|----------------------------|
| `get`      | Retrieve an event.         |
| `list`     | Retrieve a list of events. |
| `re_emit`  | Re‑emit an event.          |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import EventsAPI


def main():
    DOMAIN = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"

    events_api = EventsAPI(DOMAIN, API_KEY)

    events = events_api.list()

    print(dumps(events, indent=4))
```
```json5
{
    "body": {
        "events":[...],
        //...[snip]...//
    },
    "headers": {...},
    "status_code": ...
}
```

</details>


<details>
<summary>FoldersAPI</summary>
Manage folders

### Methods

| **Method** | **Description**             |
|------------|-----------------------------|
| `create`   | Create a folder.            |
| `get`      | Retrieve a single folder.   |
| `udpate`   | Update a folder.            |
| `list`     | Retrieve a list of folders. |
| `delete`   | Delete a folder.            |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import FoldersAPI


def main():
    DOMAIN = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"

    folders_api = FoldersAPI(DOMAIN, API_KEY)

    folders = folders_api.list()

    print(dumps(folders, indent=4))
```
```json5
{
    "body": {
        "folders":[...],
        //...[snip]...//
    },
    "headers": {...},
    "status_code": ...
}
```

</details>


<details>
<summary>ResourcesAPI</summary>
Manage resources

### Methods

| **Method**        | **Description**                                                                |
|-------------------|--------------------------------------------------------------------------------|
| `create`          | Create a resource (text or json).                                              |
| `get`             | Retrieve a resource.                                                           |
| `udpate`          | Update a resource.                                                             |
| `list`            | Retrieve a list of resources.                                                  |
| `delete`          | Delete a resource.                                                             |
| `remove_element`  | Remove a top level element from an array or key from an object in a resource.  |
| `append_element`  | Append a string or an array to a resource.                                     |
| `replace_element` | Replace a top level element from an array or key from an object in a resource. |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import ResourcesAPI


def main():
    DOMAIN = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"

    resources_api = ResourcesAPI(DOMAIN, API_KEY)

    resources = resources_api.list()

    print(dumps(resources, indent=4))
```
```json5
{
    "body": {
        "global_resources":[...],
        //...[snip]...//
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>RecordsAPI</summary>
Manage records.

### Methods

| **Method**     | **Description**             |
|----------------|-----------------------------|
| `create`       | Create record.              |
| `get`          | Retrieve a single record.   |
| `update`       | Updates a single record.    |
| `list`         | Retrieve a list of records. |
| `delete`       | Delete a record.            |


### Subclasses

| **Path**                      | **Class**            | **Description**           |
|-------------------------------|----------------------|---------------------------|
| `TenantAPI.records.types`     | `RecordTypesAPI`     | Manage record types.      |
| `TenantAPI.records.views`     | `RecordViewsAPI`     | Manage records views.     |
| `TenantAPI.records.artifacts` | `RecordArtifactsAPI` | Manage records artifacts. |


### Usage:

```python
from json import dumps
from tapi import RecordsAPI

def main():
    DOMAIN  = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"
    
    records_api = RecordsAPI(DOMAIN, API_KEY)
    
    records = records_api.list(record_type_id=1234)
    
    print(dumps(records, indent = 4))
```
```json5
{
    "body": {
        "record_results": [...],
        //...[snip]...//
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>RecordTypesAPI</summary>
Manage record types

### Methods

| **Method**        | **Description**                  |
|-------------------|----------------------------------|
| `create`          | Create a new record type.        |
| `get`             | Retrieve a single record type.   |
| `list`            | Retrieve a list of record types. |
| `delete`          | Delete a record type.            |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import RecordTypesAPI


def main():
    DOMAIN = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"

    record_types_api = RecordTypesAPI(DOMAIN, API_KEY)

    record_types = record_types_api.list(team_id=1234)

    print(dumps(record_types, indent=4))
```
```json5
{
    "body": {
        "record_types":[...],
        //...[snip]...//
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>RecordArtifactsAPI</summary>
Pull record artifacts.

### Methods

| **Method**        | **Description**                         |
|-------------------|-----------------------------------------|
| `get`             | Retrieve an individual record artifact. |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import RecordArtifactsAPI


def main():
    DOMAIN = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"

    record_artifacts_api = RecordArtifactsAPI(DOMAIN, API_KEY)

    record_artifacts = record_artifacts_api.get(record_id = 1234, artifact_id = 5678)

    print(dumps(record_artifacts, indent=4))
```
```json5
{
    "body": {
        "id": 1,
        "value": "artifact value",
        "record_field": {
            "id": 1,
            "name": "record field name"
        },
        "created_at": "2024-02-16T15:37:39Z",
        "updated_at": "2024-02-16T15:37:39Z"
        //...[snip]...//
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>RecordViewsAPI</summary>
Manage record views

### Methods

| **Method** | **Description**                            |
|------------|--------------------------------------------|
| `list`     | Retrieve a paginated list of record views. |
| `delete`   | Delete a record view.                      |
| `export`   | Export a record view.                      |
| `import`   | Import a record view.                      |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import RecordViewsAPI


def main():
    DOMAIN = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"

    record_views_api = RecordViewsAPI(DOMAIN, API_KEY)

    record_views = record_views_api.list()

    print(dumps(record_views, indent=4))
```
```json5
{
    "body": {
        "record_views":[...]
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>ReportingAPI</summary>
Get action performance and time saved metrics 

### Methods

| **Method**   | **Description**                                               |
|------------- |---------------------------------------------------------------|
| `time_saved` | Returns timed and dated records of time saved by using Tines. |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import ReportingAPI


def main():
    DOMAIN = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"

    reporting_api = ReportingAPI(DOMAIN, API_KEY)

    time_saved = reporting_api.time_saved()

    print(dumps(time_saved, indent=4))
```
```json5
{
    "body": {
        "time_saved": [...]
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>AdminAPI</summary>
Manage tenant through admin endpoint

### Methods

| **Method**                         | **Description**                                                                          |
|------------------------------------|------------------------------------------------------------------------------------------|
| `set_custom_certificate_authority` | Set a custom certificate authority for use by all of your IMAP and HTTP Request actions. |
| `tunnel_health`                    | Retrieve the health status of tunnels.                                                   |

### Subclasses

| **Path**                                  | **Class**                     | **Description**                         |
|-------------------------------------------|-------------------------------|-----------------------------------------|
| `TenantAPI.admin.jobs`                    | `JobsAPI`                     | Manage tenant jobs. (Self Hosted Only)  |
| `TenantAPI.admin.users`                   | `UsersAPI`                    | Manage tenant-wide users.               |
| `TenantAPI.admin.templates`               | `TemplatesAPI`                | Manage templates.                       |
| `TenantAPI.admin.ip_access_control`       | `IpAccessControlAPI`          | Manage IP access control.               |
| `TenantAPI.admin.scim_user_group_mapping` | `SCIMUserGroupMappingAPI`     | Manage SCIM user group mappings.        |
| `TenantAPI.admin.story_sync_destinations` | `StorySyncDestinationsAPI`    | Manage story syncing.                   |
| `TenantAPI.admin.egress_rules`            | `ActionEgressControlRulesAPI` | Manage egress rules. (Self Hosted Only) |


### Usage:

```python
from json import dumps
from tapi import AdminAPI


def main():
    DOMAIN = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"

    admin_api = AdminAPI(DOMAIN, API_KEY)

    set_sert = admin_api.set_custom_certificate_authority(
        name        = "default",
        certificate = "<PEM encoded X.509 certificate>"
    )

    print(dumps(set_sert, indent=4))
```
```json5
{
    "body": "",
    "headers": {...},
    "status_code": 200
}
```

</details>

<details>
<summary>ActionEgressControlRulesAPI</summary>
Manage egress control rules (Self Hosted Only)

### Methods

| **Method** | **Description**                                  |
|------------|--------------------------------------------------|
| `create`   | Create a new Action egress control rule.         |
| `get`      | Get an Action egress control rule by ID.         |
| `update`   | Update an existing action egress control rule.   |
| `list`     | List Action egress control rules for the tenant. |
| `delete`   | Delete an existing Action egress control rule.   |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import ActionEgressControlRulesAPI


def main():
    DOMAIN = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"

    egress_con_api = ActionEgressControlRulesAPI(DOMAIN, API_KEY)

    controls = egress_con_api.list()

    print(dumps(controls, indent=4))
```
```json5
{
    "body": {
      "admin/action_egress_control_rules": [],
      //...[snip]...//
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>IpAccessControlAPI</summary>
Manage tenant IP access rules

### Methods

| **Method** | **Description**                              |
|------------|----------------------------------------------|
| `create`   | Create a new IP access control rule.         |
| `get`      | Get an IP access control rule by ID.         |
| `update`   | Update an existing IP access control rule.   |
| `list`     | List IP access control rules for the tenant. |
| `delete`   | Delete an existing IP access control rule.   |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import IpAccessControlAPI


def main():
    DOMAIN = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"

    ip_acc_con_api = IpAccessControlAPI(DOMAIN, API_KEY)

    ip_rules = ip_acc_con_api.list()

    print(dumps(ip_rules, indent=4))
```
```json5
{
    "body": {
      "admin/ip_access_control_rules": [],
      //...[snip]...//
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>JobsAPI</summary>
Manage tenant jobs. (Self Hosted Only)

### Methods

| **Method**     | **Description**                                             |
|----------------|-------------------------------------------------------------|
| `list`         | Retrieve a list of dead, in progress, queued or retry jobs. |
| `delete`       | Delete all dead, queued or retry jobs.                      |
| `delete_by_id` | Delete all dead, queued or retry jobs by action id.         |


### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import JobsAPI


def main():
    DOMAIN = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"

    jobs_api = JobsAPI(DOMAIN, API_KEY)

    jobs = jobs_api.list(job_type = "dead")

    print(dumps(jobs, indent=4))
```
```json5
{
    "body": {
      "admin/dead_jobs": [],
      //...[snip]...//
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>SCIMUserGroupMappingAPI</summary>
Manage SCIM user group mappings.

### Methods

| **Method** | **Description**                                    |
|------------|----------------------------------------------------|
| `list`     | Get the SCIM user group mappings for the tenant.   |
| `update`   | Update the SCIM user group mapping for the tenant. |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import SCIMUserGroupMappingAPI


def main():
    DOMAIN = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"

    scim_api = SCIMUserGroupMappingAPI(DOMAIN, API_KEY)

    scim_groups = scim_api.list()

    print(dumps(scim_groups, indent=4))
```
```json5
{
    "body": {
      "mappings": [],
      //...[snip]...//
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>TemplatesAPI</summary>
Manage templates

### Methods

| **Method** | **Description**                       |
|------------|---------------------------------------|
| `create`   | Create a private template.            |
| `get`      | Retrieve a private template.          |
| `update`   | Update a private template.            |
| `list`     | Retrieve a list of private templates. |
| `delete`   | Delete a private template by ID.      |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import TemplatesAPI


def main():
    DOMAIN = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"

    templates_api = TemplatesAPI(DOMAIN, API_KEY)

    templates = templates_api.list()

    print(dumps(templates, indent=4))
```
```json5
{
    "body": {
      "admin/templates": [],
      //...[snip]...//
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>UsersAPI</summary>
Manage tenant-wide users

### Methods

| **Method**          | **Description**                                                                |
|---------------------|--------------------------------------------------------------------------------|
| `create`            | Create a user in a Tines tenant.                                               |
| `get`               | Retrieve details of a specific user.                                           |
| `sign_in_activity`  | Retrieve a list of sign-in activities by a specified user.                     |
| `update`            | Update a User.                                                                 |
| `list`              | Retrieve a list of users from the Tines tenant.                                |
| `delete`            | Delete a specific user.                                                        |
| `resend_invitation` | Resend platform invitation to specified user.                                  |
| `expire_session`    | Expires a user’s session, signing them out of the Tines tenant on all devices. |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import UsersAPI


def main():
    DOMAIN = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"

    users_api = UsersAPI(DOMAIN, API_KEY)

    users = users_api.list()

    print(dumps(users, indent=4))
```
```json5
{
    "body": {
      "admin/users": [],
      //...[snip]...//
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>StorySyncDestinationsAPI</summary>
Manage story syncing

### Methods

| **Method**    | **Description**                                                                |
|---------------|--------------------------------------------------------------------------------|
| `create`      | Create a new sync destination and subscribe it to one or more stories.         |
| `list`        | Retrieve a paginated list of sync destinations configured on the tenant.       |
| `delete`      | Remove a sync destination configuration.                                       |
| `manual_sync` | Trigger an immediate push of all subscribed stories to the destination tenant. |

### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import StorySyncDestinationsAPI


def main():
    DOMAIN = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"

    story_sync_api = StorySyncDestinationsAPI(DOMAIN, API_KEY)

    story_syncs = story_sync_api.list()

    print(dumps(users, indent=4))
```
```json5
{
    "body": {
      "sync_destinations": [
        {
            "id": 23,
            "destination_tenant_url": "https://<<META.tenant.domain>>.tines.com",
            "destination_team_id": 42,
            "origin_team_id": 7,
            "subscriptions": [
                {
                "story": {
                    "id": 9981,
                    "name": "Example"
                },
                "status": "synced",
                "error_message": null
                }
            ]
        },
        //...[snip]...//
      ]
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>GroupsAPI</summary>
Pull group actions events and logs

### Methods

| **Method**        | **Description**                            |
|-------------------|--------------------------------------------|
| `list_run_events` | Retrieve a list of events for a group run. |
| `list_runs`       | Retrieve a list of group runs.             |


### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import GroupsAPI


def main():
    DOMAIN = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"

    groups_api = GroupsAPI(DOMAIN, API_KEY)

    events = groups_api.list_run_events(
        group_id = 1234,
        group_run_guid = "aaaabbbbccccddddeeeeffff"
    )

    print(dumps(events, indent=4))
```
```json5
{
    "body": {
      "group_run_events": [],
      //...[snip]...//
    },
    "headers": {...},
    "status_code": ...
}
```

</details>

<details>
<summary>DraftsAPI</summary>
Manage story drafts

### Methods

| **Method** | **Description**                        |
|------------|----------------------------------------|
| `create`   | Create a new draft for a story.        |
| `list`     | Retrieve a list of drafts for a story. |
| `delete`   | Delete a draft for a story.            |


### Subclasses
- **None**

### Usage:

```python
from json import dumps
from tapi import DraftsAPI


def main():
    DOMAIN = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"

    drafts_api = DraftsAPI(DOMAIN, API_KEY)

    drafts = drafts_api.list(story_id = 1234)

    print(dumps(drafts, indent=4))
```
```json5
{
    "body": {
      "drafts": [],
      //...[snip]...//
    },
    "headers": {...},
    "status_code": ...
}
```

</details>
