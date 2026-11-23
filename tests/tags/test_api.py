import pytest

from tests.support import Case, assert_covers, assert_sent, case_id

CASES = [
    Case(target="tags.list", arguments={}, route="GET /api/v1/tags"),
    Case(
        target="tags.list",
        arguments={"team_id": 3, "per_page": 100, "page": 2},
        route="GET /api/v1/tags",
        params={"team_id": 3, "per_page": 100, "page": 2},
    ),
    Case(target="tags.get", arguments={"tag_id": 17}, route="GET /api/v1/tags/17"),
    Case(
        target="tags.create",
        arguments={"name": "priority-high", "team_id": 1, "color": "red"},
        route="POST /api/v1/tags",
        body={"name": "priority-high", "team_id": 1, "color": "red"},
    ),
    Case(
        target="tags.update",
        name="required arguments send an empty JSON body",
        arguments={"tag_id": 17},
        route="PATCH /api/v1/tags/17",
        body={},
    ),
    Case(
        target="tags.update",
        arguments={"tag_id": 17, "name": "priority-critical", "color": "#9B61FF"},
        route="PATCH /api/v1/tags/17",
        body={"name": "priority-critical", "color": "#9B61FF"},
    ),
    Case(target="tags.delete", arguments={"tag_id": 17}, route="DELETE /api/v1/tags/17"),
    Case(
        target="tags.delete",
        name="team_id is sent in the query, not in the body",
        arguments={"tag_id": 17, "team_id": 5},
        route="DELETE /api/v1/tags/17",
        params={"team_id": 5},
    ),
]


@pytest.mark.parametrize("case", CASES, ids=case_id)
def test_request(tines, router, case):
    assert_sent(tines=tines, router=router, case=case)


def test_every_method_and_argument_has_a_case(tines):
    assert_covers(tines=tines, area="tags", cases=CASES)
