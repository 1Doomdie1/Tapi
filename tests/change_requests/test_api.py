import pytest

from tests.support import Case, assert_covers, assert_sent, case_id

CASES = [
    Case(target="change_requests.list", arguments={}, route="GET /api/v1/change_requests"),
    Case(
        target="change_requests.list",
        name="a tuple of teams and a list of statuses are sent once per value",
        arguments={
            "team_ids": (3, 4),
            "statuses": ["PENDING", "APPROVED"],
            "per_page": 50,
            "page": 2,
        },
        route="GET /api/v1/change_requests",
        params={
            "team_id[]": [3, 4],
            "status[]": ["PENDING", "APPROVED"],
            "per_page": 50,
            "page": 2,
        },
    ),
    Case(
        target="change_requests.get",
        arguments={"change_request_id": 21},
        route="GET /api/v1/change_requests/21",
    ),
]


@pytest.mark.parametrize("case", CASES, ids=case_id)
def test_request(tines, router, case):
    assert_sent(tines=tines, router=router, case=case)


def test_every_method_and_argument_has_a_case(tines):
    assert_covers(tines=tines, area="change_requests", cases=CASES)
