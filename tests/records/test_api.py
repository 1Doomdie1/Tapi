from datetime import UTC, datetime

import httpx
import pytest

from tests.support import Case, assert_covers, assert_sent, case_id

RECORDS = "/api/v2/records"

FIELD_VALUES = [
    {"field_name": "status", "value": "open"},
    {"field_id": 103, "value": {"event_id": 1}},
    {"field_name": "owner", "value": None},
]

FILTER = {
    "op": "AND",
    "nodes": [
        {"field_name": "Status", "operator": "EQUAL", "value": "open"},
        {
            "op": "AND",
            "nodes": [{"field_id": 102, "operator": "IS_ANY_OF", "value": ["high", "critical"]}],
        },
    ],
}

TIME_RANGE_WIRE = [
    {"field": "updated_at", "rolling_date_range": "LAST_7_DAYS"},
    {
        "field": "created_at",
        "range_start": "2026-01-01T00:00:00+00:00",
        "range_end": "2026-02-01T00:00:00Z",
    },
]

RECORD_CASES = [
    Case(
        target="records.create",
        arguments={"record_type_id": 42},
        route=f"POST {RECORDS}",
        body={"record_type_id": 42},
    ),
    Case(
        target="records.create",
        name="false is sent, and a tuple of field values is sent as a list",
        arguments={
            "record_type_id": 42,
            "record_type_name": "alerts",
            "field_values": tuple(FIELD_VALUES),
            "parent_id": 555,
            "test_mode": False,
            "idempotency_key": "once",
        },
        route=f"POST {RECORDS}",
        body={
            "record_type_id": 42,
            "record_type_name": "alerts",
            "field_values": FIELD_VALUES,
            "parent_id": 555,
            "test_mode": False,
        },
    ),
    Case(target="records.get", arguments={"record_id": 555}, route=f"GET {RECORDS}/555"),
    Case(
        target="records.get",
        name="includes, expansions and fields are sent as one comma-separated value each",
        arguments={
            "record_id": 555,
            "record_type_id": 42,
            "include": ("record_type", "child_record_ids", "cases"),
            "expand": ["fields.payload", "fields.log"],
            "fields": ("status", "severity"),
            "timezone": "Europe/Bucharest",
        },
        route=f"GET {RECORDS}/555",
        params={
            "record_type_id": 42,
            "include": "record_type,child_record_ids,cases",
            "expand": "fields.payload,fields.log",
            "fields[record]": "status,severity",
            "timezone": "Europe/Bucharest",
        },
    ),
    Case(
        target="records.get",
        name="empty sequences send nothing",
        arguments={"record_id": 555, "include": [], "expand": [], "fields": []},
        route=f"GET {RECORDS}/555",
    ),
    Case(
        target="records.update",
        arguments={"record_id": 555},
        route=f"PATCH {RECORDS}/555",
        body={},
    ),
    Case(
        target="records.update",
        name="false is sent, and a tuple of field values is sent as a list",
        arguments={
            "record_id": 555,
            "field_values": tuple(FIELD_VALUES),
            "parent_id": 556,
            "test_mode": False,
        },
        route=f"PATCH {RECORDS}/555",
        body={"field_values": FIELD_VALUES, "parent_id": 556, "test_mode": False},
    ),
    Case(
        target="records.update",
        name="an empty list of field values is sent",
        arguments={"record_id": 555, "field_values": [], "parent_id": 556},
        route=f"PATCH {RECORDS}/555",
        body={"field_values": [], "parent_id": 556},
    ),
    Case(target="records.delete", arguments={"record_id": 555}, route=f"DELETE {RECORDS}/555"),
    Case(
        target="records.delete",
        name="false is sent in the query",
        arguments={"record_id": 555, "test_mode": False},
        route=f"DELETE {RECORDS}/555",
        params={"test_mode": False},
    ),
    Case(target="records.search", arguments={}, route=f"POST {RECORDS}/search", body={}),
    Case(
        target="records.search",
        name="datetimes and strings in the time ranges, tuples as lists, and false is sent",
        arguments={
            "record_type_id": 42,
            "record_type_name": "alerts",
            "filter": FILTER,
            "sort": ({"field_name": "Severity", "direction": "DESC"}, {"field_id": 101}),
            "fields": ("status", "severity"),
            "include": ("record_type",),
            "ids": (555, 556),
            "time_range": (
                {"field": "updated_at", "rolling_date_range": "LAST_7_DAYS"},
                {
                    "field": "created_at",
                    "range_start": datetime(2026, 1, 1, tzinfo=UTC),
                    "range_end": "2026-02-01T00:00:00Z",
                },
            ),
            "timezone": "Europe/Bucharest",
            "limit": 50,
            "after": "cursor",
            "include_total": False,
            "test_mode": False,
        },
        route=f"POST {RECORDS}/search",
        body={
            "record_type_id": 42,
            "record_type_name": "alerts",
            "filter": FILTER,
            "sort": [{"field_name": "Severity", "direction": "DESC"}, {"field_id": 101}],
            "fields": {"record": ["status", "severity"]},
            "include": ["record_type"],
            "ids": [555, 556],
            "time_range": TIME_RANGE_WIRE,
            "timezone": "Europe/Bucharest",
            "limit": 50,
            "after": "cursor",
            "include_total": False,
            "test_mode": False,
        },
    ),
    Case(
        target="records.search",
        name="an empty list of fields sends nothing, and an empty list of ids is sent",
        arguments={"fields": [], "ids": []},
        route=f"POST {RECORDS}/search",
        body={"ids": []},
    ),
    Case(
        target="records.aggregate",
        arguments={"aggregations": [{"fn": "COUNT"}]},
        route=f"POST {RECORDS}/aggregate",
        body={"aggregations": [{"fn": "COUNT"}]},
    ),
    Case(
        target="records.aggregate",
        name="every argument is sent, and tuples are sent as lists",
        arguments={
            "aggregations": (
                {"fn": "COUNT", "alias": "total"},
                {"fn": "P95", "field_name": "Duration"},
            ),
            "record_type_id": 42,
            "record_type_name": "alerts",
            "group_by": ({"field_name": "Status"}, {"field_id": 104, "date_trunc": "week"}),
            "filter": FILTER,
            "time_range": (
                {"field": "updated_at", "rolling_date_range": "LAST_7_DAYS"},
                {
                    "field": "created_at",
                    "range_start": datetime(2026, 1, 1, tzinfo=UTC),
                    "range_end": "2026-02-01T00:00:00Z",
                },
            ),
            "order_by": ({"alias": "total", "direction": "DESC"},),
            "parent_ids": (555, 556),
            "timezone": "Europe/Bucharest",
            "limit": 100,
        },
        route=f"POST {RECORDS}/aggregate",
        body={
            "aggregations": [
                {"fn": "COUNT", "alias": "total"},
                {"fn": "P95", "field_name": "Duration"},
            ],
            "record_type_id": 42,
            "record_type_name": "alerts",
            "group_by": [{"field_name": "Status"}, {"field_id": 104, "date_trunc": "week"}],
            "filter": FILTER,
            "time_range": TIME_RANGE_WIRE,
            "order_by": [{"alias": "total", "direction": "DESC"}],
            "parent_ids": [555, 556],
            "timezone": "Europe/Bucharest",
            "limit": 100,
        },
    ),
    Case(
        target="records.list_cases",
        arguments={"record_id": 555},
        route=f"GET {RECORDS}/555/cases",
    ),
    Case(
        target="records.list_cases",
        arguments={"record_id": 555, "timezone": "UTC", "limit": 50, "after": "cursor"},
        route=f"GET {RECORDS}/555/cases",
        params={"timezone": "UTC", "limit": 50, "after": "cursor"},
    ),
    Case(
        target="records.link_case",
        arguments={"record_id": 555, "case_id": 42},
        route=f"POST {RECORDS}/555/cases",
        body={"case_id": 42},
    ),
    Case(
        target="records.unlink_case",
        arguments={"record_id": 555, "case_id": 42},
        route=f"DELETE {RECORDS}/555/cases/42",
    ),
    Case(
        target="records.list_child_record_ids",
        arguments={"record_id": 555},
        route=f"GET {RECORDS}/555/child_record_ids",
    ),
    Case(
        target="records.list_child_record_ids",
        arguments={"record_id": 555, "limit": 50, "after": "cursor"},
        route=f"GET {RECORDS}/555/child_record_ids",
        params={"limit": 50, "after": "cursor"},
    ),
    Case(
        target="records.list_child_records",
        arguments={"record_id": 555},
        route=f"GET {RECORDS}/555/child_records",
    ),
    Case(
        target="records.list_child_records",
        arguments={"record_id": 555, "timezone": "UTC", "limit": 50, "after": "cursor"},
        route=f"GET {RECORDS}/555/child_records",
        params={"timezone": "UTC", "limit": 50, "after": "cursor"},
    ),
]

FIELD_CASES = [
    Case(
        target="records.fields.get",
        name="a field is found by its ID",
        arguments={"record_id": 555, "field": 103},
        route=f"GET {RECORDS}/555/fields/103",
    ),
    Case(
        target="records.fields.get",
        name="a field is found by its slug, and the format is sent",
        arguments={"record_id": 555, "field": "payload", "format": "text"},
        route=f"GET {RECORDS}/555/fields/payload",
        params={"format": "text"},
    ),
    Case(
        target="records.artifacts.get",
        arguments={"record_id": 555, "artifact_id": 7},
        route="GET /api/v1/records/555/artifacts/7",
    ),
]

FIELD_DEFINITIONS = [
    {"name": "Severity", "result_type": "TEXT_ENUM", "fixed_values": ["low", "high"]},
    {"name": "Source", "result_type": "TEXT", "description": "Where it came from"},
    {"name": "Host", "result_type": "TEXT_REGEX", "config": {"regex": "^h-[0-9]+$"}},
]

RECORD_TYPE_CASES = [
    Case(target="records.record_types.list", arguments={}, route="GET /api/v2/record_types"),
    Case(
        target="records.record_types.list",
        arguments={
            "team_id": 7,
            "order": "UPDATED_AT",
            "direction": "DESC",
            "limit": 50,
            "after": "cursor",
        },
        route="GET /api/v2/record_types",
        params={
            "team_id": 7,
            "order": "UPDATED_AT",
            "direction": "DESC",
            "limit": 50,
            "after": "cursor",
        },
    ),
    Case(
        target="records.record_types.get",
        arguments={"record_type_id": 42},
        route="GET /api/v2/record_types/42",
    ),
    Case(
        target="records.record_types.create",
        arguments={"name": "Alerts", "team_id": 7, "fields": [FIELD_DEFINITIONS[1]]},
        route="POST /api/v2/record_types",
        body={"name": "Alerts", "team_id": 7, "fields": [FIELD_DEFINITIONS[1]]},
    ),
    Case(
        target="records.record_types.create",
        name="false is sent, and a tuple of fields is sent as a list",
        arguments={
            "name": "Alerts",
            "team_id": 7,
            "fields": tuple(FIELD_DEFINITIONS),
            "description": "Alerts from outside",
            "editable": False,
            "ttl_days": 0.5,
            "retention_column_name": "UPDATED_AT",
            "on_limit_reached": "EVICT_OLDEST",
            "custom_records_limit": 5000,
        },
        route="POST /api/v2/record_types",
        body={
            "name": "Alerts",
            "team_id": 7,
            "fields": FIELD_DEFINITIONS,
            "description": "Alerts from outside",
            "editable": False,
            "ttl_days": 0.5,
            "retention_column_name": "UPDATED_AT",
            "on_limit_reached": "EVICT_OLDEST",
            "custom_records_limit": 5000,
        },
    ),
    Case(
        target="records.record_types.update",
        arguments={"record_type_id": 42},
        route="PATCH /api/v2/record_types/42",
        body={},
    ),
    Case(
        target="records.record_types.update",
        name="false and an empty list of deletions are sent, and tuples are sent as lists",
        arguments={
            "record_type_id": 42,
            "name": "Alerts",
            "description": "Changed",
            "editable": False,
            "ttl_days": 30,
            "retention_column_name": "CREATED_AT",
            "on_limit_reached": "REJECT",
            "custom_records_limit": 100,
            "fields": (
                {"id": 101, "description": "Alert severity"},
                {"name": "S", "result_type": "TEXT"},
            ),
            "field_ids_to_delete": (102,),
        },
        route="PATCH /api/v2/record_types/42",
        body={
            "name": "Alerts",
            "description": "Changed",
            "editable": False,
            "ttl_days": 30,
            "retention_column_name": "CREATED_AT",
            "on_limit_reached": "REJECT",
            "custom_records_limit": 100,
            "fields": [
                {"id": 101, "description": "Alert severity"},
                {"name": "S", "result_type": "TEXT"},
            ],
            "field_ids_to_delete": [102],
        },
    ),
    Case(
        target="records.record_types.delete",
        arguments={"record_type_id": 42},
        route="DELETE /api/v2/record_types/42",
    ),
]

VIEW_EXPORT = {"schema_version": 1, "export_type": "record_view", "record_view": {"name": "Open"}}

RECORD_VIEW_CASES = [
    Case(target="records.record_views.list", arguments={}, route="GET /api/v1/record_views"),
    Case(
        target="records.record_views.list",
        arguments={
            "team_id": 14,
            "record_type_id": 3,
            "order": "RECENTLY_UPDATED",
            "per_page": 50,
            "page": 2,
        },
        route="GET /api/v1/record_views",
        params={
            "team_id": 14,
            "record_type_id": 3,
            "order": "RECENTLY_UPDATED",
            "per_page": 50,
            "page": 2,
        },
    ),
    Case(
        target="records.record_views.delete",
        arguments={"record_view_id": 9},
        route="DELETE /api/v1/record_views/9",
    ),
    Case(
        target="records.record_views.export",
        arguments={"record_view_id": 9},
        route="GET /api/v1/record_views/9/export",
    ),
    Case(
        target="records.record_views.import_",
        arguments={"team_id": 14, "data": VIEW_EXPORT},
        route="POST /api/v1/record_views/import",
        body={"team_id": 14, "data": VIEW_EXPORT},
    ),
    Case(
        target="records.record_views.import_",
        arguments={"team_id": 14, "data": VIEW_EXPORT, "mode": "replace", "name": "Imported"},
        route="POST /api/v1/record_views/import",
        body={"team_id": 14, "data": VIEW_EXPORT, "mode": "replace", "name": "Imported"},
    ),
]

CASES = [*RECORD_CASES, *FIELD_CASES, *RECORD_TYPE_CASES, *RECORD_VIEW_CASES]


@pytest.mark.parametrize("case", CASES, ids=case_id)
def test_request(tines, router, case):
    assert_sent(tines=tines, router=router, case=case)


def test_every_method_and_argument_has_a_case(tines):
    assert_covers(tines=tines, area="records", cases=CASES)


def test_the_idempotency_key_is_sent_as_a_header_and_not_in_the_body(tines, router):
    route = router.post(RECORDS).mock(return_value=httpx.Response(201, json={}))

    tines.records.create(record_type_id=42, idempotency_key="once")
    tines.records.create(record_type_id=42)

    with_key, without_key = (call.request for call in route.calls)
    assert with_key.headers["idempotency-key"] == "once"
    assert b"once" not in with_key.content
    assert "idempotency-key" not in without_key.headers
