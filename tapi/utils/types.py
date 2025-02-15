from enum   import IntEnum, StrEnum
from typing import TypedDict, Union, Dict, Any

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
    body:        Union[Dict[str, Any], str]
    headers:     Dict[str, Any]
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

class ReactionType(StrEnum):
    PLUS_ONE         = "+1"
    MINUS_ONE        = "-1"
    EYES             = "eyes"
    HEART            = "heart"
    WHITE_CHECK_MARK = "white_check_mark"

class CaseNoteColor(StrEnum):
    GOLD    = "gold"
    BLUE    = "blue"
    GREEN   = "green"
    WHITE   = "white"
    MAGENTA = "magenta"

class LogSeverityLevel(IntEnum):
    INFO    = 3
    ERROR   = 4
    WARNING = 2

class AuditLogType(StrEnum):
    LOGIN                                = "Login"
    USER_EDIT                            = "UserEdit"
    OPERATION                            = "operation"
    TEAM_UPDATE                          = "TeamUpdate"
    FORM_UPDATE                          = "FormUpdate"
    LINK_CHANGE                          = "LinkChange"
    STORY_IMPORT                         = "StoryImport"
    USER_DELETION                        = "UserDeletion"
    GROUP_FLATTEN                        = "GroupFlatten"
    FOLDER_UPDATE                        = "FolderUpdate"
    STORY_ARCHIVE                        = "StoryArchive"
    STORY_RESTORE                        = "StoryRestore"
    TEAM_CREATION                        = "TeamCreation"
    EVENT_DELETION                       = "EventDeletion"
    STORY_CREATION                       = "StoryCreation"
    STORY_MOVEMENT                       = "StoryMovement"
    TEMPLATE_UPDATE                      = "TemplateUpdate"
    TEAM_CASE_UPDATE                     = "TeamCaseUpdate"
    STORY_API_CHANGE                     = "StoryApiChange"
    FOLDER_CREATION                      = "FolderCreation"
    CREDENTIAL_SAVE                      = "CredentialSave"
    USERS_INVITATION                     = "UsersInvitation"
    TEAM_DESTRUCTION                     = "TeamDestruction"
    FORM_FIELD_UPDATE                    = "FormFieldUpdate"
    GROUP_EXTRACTION                     = "GroupExtraction"
    STORY_NAME_CHANGE                    = "StoryNameChange"
    TEMPLATE_CREATION                    = "TemplateCreation"
    FORM_FIELD_REORDER                   = "FormFieldReorder"
    FORM_FIELD_REMOVAL                   = "FormFieldRemoval"
    TEAM_CASE_CREATION                   = "TeamCaseCreation"
    ANALYTICS_CAPTURE                    = "AnalyticsCapture"
    ACTION_SIZE_CHANGE                   = "ActionSizeChange"
    RECORD_TYPE_UPDATE                   = "RecordTypeUpdate"
    USER_REINVITATION                    = "UserReinvitation"
    TEAM_MEMBER_REMOVAL                  = "TeamMemberRemoval"
    BATCH_STORY_ARCHIVE                  = "BatchStoryArchive"
    ACTIONS_NAME_CHANGE                  = "ActionsNameChange"
    FOLDER_DESTRUCTION                   = "FolderDestruction"
    FORM_FIELD_ADDITION                  = "FormFieldAddition"
    STORY_LOCKED_CHANGE                  = "StoryLockedChange"
    TEST_STORY_CREATION                  = "TestStoryCreation"
    TEST_STORY_DELETION                  = "TestStoryDeletion"
    TEAM_CASE_TAGS_UPDATE                = "TeamCaseTagsUpdate"
    RECORD_REPORT_UPDATE                 = "RecordReportUpdate"
    JOBS_QUEUED_DELETION                 = "JobsQueuedDeletion"
    GLOBAL_RESOURCE_EDIT                 = "GlobalResourceEdit"
    CREDENTIAL_MOVEMENT                  = "CredentialMovement"
    EXAMPLE_STORY_IMPORT                 = "ExampleStoryImport"
    RECORD_TYPE_CREATION                 = "RecordTypeCreation"
    RECORD_WRITER_UPDATE                 = "RecordWriterUpdate"
    STORY_ITEMS_CREATION                 = "StoryItemsCreation"
    STORY_ITEMS_MOVEMENT                 = "StoryItemsMovement"
    STORY_JOBS_CLEARANCE                 = "StoryJobsClearance"
    STORY_VERSION_CREATE                 = "StoryVersionCreate"
    STORY_VERSION_IMPORT                 = "StoryVersionImport"
    TEAM_CASE_FILE_ATTACH                = "TeamCaseFileAttach"
    TENANT_CONFIG_CHANGE                 = "TenantConfigChange"
    TEMPLATE_DESTRUCTION                 = "TemplateDestruction"
    STORY_PRIORITY_CHANGE                = "StoryPriorityChange"
    STORY_EVENTS_DELETION                = "StoryEventsDeletion"
    RESOURCE_REPLACEMENT                 = "ResourceReplacement"
    ACTION_METRICS_CHANGE                = "ActionMetricsChange"
    LAST_EVENT_RE_EMISSION               = "LastEventReEmission"
    ACTION_LOGS_CLEARANCE                = "ActionLogsClearance"
    STORY_DISABLED_CHANGE                = "StoryDisabledChange"
    TEAM_MEMBERS_ADDITION                = "TeamMembersAddition"
    JOBS_RETRYING_DELETION               = "JobsRetryingDeletion"
    ANNOTATION_SIZE_CHANGE               = "AnnotationSizeChange"
    ACTIONS_OPTIONS_CHANGE               = "ActionsOptionsChange"
    RECORD_REPORT_CREATION               = "RecordReportCreation"
    RECORD_REPORT_DELETION               = "RecordReportDeletion"
    RECORD_WRITER_CREATION               = "RecordWriterCreation"
    STORY_RECIPIENT_UPDATE               = "StoryRecipientUpdate"
    STORY_VERSION_DELETION               = "StoryVersionDeletion"
    STORY_RECIPIENT_REMOVAL              = "StoryRecipientRemoval"
    ACTION_MEMORY_CLEARANCE              = "ActionMemoryClearance"
    ACTIONS_DISABLED_CHANGE              = "ActionsDisabledChange"
    ACTIONS_EVENTS_DELETION              = "ActionsEventsDeletion"
    ARCHIVED_STORY_DELETION              = "ArchivedStoryDeletion"
    CREDENTIAL_DESTRUCTION               = "CredentialDestruction"
    CREDENTIAL_REPLACEMENT               = "CredentialReplacement"
    ACTIONS_SCHEDULE_CHANGE              = "ActionsScheduleChange"
    RECORD_RESULT_SET_UPDATE             = "RecordResultSetUpdate"
    STORY_ACTIONS_AUTO_ALIGN             = "StoryActionsAutoAlign"
    RECORD_TYPE_DESTRUCTION              = "RecordTypeDestruction"
    STORY_ITEMS_DESTRUCTION              = "StoryItemsDestruction"
    TEAM_CASE_COMMENT_UPDATE             = "TeamCaseCommentUpdate"
    TEAM_CASE_WEBHOOK_UPDATE             = "TeamCaseWebhookUpdate"
    GLOBAL_RESOURCE_MOVEMENT             = "GlobalResourceMovement"
    STORY_ACTIONS_AUTO_LAYOUT            = "StoryActionsAutoLayout"
    GLOBAL_RESOURCE_CREATION             = "GlobalResourceCreation"
    ARCHIVED_STORY_DELETE_ALL            = "ArchivedStoryDeleteAll"
    STORY_DESCRIPTION_CHANGE             = "StoryDescriptionChange"
    STORY_SEND_TO_STORY_CHANGE           = "StorySendToStoryChange"
    STORY_RECIPIENT_ADDITION             = "StoryRecipientAddition"
    STORY_VERSION_NAME_CHANGE            = "StoryVersionNameChange"
    TEAM_CASE_BUTTON_CREATION            = "TeamCaseButtonCreation"
    ACTIONS_MONITORING_CHANGE            = "ActionsMonitoringChange"
    ANNOTATION_CONTENT_CHANGE            = "AnnotationContentChange"
    RECORD_WRITER_DESTRUCTION            = "RecordWriterDestruction"
    SSO_CONFIGURATION_OIDC_SET           = "SsoConfigurationOidcSet"
    SSO_CONFIGURATION_SAML_SET           = "SsoConfigurationSamlSet"
    STORY_ACTIONS_POSITIONING            = "StoryActionsPositioning"
    TENANT_FEATURE_FLAG_TOGGLE           = "TenantFeatureFlagToggle"
    TEAM_CASE_COMMENT_CREATION           = "TeamCaseCommentCreation"
    TENANT_PLAN_UPGRADE_REQUEST          = "TenantPlanUpgradeRequest"
    STORY_KEEP_EVENTS_FOR_CHANGE         = "StoryKeepEventsForChange"
    RECORD_REPORT_ELEMENT_UPDATE         = "RecordReportElementUpdate"
    GLOBAL_RESOURCE_DESTRUCTION          = "GlobalResourceDestruction"
    SSO_CONFIGURATION_DEFAULT_SET        = "SsoConfigurationDefaultSet"
    STORY_REPORTING_STATUS_CHANGE        = "StoryReportingStatusChange"
    TEAM_CASE_ADD_COMMENT_REACTION       = "TeamCaseAddCommentReaction"
    TEAM_CASE_SUBSCRIBER_CREATION        = "TeamCaseSubscriberCreation"
    TEAM_CASE_SUBSCRIBER_DELETION        = "TeamCaseSubscriberDeletion"
    TEAM_CASES_SAVED_VIEW_CREATION       = "TeamCasesSavedViewCreation"
    AUTHENTICATION_TOKEN_CREATION        = "AuthenticationTokenCreation"
    AUTHENTICATION_TOKEN_DELETION        = "AuthenticationTokenDeletion"
    CREDENTIAL_OAUTH_TOKEN_REFRESH       = "CredentialOauthTokenRefresh"
    RECORD_REPORT_ELEMENT_CREATION       = "RecordReportElementCreation"
    CUSTOM_CERTIFICATE_AUTHORITY_SET     = "CustomCertificateAuthoritySet"
    TEAM_CASE_REMOVE_COMMENT_REACTION    = "TeamCaseRemoveCommentReaction"
    TEAM_CASES_SAVED_VIEW_DESTRUCTION    = "TeamCasesSavedViewDestruction"
    RECORD_REPORT_ELEMENT_DESTRUCTION    = "RecordReportElementDestruction"
    RECORD_REPORT_ELEMENT_COLUMN_REORDER = "RecordReportElementColumnReorder"