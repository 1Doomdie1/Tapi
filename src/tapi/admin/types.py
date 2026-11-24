from collections.abc import Mapping, Sequence
from typing import Any, Literal, NotRequired, TypedDict

UserFilter = Literal["ALL", "ADMIN", "ACTIVE", "INACTIVE", "TENANT_OWNER"]

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
    "eventTransformation",
    "trigger",
    "webhook",
    "httpRequest",
    "sendToStory",
    "email",
    "imap",
    "grpcRequest",
    "mcpRequest",
    "group",
    "groupInput",
    "groupOutput",
    "form",
    "file",
    "record",
    "case",
    "runScript",
    "llm",
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


class UserGroupMappingEntry(TypedDict, total=False):
    group_name: str
    team_name: str
    role_name: str


class UserGroupMappingTenantPermission(TypedDict, total=False):
    group_name: str
    permission: str


class UserGroupMapping(TypedDict, total=False):
    mappings: Sequence[UserGroupMappingEntry]
    tenant_permissions: Sequence[UserGroupMappingTenantPermission]
    tenant_owners_groups: Sequence[str]
