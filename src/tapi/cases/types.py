from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any, Literal, NotRequired, TypedDict

CaseStatus = Literal["OPEN", "CLOSED"]

CasePriority = Literal["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]

CaseOrder = Literal[
    "RECENTLY_EDITED",
    "LEAST_RECENTLY_EDITED",
    "PRIORITY_ASC",
    "PRIORITY_DESC",
    "OPENED_ASC",
    "OPENED_DESC",
    "CREATED_ASC",
    "CREATED_DESC",
]

SlaStatus = Literal["WARNING", "EXCEEDED"]

SlaType = Literal["resolution", "response"]

NoteColor = Literal["white", "gold", "magenta", "green", "blue", "red", "mint", "indigo"]

NoteType = Literal["html", "text"]

Reaction = Literal["+1", "-1", "eyes", "heart", "white_check_mark"]

BlockColor = Literal[
    "primary", "white", "gold", "magenta", "green", "blue", "red", "mint", "indigo"
]

CaseActionType = Literal["webhook", "page", "chat", "story", "app"]

FieldType = Literal["string", "number", "boolean", "timestamp", "email", "url", "ip_address"]

FieldValidation = Literal["none", "options", "regex"]

WebhookNotification = Literal[
    "ALL",
    "CREATED",
    "ASSIGNED",
    "UNASSIGNED",
    "COMMENTED",
    "DELETED_COMMENT",
    "COMMENT_UPDATED",
    "STATUS_UPDATED",
    "SUB_STATUS_UPDATED",
    "SEVERITY_UPDATED",
    "TAGS_ADDED",
    "TAGS_REMOVED",
    "FILE_ATTACHED",
    "FILE_ATTACHED_AND_COMMENTED",
    "FILE_DELETED",
    "FILE_PASTED",
    "CHECKLIST_ITEM_COMPLETED",
    "CHECKLIST_ITEM_INCOMPLETE",
    "LINKED_CASE_ADDED",
    "LINKED_CASE_REMOVED",
    "METADATA_UPDATED",
    "SLA_WARNING",
    "SLA_EXCEEDED",
    "TEAM_UPDATED",
    "FIELD_UPDATED",
    "DESCRIPTION_UPDATED",
    "NOTE_ADDED",
    "NOTE_UPDATED",
    "NOTE_DELETED",
    "TITLE_UPDATED",
    "TASK_CREATED",
    "TASK_DELETED",
    "TASK_COMPLETED",
    "TASK_INCOMPLETE",
    "TASK_UPDATED",
    "TASK_ASSIGNED",
    "TASK_UNASSIGNED",
]

BlockType = Literal[
    "note",
    "file",
    "linked_cases",
    "metadata",
    "closure_conditions",
    "case_action",
    "block_group",
    "html",
]

ActivityType = Literal[
    "CREATED",
    "ASSIGNED",
    "UNASSIGNED",
    "STATUS_UPDATED",
    "SUB_STATUS_UPDATED",
    "SEVERITY_UPDATED",
    "COMMENTED",
    "DELETED_COMMENT",
    "COMMENT_UPDATED",
    "DESCRIPTION_UPDATED",
    "FIELD_UPDATED",
    "FILE_ATTACHED",
    "FILE_ATTACHED_AND_COMMENTED",
    "FILE_DELETED",
    "TAGS_ADDED",
    "TAGS_REMOVED",
    "RECORD_RESULT_SET_ADDED",
    "RECORD_RESULT_SET_REMOVED",
    "CHECKLIST_ITEM_COMPLETED",
    "CHECKLIST_ITEM_INCOMPLETE",
    "LINKED_CASE_ADDED",
    "LINKED_CASE_REMOVED",
    "METADATA_UPDATED",
    "NOTE_ADDED",
    "NOTE_DELETED",
    "NOTE_UPDATED",
    "SLA_WARNING",
    "SLA_EXCEEDED",
    "TASK_CREATED",
    "TASK_DELETED",
    "TASK_COMPLETED",
    "TASK_INCOMPLETE",
    "TASK_UPDATED",
    "TASK_ASSIGNED",
    "TASK_UNASSIGNED",
    "TEAM_UPDATED",
    "TITLE_UPDATED",
]

SearchField = Literal[
    "access_restricted",
    "applicable_sla_type",
    "assignee",
    "assignees",
    "author",
    "authors",
    "case_field",
    "case_id",
    "comment.author",
    "comment.created_at",
    "comment.text",
    "comment_count",
    "created_at",
    "description",
    "group",
    "linked_cases_count",
    "metadata",
    "name",
    "note.created_at",
    "note.text",
    "opened_at",
    "opened_by",
    "priority",
    "record.value",
    "recorded_sla_status",
    "resolved_at",
    "resolved_by",
    "restricted",
    "search",
    "severity",
    "sla",
    "sla_time",
    "status",
    "sub_status",
    "subscriber",
    "subscribers",
    "tag",
    "tags",
    "task.assignee",
    "task.completed",
    "task.text",
    "task_count",
    "team",
    "updated_at",
]

SearchOperator = Literal[
    "IS",
    "IS_NOT",
    "IS_ANY_OF",
    "IS_ALL_OF",
    "IS_NONE_OF",
    "CONTAINS",
    "NOT_CONTAINS",
    "CONTAINS_ALL",
    "NOT_CONTAINS_ALL",
    "CONTAINS_PHRASE",
    "NOT_CONTAINS_PHRASE",
    "STARTS_WITH",
    "ENDS_WITH",
    "FUZZY",
    "BEFORE",
    "AFTER",
    "ON",
    "BETWEEN",
    "IN_THE_LAST",
    "IS_EMPTY",
    "IS_NOT_EMPTY",
]

SearchSortField = Literal[
    "created_at", "name", "opened_at", "priority", "resolved_at", "updated_at"
]

SearchDirection = Literal["ASC", "DESC"]

SearchCollection = Literal["comment", "note", "record", "task"]

SearchGroupOperator = Literal["AND", "OR", "NOT"]


class ClosureCondition(TypedDict):
    name: str
    formula: str


class CaseTask(TypedDict):
    description: str
    assignee_ids: NotRequired[Sequence[int]]
    assignee_emails: NotRequired[Sequence[str]]


class TaskInput(TypedDict):
    description: str
    assignee_emails: NotRequired[Sequence[str]]


class CaseActionInput(TypedDict):
    url: str
    label: str
    action_type: CaseActionType
    action_text: NotRequired[str]
    query_params: NotRequired[Mapping[str, str]]


class NoteElement(TypedDict):
    content: str
    note_type: NoteType
    color: NotRequired[NoteColor]
    sensitive: NotRequired[bool]


class FileElement(TypedDict):
    filename: str
    file_contents: str
    annotation: NotRequired[str]


class CaseBlock(TypedDict):
    title: str
    block_type: BlockType
    elements: Sequence[NoteElement | FileElement]
    hidden: NotRequired[bool]
    default_collapsed: NotRequired[bool]
    guid: NotRequired[str]
    parent_block_guid: NotRequired[str]


class FieldOptions(TypedDict):
    options: Sequence[str]


class FieldRegex(TypedDict):
    regex: str


FieldValidationOptions = FieldOptions | FieldRegex


class TemplateButton(TypedDict):
    button_type: CaseActionType
    url: str
    label: str
    button_text: NotRequired[str]


class TemplateOptions(TypedDict, total=False):
    name: str
    description: str
    status: CaseStatus
    priority: CasePriority
    sub_status_id: int
    assignee_emails: Sequence[str]
    tag_names: Sequence[str]
    team_case_buttons: Sequence[TemplateButton]
    tasks: Sequence[TaskInput]
    closure_conditions: Sequence[ClosureCondition]
    blocks: Sequence[CaseBlock]
    field_values: Mapping[str, Any]
    metadata: Mapping[str, Any]


class FieldFilter(TypedDict):
    key: str
    value: Any


class RecordFieldFilter(TypedDict):
    id: int
    value: Any


class CaseFilters(TypedDict, total=False):
    search: str
    name: str
    comment: str
    note: str
    status: CaseStatus
    sub_status_names: Sequence[str]
    exclude_sub_status_names: Sequence[str]
    priority: Sequence[CasePriority]
    exclude_priorities: Sequence[CasePriority]
    assignees: Sequence[int | str]
    and_assignees: Sequence[int]
    exclude_assignees: Sequence[int]
    assigned_to_me: bool
    authors: Sequence[int | str]
    exclude_authors: Sequence[int]
    subscribed: bool
    my_open_tasks: bool
    tags: Sequence[str]
    and_tags: Sequence[str]
    or_tags: Sequence[str]
    exclude_tags: Sequence[str]
    metadata: dict[str, Any]
    and_metadata: Sequence[FieldFilter]
    or_metadata: Sequence[FieldFilter]
    fields: Sequence[FieldFilter]
    and_fields: Sequence[FieldFilter]
    or_fields: Sequence[FieldFilter]
    record_field: RecordFieldFilter
    records: Sequence[str]
    sla_status: Sequence[SlaStatus]
    and_sla_status: Sequence[SlaStatus]
    exclude_sla_status: Sequence[SlaStatus]
    sla_type: Sequence[SlaType]
    and_sla_type: Sequence[SlaType]
    exclude_sla_type: Sequence[SlaType]
    case_ids: Sequence[int]
    child_team_ids: Sequence[int]
    start_date: datetime | str
    end_date: datetime | str
    relative_date: str
    time_range: str
    opened_at_start_date: datetime | str
    opened_at_end_date: datetime | str
    opened_at_relative_date: str
    resolved_at_start_date: datetime | str
    resolved_at_end_date: datetime | str
    resolved_at_relative_date: str
    updated_at_start_date: datetime | str
    updated_at_end_date: datetime | str
    updated_at_relative_date: str


class BulkFieldUpdate(TypedDict):
    input_id: int
    value: Any
    upsert: NotRequired[bool]


class SearchCondition(TypedDict):
    field: SearchField
    operator: SearchOperator
    value: NotRequired[Any]
    key: NotRequired[str]


class SearchGroup(TypedDict):
    op: SearchGroupOperator
    nodes: "Sequence[SearchNode]"


class SearchNested(TypedDict):
    op: Literal["NESTED"]
    path: SearchCollection
    filter: "SearchNode"


SearchNode = SearchCondition | SearchGroup | SearchNested


class SearchSort(TypedDict):
    field: SearchSortField
    direction: SearchDirection


class SearchPage(TypedDict, total=False):
    size: int
    token: str
