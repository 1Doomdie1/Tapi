import pytest

from tests.support import Case, assert_covers, assert_sent, case_id

CASES = [
    Case(target="info.get", arguments={}, route="GET /api/v1/info"),
    Case(target="info.web_stats", arguments={}, route="GET /api/v1/info/web_stats"),
    Case(target="info.worker_stats", arguments={}, route="GET /api/v1/info/worker_stats"),
]


@pytest.mark.parametrize("case", CASES, ids=case_id)
def test_request(tines, router, case):
    assert_sent(tines=tines, router=router, case=case)


def test_every_method_and_argument_has_a_case(tines):
    assert_covers(tines=tines, area="info", cases=CASES)
