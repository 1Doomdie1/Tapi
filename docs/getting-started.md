# Getting started

tapi is an unofficial Python wrapper for the Tines REST API. This page covers installing it and
creating a client. It requires Python 3.11 or newer.

## Installation

tapi is not published on PyPI yet. Install it from a checkout of the repository:

```powershell
python -m pip install -e .
```

## Creating a client

`Tines` is the entry point. A client is bound to one tenant and one API key.

```python
from tapi import Tines

tines = Tines(tenant_domain="acme.tines.com", api_key="<your API key>")
```

| Argument        | Environment variable  | Meaning                                                                                                                                             |
| --------------- | --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tenant_domain` | `TINES_TENANT_DOMAIN` | The domain of your tenant, such as `acme.tines.com`. Self-hosted tenants and tenants with a custom domain use their own domain. A scheme is accepted and any path is ignored. |
| `api_key`       | `TINES_API_KEY`       | A Tines API key: personal, service, team or tenant owner.                                                                                           |
| `timeout`       | none                  | Seconds to wait for the connection and for each part of a reply. Defaults to 30.                                                                    |

All arguments are keyword-only. An argument takes precedence over its environment variable, so
`Tines()` with no arguments reads both values from the environment.

If the tenant domain or the API key is missing, creating the client raises
`TinesConfigurationError`.

## Closing the client

The client keeps connections open for reuse. Use it as a context manager, or call `close()` when
you are done:

```python
with Tines() as tines:
    ...
```

## What is available

The client and its core layer are in place. Endpoint modules are attached to `Tines` as attributes
as they are implemented. So far there are sixteen: [Info](endpoints/info.md), [AI](endpoints/ai.md),
[Apps](endpoints/apps.md), [Audit logs](endpoints/audit_logs.md), [Cases](endpoints/cases.md),
[Change requests](endpoints/change_requests.md), [Credentials](endpoints/credentials.md),
[Dashboards](endpoints/dashboards.md), [Folders](endpoints/folders.md),
[Reporting](endpoints/reporting.md), [Resources](endpoints/resources.md),
[Skills](endpoints/skills.md), [Stories](endpoints/stories.md) (with its
[actions](endpoints/stories_actions.md)), [Tags](endpoints/tags.md), [Teams](endpoints/teams.md) and
[Workbench](endpoints/workbench.md).

```python
response = tines.info.get()
response.status_code
response.data["stack"]["region"]
```

See [Architecture](architecture.md) for how the pieces fit together and
[Responses](responses.md) for what every call returns.
