import pytest

from tests.support import Case, assert_covers, assert_sent, case_id

CASES = [
    Case(target="folders.list", arguments={}, route="GET /api/v1/folders"),
    Case(
        target="folders.list",
        arguments={"team_id": 3, "content_type": "STORY", "per_page": 100, "page": 2},
        route="GET /api/v1/folders",
        params={"team_id": 3, "content_type": "STORY", "per_page": 100, "page": 2},
    ),
    Case(target="folders.get", arguments={"folder_id": 4}, route="GET /api/v1/folders/4"),
    Case(
        target="folders.create",
        arguments={"name": "Playbooks", "content_type": "STORY", "team_id": 1},
        route="POST /api/v1/folders",
        body={"name": "Playbooks", "content_type": "STORY", "team_id": 1},
    ),
    Case(
        target="folders.create",
        arguments={
            "name": "Nested",
            "content_type": "RESOURCE",
            "team_id": 1,
            "parent_folder_id": 4,
        },
        route="POST /api/v1/folders",
        body={"name": "Nested", "content_type": "RESOURCE", "team_id": 1, "parent_folder_id": 4},
    ),
    Case(
        target="folders.update",
        arguments={"folder_id": 4, "name": "Renamed"},
        route="PATCH /api/v1/folders/4",
        body={"name": "Renamed"},
    ),
    Case(
        target="folders.update",
        arguments={"folder_id": 4, "name": "Renamed", "parent_folder_id": 7},
        route="PATCH /api/v1/folders/4",
        body={"name": "Renamed", "parent_folder_id": 7},
    ),
    Case(target="folders.delete", arguments={"folder_id": 4}, route="DELETE /api/v1/folders/4"),
]


@pytest.mark.parametrize("case", CASES, ids=case_id)
def test_request(tines, router, case):
    assert_sent(tines=tines, router=router, case=case)


def test_every_method_and_argument_has_a_case(tines):
    assert_covers(tines=tines, area="folders", cases=CASES)
