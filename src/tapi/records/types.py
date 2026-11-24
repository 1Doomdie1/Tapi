from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any, Literal, NotRequired, TypedDict

RecordInclude = Literal[
    "record_type", "parent_record", "child_records", "child_record_ids", "cases"
]

RecordSearchInclude = Literal["record_type", "parent_record"]

FieldFormat = Literal["json", "text", "txt", "plain"]

FieldResultType = Literal[
    "TEXT",
    "TEXT_ENUM",
    "TEXT_REGEX",
    "EMAIL",
    "URL",
    "IP_ADDRESS",
    "NUMBER",
    "BOOLEAN",
    "TIMESTAMP",
    "JSON",
    "ARTIFACT",
]

RetentionColumn = Literal["CREATED_AT", "UPDATED_AT"]

OnLimitReached = Literal["REJECT", "EVICT_OLDEST"]

RecordTypeOrder = Literal["NAME", "CREATED_AT", "UPDATED_AT"]

SortDirection = Literal["ASC", "DESC"]

RecordViewOrder = Literal["NAME", "RECENTLY_CREATED", "RECENTLY_UPDATED"]

RecordViewImportMode = Literal["new", "replace"]

FilterOperator = Literal[
    "EQUAL",
    "NOT_EQUAL",
    "GREATER_THAN",
    "GREATER_THAN_OR_EQUAL_TO",
    "LESS_THAN",
    "LESS_THAN_OR_EQUAL_TO",
    "IS_ANY_OF",
    "IS_NONE_OF",
    "CONTAINS",
    "STARTS_WITH",
    "ENDS_WITH",
    "IS_EMPTY",
    "IS_NOT_EMPTY",
    "IS_TRUE",
    "IS_FALSE",
    "IS_IN_ANY_CIDR",
    "IS_NOT_IN_ANY_CIDR",
]

TimeRangeField = Literal["created_at", "updated_at"]

RollingDateRange = Literal[
    "TODAY", "YESTERDAY", "LAST_7_DAYS", "LAST_31_DAYS", "LAST_365_DAYS", "ALL_TIME"
]

AggregationFunction = Literal["COUNT", "SUM", "AVG", "MIN", "MAX", "MEDIAN", "P90", "P95", "P99"]

DateTrunc = Literal["hour", "day", "week", "month", "year"]


class FieldValue(TypedDict):
    value: Any
    field_id: NotRequired[int]
    field_name: NotRequired[str]


class RecordFilterCondition(TypedDict):
    operator: FilterOperator
    field_id: NotRequired[int]
    field_name: NotRequired[str]
    value: NotRequired[Any]


class RecordFilterGroup(TypedDict):
    op: Literal["AND"]
    nodes: "Sequence[RecordFilterNode]"


RecordFilterNode = RecordFilterCondition | RecordFilterGroup


class RecordSort(TypedDict):
    field_id: NotRequired[int]
    field_name: NotRequired[str]
    direction: NotRequired[SortDirection]


class RecordTimeRange(TypedDict, total=False):
    field: TimeRangeField
    rolling_date_range: RollingDateRange
    range_start: datetime | str
    range_end: datetime | str


class RecordAggregation(TypedDict):
    fn: AggregationFunction
    field_id: NotRequired[int]
    field_name: NotRequired[str]
    alias: NotRequired[str]


class RecordGroupBy(TypedDict, total=False):
    field_id: int
    field_name: str
    date_trunc: DateTrunc


class RecordOrderBy(TypedDict, total=False):
    field_id: int
    field_name: str
    alias: str
    direction: SortDirection


class RecordTypeField(TypedDict):
    name: str
    result_type: FieldResultType
    fixed_values: NotRequired[Sequence[str]]
    description: NotRequired[str]
    config: NotRequired[Mapping[str, Any]]


class RecordTypeFieldChange(TypedDict, total=False):
    id: int
    name: str
    result_type: FieldResultType
    fixed_values: Sequence[str]
    description: str
    config: Mapping[str, Any]
