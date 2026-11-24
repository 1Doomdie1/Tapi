import pytest

from tests.support import Case, assert_covers, assert_sent, case_id

FILES = ({"path": "App.tsx", "contents": "export default () => null;"}, {"path": "empty.txt"})

CASES = [
    Case(target="apps.list", arguments={}, route="GET /api/v1/apps"),
    Case(
        target="apps.list",
        arguments={"per_page": 100, "page": 2},
        route="GET /api/v1/apps",
        params={"per_page": 100, "page": 2},
    ),
    Case(target="apps.get", arguments={"app_id": 42}, route="GET /api/v1/apps/42"),
    Case(
        target="apps.create",
        arguments={"team_id": 1},
        route="POST /api/v1/apps",
        body={"team_id": 1},
    ),
    Case(
        target="apps.create",
        arguments={"team_id": 1, "name": "Tracker", "description": "An app"},
        route="POST /api/v1/apps",
        body={"team_id": 1, "name": "Tracker", "description": "An app"},
    ),
    Case(target="apps.delete", arguments={"app_id": 42}, route="DELETE /api/v1/apps/42"),
    Case(target="apps.export", arguments={"app_id": 42}, route="GET /api/v1/apps/42/export"),
    Case(
        target="apps.export",
        arguments={"app_id": 42, "version_id": 7},
        route="GET /api/v1/apps/42/export",
        params={"version_id": 7},
    ),
    Case(
        target="apps.replace_files",
        name="a tuple of files is sent as a list",
        arguments={"app_id": 42, "files": FILES},
        route="PUT /api/v1/apps/42/files",
        body={"files": list(FILES)},
    ),
    Case(
        target="apps.publish",
        name="required arguments send an empty JSON body",
        arguments={"app_id": 42},
        route="POST /api/v1/apps/42/publish",
        body={},
    ),
    Case(
        target="apps.publish",
        arguments={"app_id": 42, "name": "v1", "description": "First release"},
        route="POST /api/v1/apps/42/publish",
        body={"name": "v1", "description": "First release"},
    ),
]


@pytest.mark.parametrize("case", CASES, ids=case_id)
def test_request(tines, router, case):
    assert_sent(tines=tines, router=router, case=case)


def test_every_method_and_argument_has_a_case(tines):
    assert_covers(tines=tines, area="apps", cases=CASES)
