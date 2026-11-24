from collections.abc import Mapping
from typing import Any, Literal, NotRequired, TypedDict

UserFilter = Literal["TENANT_OWNER"]

UserInclude = Literal["team_memberships"]

AgentType = Literal[
    "Agents::EmailAgent",
    "Agents::EventTransformationAgent",
    "Agents::HTTPRequestAgent",
    "Agents::IMAPAgent",
    "Agents::LLMAgent",
    "Agents::TriggerAgent",
    "Agents::WebhookAgent",
    "Agents::SendToStoryAgent",
]

ReadAccess = Literal["TEAM", "GLOBAL", "SPECIFIC_TEAMS"]

EgressActionType = Literal["http-request", "send-email"]

SyncMode = Literal["live_readonly", "draft_editable"]

SmtpAuthType = Literal["plain", "login", "cram_md5"]

SmtpEncryptionMode = Literal["none", "tls", "starttls_auto", "starttls_strict"]

ActionInputType = Literal[
    "TEXT", "NUMBER", "BOOLEAN", "DATE", "OBJECT", "OPTION", "CODE", "CREDENTIAL"
]


class ActionInput(TypedDict):
    name: str
    type: ActionInputType
    required: NotRequired[bool]
    description: NotRequired[str]
    default_value: NotRequired[Any]
    data: NotRequired[Mapping[str, Any]]
