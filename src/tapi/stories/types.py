from typing import Literal, NotRequired, TypedDict

StoryMode = Literal["TEST", "LIVE"]

StoryFilter = Literal[
    "SEND_TO_STORY_ENABLED",
    "HIGH_PRIORITY",
    "API_ENABLED",
    "FAVORITE",
    "CHANGE_CONTROL_ENABLED",
    "CHANGE_CONTROL_DISABLED",
    "ENABLED",
    "DISABLED",
    "LOCKED",
    "ALL_STORIES",
    "WORKBENCH_ENABLED",
    "TUNNELS_ENABLED",
]

StoryOrder = Literal[
    "NAME",
    "NAME_DESC",
    "RECENTLY_EDITED",
    "LEAST_RECENTLY_EDITED",
    "ACTION_COUNT_ASC",
    "ACTION_COUNT_DESC",
    "CONCURRENT_RUNS_COUNT_DESC",
    "PENDING_ACTION_RUNS_COUNT_DESC",
    "NOT_WORKING_ACTIONS_COUNT_DESC",
]

KeepEventsFor = Literal[
    3600,
    21600,
    86400,
    259200,
    604800,
    1209600,
    2592000,
    5184000,
    7776000,
    15552000,
    31536000,
]

SendToStoryAccessSource = Literal["STS", "STS_AND_WORKBENCH", "WORKBENCH", "OFF"]

SendToStoryAccess = Literal["TEAM", "GLOBAL", "SPECIFIC_TEAMS"]

DiagramFormat = Literal["png", "svg"]

DiagramContent = Literal["full", "actions"]

ImportMode = Literal["new", "versionReplace"]

ActionType = Literal[
    "Agents::EmailAgent",
    "Agents::EventTransformationAgent",
    "Agents::HTTPRequestAgent",
    "Agents::IMAPAgent",
    "Agents::LLMAgent",
    "Agents::TriggerAgent",
    "Agents::WebhookAgent",
    "Agents::SendToStoryAgent",
    "Agents::GroupAgent",
    "Agents::RunScriptAgent",
]

ActionFilterType = Literal[
    "Agents::CaseAgent",
    "Agents::EmailAgent",
    "Agents::EventTransformationAgent",
    "Agents::FormAgent",
    "Agents::GroupAgent",
    "Agents::HTTPRequestAgent",
    "Agents::IMAPAgent",
    "Agents::LLMAgent",
    "Agents::RecordAgent",
    "Agents::RunScriptAgent",
    "Agents::SendToStoryAgent",
    "Agents::TriggerAgent",
    "Agents::WebhookAgent",
]

LinkType = Literal["DEFAULT", "NO_MATCH", "FAILURE"]

ActionLogLevel = Literal[2, 3, 4]


class ActionPosition(TypedDict):
    """The coordinates of an action on the story diagram."""

    x: float
    y: float


class NotePosition(TypedDict):
    """The coordinates of a note on the story diagram."""

    x: int
    y: int


class Link(TypedDict):
    """A link between two actions: the ``source_id`` and the ``receiver_id``."""

    source_id: int
    receiver_id: int


class SourceLink(TypedDict):
    """A link from a source action: its ``source_id`` and, optionally, the link ``type``."""

    source_id: int
    type: NotRequired[LinkType]


class ReceiverLink(TypedDict):
    """A link to a receiver action: its ``receiver_id`` and, optionally, the link ``type``."""

    receiver_id: int
    type: NotRequired[LinkType]
