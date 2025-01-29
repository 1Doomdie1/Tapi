from enum   import IntEnum, StrEnum
from typing import TypedDict, Union

class KeepEventsFor(IntEnum):
    ONE_HOUR                      = 3600
    SIX_HOURS                     = 21600
    ONE_DAY                       = 86400
    THREE_DAYS                    = 259200
    SEVEN_DAYS                    = 604800
    FOURTEEN_DAYS                 = 1209600
    THIRTY_DAYS                   = 2592000
    SIXTY_DAYS                    = 5184000
    NINETY_DAYS                   = 7776000
    ONE_HUNDRED_EIGHTY_DAYS       = 15552000
    THREE_HUNDRED_SIXTY_FIVE_DAYS = 31536000

class StoryMode(StrEnum):
    ALL  = ""
    LIVE = "LIVE"
    TEST = "TEST"

class SendToStoryAccessSource(StrEnum):
    OFF               = "OFF"
    STS               = "STS"
    WORKBENCH         = "WORKBENCH"
    STS_AND_WORKBENCH = "STS_AND_WORKBENCH"

class SendToStoryAccess(StrEnum):
    TEAM           = "TEAM"
    GLOBAL         = "GLOBAL"
    SPECIFIC_TEAMS = "SPECIFIC_TEAMS"

class Filter(StrEnum):
    LOCKED                 = "LOCKED"
    FAVORITE               = "FAVORITE"
    DISABLED               = "DISABLED"
    PUBLISHED              = "PUBLISHED"
    API_ENABLED            = "API_ENABLED"
    HIGH_PRIORITY          = "HIGH_PRIORITY"
    SEND_TO_STORY_ENABLED  = "SEND_TO_STORY_ENABLED"
    CHANGE_CONTROL_ENABLED = "CHANGE_CONTROL_ENABLED"

class StoriesReturnOrder(StrEnum):
    NAME                  = "NAME"
    NAME_DESC             = "NAME_DESC"
    RECENTLY_EDITED       = "RECENTLY_EDITED"
    ACTION_COUNT_ASC      = "ACTION_COUNT_ASC"
    ACTION_COUNT_DESC     = "ACTION_COUNT_DESC"
    LEAST_RECENTLY_EDITED = "LEAST_RECENTLY_EDITED"

class Mode(StrEnum):
    NEW = "new"
    VERSION_REPLACE = "versionReplace"

class Role(StrEnum):
    VIEWER = "VIEWER"
    EDITOR = "EDITOR"
    TEAM_ADMIN = "TEAM_ADMIN"

class CasePriority(StrEnum):
    LOW      = "LOW"
    HIGH     = "HIGH"
    INFO     = "INFO"
    MEDIUM   = "MEDIUM"
    CRITICAL = "CRITICAL"

class CaseStatus(StrEnum):
    OPEN  = "OPEN"
    CLOSE = "CLOSE"

class CaseReturnOrder(StrEnum):
    OPENED_ASC            = "OPENED_ASC"
    OPENED_DESC           = "OPENED_DESC"
    CREATED_ASC           = "CREATED_ASC"
    CREATED_DESC          = "CREATED_DESC"
    PRIORITY_ASC          = "PRIORITY_ASC"
    PRIORITY_DESC         = "PRIORITY_DESC"
    RECENTLY_EDITED       = "RECENTLY_EDITED"
    LEAST_RECENTLY_EDITED = "LEAST_RECENTLY_EDITED"

class CaseActionType(StrEnum):
    PAGE    = "page"
    WEBHOOK = "webhook"


class CaseActivityType(StrEnum):
    CREATED                     = "CREATED"
    ASSIGNED                    = "ASSIGNED"
    COMMENTED                   = "COMMENTED"
    UNASSIGNED                  = "UNASSIGNED"
    TAGS_ADDED                  = "TAGS_ADDED"
    SLA_WARNING                 = "SLA_WARNING"
    FILE_DELETED                = "FILE_DELETED"
    TAGS_REMOVED                = "TAGS_REMOVED"
    SLA_EXCEEDED                = "SLA_EXCEEDED"
    FILE_ATTACHED               = "FILE_ATTACHED"
    FIELD_UPDATED               = "FIELD_UPDATED"
    STATUS_UPDATED              = "STATUS_UPDATED"
    DELETED_COMMENT             = "DELETED_COMMENT"
    METADATA_UPDATED            = "METADATA_UPDATED"
    SEVERITY_UPDATED            = "SEVERITY_UPDATED"
    LINKED_CASE_ADDED           = "LINKED_CASE_ADDED"
    SUB_STATUS_UPDATED          = "SUB_STATUS_UPDATED"
    LINKED_CASE_REMOVED         = "LINKED_CASE_REMOVED"
    RECORD_RESULT_SET_ADDED     = "RECORD_RESULT_SET_ADDED"
    CHECKLIST_ITEM_COMPLETED    = "CHECKLIST_ITEM_COMPLETED"
    CHECKLIST_ITEM_INCOMPLETE   = "CHECKLIST_ITEM_INCOMPLETE"
    RECORD_RESULT_SET_REMOVED   = "RECORD_RESULT_SET_REMOVED"
    FILE_ATTACHED_AND_COMMENTED = "FILE_ATTACHED_AND_COMMENTED"

class CaseInputType(StrEnum):
    STRING    = "string"
    NUMBER    = "number"
    BOOLEAN   = "boolean"
    TIMESTAMP = "timestamp"

class CaseValidationType(StrEnum):
    REGEX   = "regex"
    OPTIONS = "options"

class HTTPResponse(TypedDict):
    body:        Union[dict, str]
    headers:     dict
    status_code: int

class ActionType(StrEnum):
    IMAP_AGENT            = "Agents::IMAPAgent"
    EMAIL_AGENT           = "Agents::EmailAgent"
    GROUP_AGENT           = "Agents::GroupAgent"
    TRIGGER_AGENT         = "Agents::TriggerAgent"
    WEB_HOOK_AGENT        = "Agents::WebhookAgent"
    HTTP_REQUEST_AGENT    = "Agents::HTTPRequestAgent"
    SEND_T0_STORY_AGENT   = "Agents::SendToStoryAgent"
    EVENT_TRANSFORM_AGENT = "Agents::EventTransformationAgent"
