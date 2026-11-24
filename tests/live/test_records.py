import time
import uuid
from datetime import UTC, datetime, timedelta
from functools import partial

import pytest

from tests.live.helpers import all_cursor_items, all_items, check, throwaway, wait_until_gone

pytestmark = pytest.mark.writes

FIELDS = [
    {"name": "Status", "result_type": "TEXT_ENUM", "fixed_values": ["open", "closed"]},
    {"name": "Score", "result_type": "NUMBER", "description": "A number."},
    {"name": "Seen", "result_type": "TIMESTAMP"},
    {"name": "Active", "result_type": "BOOLEAN"},
    {"name": "Log", "result_type": "ARTIFACT"},
]


@pytest.fixture
def record_type(live, team_id, cleanup):
    if live.records.record_types.list(limit=1).status_code != 200:
        pytest.skip("the test tenant has no access to records")
    name = throwaway(kind="record-type")
    created = check(
        reply=live.records.record_types.create(
            name=name,
            team_id=team_id,
            fields=FIELDS,
            description="A throwaway record type.",
            editable=True,
            ttl_days=1,
            retention_column_name="UPDATED_AT",
            on_limit_reached="REJECT",
            custom_records_limit=100,
        ),
        status=201,
    )["data"]
    cleanup.add(
        description=f"record type {created['id']}",
        action=partial(live.records.record_types.delete, record_type_id=created["id"]),
    )
    return created


def test_a_record_type_is_created_read_listed_changed_and_deleted(live, team_id, record_type):
    types = live.records.record_types
    type_id = record_type["id"]
    by_name = {field["name"]: field for field in record_type["fields"]}

    assert record_type["description"] == "A throwaway record type."
    assert (record_type["editable"], record_type["ttl_days"]) == (True, 1.0)
    assert record_type["retention_column_name"] == "UPDATED_AT"
    assert (record_type["on_limit_reached"], record_type["custom_records_limit"]) == ("REJECT", 100)
    assert record_type["has_custom_limit"] is True
    assert record_type["relationships"]["team"]["id"] == team_id
    assert {"Status", "Score", "Seen", "Active", "Log"} <= set(by_name)
    assert by_name["Status"]["fixed_values"] == ["open", "closed"]
    assert by_name["Score"]["description"] == "A number."
    assert check(reply=types.get(record_type_id=type_id), status=200)["data"] == record_type
    listed = all_cursor_items(method=types.list, arguments={"team_id": team_id})
    assert type_id in {item["id"] for item in listed}
    newest = check(reply=types.list(order="CREATED_AT", direction="DESC", limit=1), status=200)
    assert len(newest["data"]) == 1

    time.sleep(1.1)
    changed = check(
        reply=types.update(
            record_type_id=type_id,
            description="Changed.",
            ttl_days=3,
            on_limit_reached="EVICT_OLDEST",
            custom_records_limit=200,
            fields=[
                {"id": by_name["Score"]["id"], "description": "Changed number."},
                {"name": "Extra", "result_type": "TEXT"},
            ],
            field_ids_to_delete=[by_name["Seen"]["id"]],
        ),
        status=200,
    )["data"]
    names = {field["name"]: field for field in changed["fields"]}
    assert changed["description"] == "Changed."
    assert (changed["ttl_days"], changed["on_limit_reached"]) == (3.0, "EVICT_OLDEST")
    assert changed["custom_records_limit"] == 200
    assert "Extra" in names
    assert "Seen" not in names
    assert names["Score"]["description"] == "Changed number."
    assert changed["updated_at"] != record_type["updated_at"]

    nothing = types.update(record_type_id=type_id)
    bad_type = types.create(
        name=f"{record_type['name']}-bad",
        team_id=team_id,
        fields=[{"name": "X", "result_type": "BOGUS"}],
    )
    assert nothing.status_code == 400
    assert bad_type.status_code == 422
    assert types.get(record_type_id=999999999).status_code == 404
    assert types.update(record_type_id=999999999, description="x").status_code == 404
    assert types.delete(record_type_id=999999999).status_code == 404
    assert types.list(team_id=999999999).status_code == 404

    check(reply=types.delete(record_type_id=type_id), status=204)
    assert types.get(record_type_id=type_id).status_code == 404


def test_records_are_created_read_searched_changed_linked_and_deleted(
    live, team_id, record_type, cleanup
):
    records = live.records
    type_id = record_type["id"]
    by_name = {field["name"]: field for field in record_type["fields"]}
    key = uuid.uuid4().hex
    started = datetime.now(UTC)

    values = [
        {"field_name": "Status", "value": "open"},
        {"field_name": "Score", "value": 5},
        {"field_name": "Seen", "value": "2026-01-01T00:00:00Z"},
        {"field_id": by_name["Active"]["id"], "value": True},
        {"field_name": "Log", "value": "line one\nline two"},
    ]
    created = check(
        reply=records.create(record_type_id=type_id, field_values=values, idempotency_key=key),
        status=201,
    )
    parent = created["data"]
    parent_id = parent["id"]
    assert parent["relationships"] == {"record_type": {"id": type_id}, "parent_record": None}
    assert (parent["fields"]["status"], parent["fields"]["score"]) == ("open", 5)
    assert parent["fields"]["log"]["expandable"] is True
    assert set(created["field_ids"]) >= {"status", "score", "seen", "active", "log"}

    replay = check(
        reply=records.create(record_type_id=type_id, field_values=values, idempotency_key=key),
        status=201,
    )
    assert replay["data"]["id"] == parent_id
    other_body = records.create(
        record_type_id=type_id,
        field_values=[{"field_name": "Status", "value": "closed"}],
        idempotency_key=key,
    )
    assert other_body.status_code == 422

    child = check(
        reply=records.create(
            record_type_name=record_type["name"],
            field_values=[
                {"field_name": "Status", "value": "closed"},
                {"field_name": "Score", "value": 9},
            ],
            parent_id=parent_id,
            test_mode=False,
        ),
        status=201,
    )["data"]
    child_id = child["id"]
    assert child["relationships"]["parent_record"] == {"id": parent_id}

    full = check(
        reply=records.get(
            record_id=parent_id,
            record_type_id=type_id,
            include=["record_type", "child_record_ids", "cases"],
            expand=["fields.log"],
            fields=["status", "score"],
            timezone="Europe/Bucharest",
        ),
        status=200,
    )
    assert set(full["data"]["fields"]) == {"status", "score"}
    assert full["data"]["relationships"]["child_record_ids"]["ids"] == [child_id]
    assert full["included"]["record_type"][0]["id"] == type_id
    assert records.get(record_id=parent_id, record_type_id=999999999).status_code == 404

    log = check(reply=records.fields.get(record_id=parent_id, field="log"), status=200)
    assert log == "line one\nline two"
    by_id = check(
        reply=records.fields.get(record_id=parent_id, field=by_name["Log"]["id"], format="text"),
        status=200,
    )
    assert by_id == log
    assert records.fields.get(record_id=parent_id, field="status").status_code == 400

    children = check(reply=records.list_child_record_ids(record_id=parent_id, limit=5), status=200)
    assert children["data"] == [child_id]
    child_records = check(reply=records.list_child_records(record_id=parent_id), status=200)
    assert [item["id"] for item in child_records["data"]] == [child_id]

    time.sleep(1.1)
    updated = check(
        reply=records.update(
            record_id=child_id,
            field_values=[
                {"field_name": "Score", "value": 11},
                {"field_name": "Status", "value": None},
            ],
            test_mode=False,
        ),
        status=200,
    )["data"]
    assert updated["fields"]["score"] == 11
    assert updated["fields"]["status"] is None
    assert updated["updated_at"] != child["updated_at"]
    assert records.update(record_id=child_id, field_values=[]).status_code == 400
    assert (
        records.update(record_id=child_id, test_mode=True, parent_id=parent_id).status_code == 422
    )

    found = check(
        reply=records.search(
            record_type_id=type_id,
            filter={
                "op": "AND",
                "nodes": [
                    {"field_name": "Status", "operator": "EQUAL", "value": "open"},
                    {"field_name": "Score", "operator": "GREATER_THAN", "value": 1},
                ],
            },
            sort=[{"field_name": "Score", "direction": "DESC"}],
            fields=["status"],
            include=["record_type"],
            time_range=[{"field": "created_at", "range_start": started - timedelta(minutes=5)}],
            include_total=True,
            limit=10,
        ),
        status=200,
    )
    assert [item["id"] for item in found["data"]] == [parent_id]
    assert found["page"]["total"] == 1
    by_ids = check(
        reply=records.search(record_type_id=type_id, ids=[parent_id, child_id]), status=200
    )
    assert {item["id"] for item in by_ids["data"]} == {parent_id, child_id}
    first_page = check(
        reply=records.search(record_type_id=type_id, limit=1, include_total=True), status=200
    )
    assert first_page["page"]["total"] == 2
    second_page = check(
        reply=records.search(
            record_type_id=type_id, limit=1, after=first_page["page"]["next_page_token"]
        ),
        status=200,
    )
    assert second_page["data"][0]["id"] != first_page["data"][0]["id"]
    assert records.search(record_type_id=type_id, after="bogus").status_code == 400

    totals = check(
        reply=records.aggregate(
            record_type_id=type_id,
            aggregations=[
                {"fn": "COUNT", "alias": "total"},
                {"fn": "SUM", "field_name": "Score", "alias": "points"},
            ],
            group_by=[{"field_name": "Active"}],
            order_by=[{"alias": "total", "direction": "DESC"}],
            limit=10,
        ),
        status=200,
    )
    assert totals["meta"]["row_count"] == len(totals["rows"])
    assert sum(row["total"] for row in totals["rows"]) == 2
    assert records.aggregate(record_type_id=type_id, aggregations=[]).status_code == 400

    case = check(reply=live.cases.create(team_id=team_id, name=throwaway(kind="case")), status=201)
    cleanup.add(
        description=f"case {case['case_id']}",
        action=partial(live.cases.delete, case_id=case["case_id"]),
    )
    check(reply=records.link_case(record_id=parent_id, case_id=case["case_id"]), status=204)
    check(reply=records.link_case(record_id=parent_id, case_id=case["case_id"]), status=204)
    linked = check(reply=records.list_cases(record_id=parent_id), status=200)
    assert [item["id"] for item in linked["data"]] == [case["case_id"]]
    check(reply=records.unlink_case(record_id=parent_id, case_id=case["case_id"]), status=204)
    check(reply=records.unlink_case(record_id=parent_id, case_id=case["case_id"]), status=204)
    assert check(reply=records.list_cases(record_id=parent_id), status=200)["data"] == []

    refused = {
        "a record without a record type": records.create(),
        "a record of a type that does not exist": records.create(record_type_id=999999999),
        "a value that is not valid": records.create(
            record_type_id=type_id, field_values=[{"field_name": "Score", "value": "text"}]
        ),
    }
    assert [reply.status_code for reply in refused.values()] == [400, 404, 422]

    check(reply=records.delete(record_id=child_id, test_mode=False), status=204)
    assert records.get(record_id=child_id).status_code == 404
    assert records.delete(record_id=child_id).status_code == 404
    check(reply=records.delete(record_id=parent_id), status=204)
    assert wait_until_gone(read=partial(records.get, record_id=parent_id)) == 404


def test_a_record_view_is_imported_listed_exported_and_deleted(live, team_id, record_type, cleanup):
    views = live.records.record_views
    view_name = throwaway(kind="record-view")
    element_id = "a1b2c3d4e5f6"
    data = {
        "schema_version": 1,
        "export_type": "record_view",
        "exported_at": "2026-01-01T00:00:00Z",
        "record_view": {
            "name": view_name,
            "report_view": "chart",
            "elements": [
                {
                    "id": element_id,
                    "name": "By status",
                    "record_type_name": record_type["name"],
                    "element_type": "bar_chart",
                    "axes": [{"direction": "X", "record_field_name": "Status"}],
                    "aggregation": "COUNT",
                    "rolling_date_range": "LAST_7_DAYS",
                    "range_start": None,
                    "range_end": None,
                    "filters": {"stories": [], "fields": []},
                    "order": {"field": None, "direction": "DESC"},
                    "color_palette": "colorful",
                    "options": {},
                    "record_fields": [],
                    "test_mode": False,
                }
            ],
            "layout": [{"i": element_id, "h": 4, "w": 6, "x": 0, "y": 0}],
        },
    }

    imported = check(reply=views.import_(team_id=team_id, data=data), status=201)
    view_id = imported["id"]
    cleanup.add(
        description=f"record view {view_id}", action=partial(views.delete, record_view_id=view_id)
    )
    assert (imported["name"], imported["team"]["id"]) == (view_name, team_id)

    listed = all_items(
        method=views.list, key="record_views", arguments={"record_type_id": record_type["id"]}
    )
    ours = [item for item in listed if item["id"] == view_id]
    assert len(ours) == 1
    assert ours[0]["record_type"]["id"] == record_type["id"]
    assert [
        (item["report_view"], item["name"] == record_type["name"])
        for item in listed
        if item["id"] != view_id
    ] == [("split_view", True)]
    newest = check(reply=views.list(order="RECENTLY_CREATED", per_page=1), status=200)
    assert len(newest["record_views"]) == 1

    exported = check(reply=views.export(record_view_id=view_id), status=200)
    assert exported["export_type"] == "record_view"
    assert exported["record_view"]["name"] == view_name
    assert exported["record_view"]["elements"][0]["record_type_name"] == record_type["name"]

    renamed = f"{view_name}-copy"
    copy = check(reply=views.import_(team_id=team_id, data=exported, name=renamed), status=201)
    cleanup.add(
        description=f"record view {copy['id']}",
        action=partial(views.delete, record_view_id=copy["id"]),
    )
    assert copy["name"] == renamed
    replaced = check(
        reply=views.import_(team_id=team_id, data=exported, mode="replace", name=renamed),
        status=201,
    )
    assert replaced["name"] == renamed

    refused = views.import_(team_id=999999999, data=data)
    assert refused.status_code in (400, 404)
    assert views.export(record_view_id=999999999).status_code == 404

    for item_id in {view_id, copy["id"], replaced["id"]}:
        check(reply=views.delete(record_view_id=item_id), status=204)
    assert views.delete(record_view_id=view_id).status_code == 404
