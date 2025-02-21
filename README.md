from tapi.utils.types import AuditLogType

# Tapi (Tines API)
A simple Python wrapper for the Tines API.

## ⚠ Disclaimer 
The library is still under development so major changes and bugs are to be expected. Please feel free to open issues if you encounter any!
## ⚙️Installation 
```bash
git clone https://github.com/1Doomdie1/Tapi.git
cd tapi
py -m build -s -w
pip install .
```

## 🔄 Usage

### ✨ Using the main `TenantAPI` class
This class provides access to all endpoints offered by the Tines API.

```python
from tapi import TenantAPI

def main():
    tenant = TenantAPI(<DOMAIN>, <API_KEY>)
    teams = tenant.teams.list()
    cases = tenant.cases.list()
    stories = tenant.stories.list()

if __name__ == "__main__":
    main()
```

### 🔧 Using specific endpoint classes
While the main `TenantAPI` class is convenient, using specific endpoint classes may be preferable in certain scenarios. Each class requires `DOMAIN` and `API_KEY` to be passed explicitly.

```python
from tapi import CaseAPI, TeamsAPI, StoriesAPI

def main():
    DOMAIN = "MY_COOL_DOMAIN"
    API_KEY = "DO_NOT_PUT_THIS_ON_GITHUB"

    cases_api = CaseAPI(DOMAIN, API_KEY)
    teams_api = TeamsAPI(DOMAIN, API_KEY)
    stories_api = StoriesAPI(DOMAIN, API_KEY)

if __name__ == "__main__":
    main()
```

### Disabling SSL verification
There are cases when SSL verification can pose a problem in making a request to Tines REST API, fortunately
there is an easy way of disabling SSL verification in Tapi. Here is how:

```python

import tapi

tapi.utils.http.disable_ssl_verification()
```

### Classes

<details>
<summary>TenantAPI</summary>
This class is designed to be used as a "parent" class from which all other endpoints in tines can be accessed.

### Methods

| **Method** | **Description**                        |
|------------|----------------------------------------|
| `info`     | Retries information about the tenant.  |

### Subclasses

| **Path**                | **Class**        | **Description**            |
|-------------------------|------------------|----------------------------|
| `TenantAPI.cases`       | `CaseAPI`        | Manage cases.              |
| `TenantAPI.teams`       | `TeamsAPI`       | Manage teams.              |
| `TenantAPI.stories`     | `StoriesAPI`     | Manage workflows.          |
| `TenantAPI.audit_logs`  | `AuditLogsAPI`   | Pull tenant logs.          |
| `TenantAPI.credentials` | `CredentialsAPI` | Manage tenant credentials. |


### Usage:
```python
from json import dumps
from tapi import TenantAPI

def main():
    DOMAIN  = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"
    
    tenant = TenantAPI(DOMAIN, API_KEY)
    
    cases = tenant.cases.list()
    
    print(dumps(cases, indent = 4))
```
```json
{
    "body": {
        "cases": [
            {
                "case_id": 1,
                "name": "My Case Name",
                "description": "",
                "status": "OPEN",
                ...[snip]...
            }
        ...[snip]...
        ]
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

| **Method**     | **Description**                         |
|----------------|-----------------------------------------|
| `create`       | Create story.                           |
| `get`          | Get story details.                      |
| `update`       | Update story details.                   |
| `list`         | List all stories in the tenant or team. |
| `delete`       | Delete story.                           |
| `batch_delete` | Delete multiple stories.                |
| `export`       | Export story.                           |
| `import_`      | Import story.                           |

### Subclasses

| **Path**                           | **Class**          | **Description**              |
|------------------------------------|--------------------|------------------------------|
| `TenantAPI.stories.runs`           | `RunsAPI`          | Manage case runs.            |
| `TenantAPI.stories.notes`          | `NotesAPI`         | Manage case notes.           |
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
```json
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
                ...[snip]...
            }
        ...[snip]...
        ]
    },
    "headers": {...},
    "status_code": ...,
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
```json
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
            ...[snip]...
        ]
    },
    "headers": {...},
    "status_code": ...,
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
```json
{
    "body": {
        "story_versions": [
            {
                "id": 69670,
                "name": "",
                "description": "",
                "timestamp": "2025-01-27T21:20:00Z"
            },
            ...[snip]...
        ],
    },
    "headers": {...},
    "status_code": ...,
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
```json
{
    "body": {
        "teams": [
            {
                "id": 12345,
                "name": "My Team",
                "groups": []
            },
            ...[snip]...
        ],
    },
    "headers": {...},
    "status_code": ...,
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
```json
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
            ...[snip]...
        ],
    },
    "headers": {...},
    "status_code": ...,
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
| `TenantAPI.cases.inputs`       | `CaseInputsAPI`      | Manage case inputs.      |
| `TenantAPI.cases.fields`       | `CaseFieldsAPI`      | Manage case fields.      |
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
from tapi import CaseAPI

def main():
    DOMAIN  = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"
    
    case_api = CaseAPI(DOMAIN, API_KEY)
    
    cases = case_api.list()
    
    print(dumps(cases, indent = 4))
```
```json
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
            ...[snip]...
        ],
    },
    "headers": {...},
    "status_code": ...,
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
```json
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
            ...[snip]...
        ],
    },
    "headers": {...},
    "status_code": ...,
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
```json
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
                    "email": john@doe.io,
                    "avatar_url": "",
                    "is_service_account": false
                },
                "reactions": []
            },
            ...[snip]...
        ],
    },
    "headers": {...},
    "status_code": ...,
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
```json
{
    "body": {
        "case_id": 1234,
        "assignees": [...],
        ...[snip]...
    },
    "headers": {...},
    "status_code": ...,
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
```json
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
    "status_code": ...,
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
```json
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
    "status_code": ...,
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
```json
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
            ...[snip]...
        ],
    },
    "headers": {...},
    "status_code": ...,
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
from json import dumps
from tapi import ReactionType
from tapi import CaseCommentsReactionsAPI


def main():
    DOMAIN = "my-cool-domain-1234"
    API_KEY = "do_not_put_this_on_github_lol"

    comments_reactions_api = CaseCommentsReactionsAPI(DOMAIN, API_KEY)

    reaction = comments_reactions_api.add(
        case_id=1234,
        comment_id=5678,
        value=ReactionType.PLUS_ONE
    )

    print(dumps(comments, indent=4))
```
```json
{
    "body": {
    ...[snip]...
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
    ...[snip]...
    },
    "headers": {...},
    "status_code": ...,
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
```json
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
            ...[snip]...
        ],
    },
    "headers": {...},
    "status_code": ...,
}
```

</details>

<details>
<summary>CaseFilesAPI</summary>
Manage case files.

### Methods

| **Method** | **Description**                      |
|------------|--------------------------------------|
| `create`   | Attach a file to a case.             |
| `get`      | Retrieve details for a case file.    |
| `list`     | Retrieve a list of files for a case. |
| `delete`   | Delete a file from a case.           |
| `download` | Retrieve a case file attachment.     |

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
```json
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
            ...[snip]...
        ],
        ...[snip]...
    },
    "headers": {...},
    "status_code": ...,
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
```json
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
        ...[snip]...
    },
    "headers": {...},
    "status_code": ...,
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
```json
{
    "body": {
        "case_id": 1234,
        "metadata": {
            "name": "John Doe",
        }
    },
    "headers": {...},
    "status_code": ...,
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
```json
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
            ...[snip]...
        ],
        ...[snip]...
    },
    "headers": {...},
    "status_code": ...,
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
```json
{
    "body": {
        "case_id": 1234,
        "records": [
            {
                "record_type_id": 1419,
                "record_type_name": "My Record Type",
                "record_type_record_results": [...]
            },
            ...[snip]...
        ],
        ...[snip]...
    },
    "headers": {...},
    "status_code": ...,
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
```json
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
        ...[snip]...
    },
    "headers": {...},
    "status_code": ...,
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
```json
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
                ...[snip]...
            }
        ],
        ...[snip]...
    },
    "headers": {...},
    "status_code": ...,
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
```json
{
    "body": {
        "agents":[...],
        ...[snip]...
    },
    "headers": {...},
    "status_code": ...,
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
```json
{
    "body": {
        "action_logs":[...],
        ...[snip]...
    },
    "headers": {...},
    "status_code": ...,
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
```json
{
    "body": {
        "annotations":[...],
        ...[snip]...
    },
    "headers": {...},
    "status_code": ...,
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
from json import dumps
from tapi import AuditLogsAPI
from tapi import AuditLogType


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
```json
{
    "body": {
        "audit_logs":[...],
        ...[snip]...
    },
    "headers": {...},
    "status_code": ...,
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
```json
{
    "body": {
        "user_credentials":[...],
        ...[snip]...
    },
    "headers": {...},
    "status_code": ...,
}
```

</details>