import pytest

from tests.support import Case, assert_covers, assert_sent, case_id

EXPORT = {
    "schema_version": 1,
    "export_type": "dashboard",
    "exported_at": "2026-11-23T10:00:00Z",
    "dashboard": {"name": "Overview", "notes": [], "case_lists": [], "layout": []},
}

CASES = [
    Case(target="dashboards.list", arguments={}, route="GET /api/v1/dashboards"),
    Case(
        target="dashboards.list",
        arguments={"team_id": 3, "order": "RECENTLY_EDITED", "per_page": 50, "page": 2},
        route="GET /api/v1/dashboards",
        params={"team_id": 3, "order": "RECENTLY_EDITED", "per_page": 50, "page": 2},
    ),
    Case(
        target="dashboards.delete",
        arguments={"dashboard_id": 7},
        route="DELETE /api/v1/dashboards/7",
    ),
    Case(
        target="dashboards.export",
        arguments={"dashboard_id": 7},
        route="GET /api/v1/dashboards/7/export",
    ),
    Case(
        target="dashboards.import_",
        arguments={"team_id": 3, "data": EXPORT},
        route="POST /api/v1/dashboards/import",
        body={"team_id": 3, "data": EXPORT},
    ),
    Case(
        target="dashboards.import_",
        arguments={"team_id": 3, "data": EXPORT, "mode": "replace", "new_name": "Overview"},
        route="POST /api/v1/dashboards/import",
        body={"team_id": 3, "data": EXPORT, "mode": "replace", "new_name": "Overview"},
    ),
]


@pytest.mark.parametrize("case", CASES, ids=case_id)
def test_request(tines, router, case):
    assert_sent(tines=tines, router=router, case=case)


def test_every_method_and_argument_has_a_case(tines):
    assert_covers(tines=tines, area="dashboards", cases=CASES)
