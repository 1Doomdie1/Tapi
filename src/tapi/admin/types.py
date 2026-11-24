from collections.abc import Mapping
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
