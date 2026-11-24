from datetime import UTC, datetime

import pytest

from tests.support import Case, assert_covers, assert_sent, case_id

CASES = [
    Case(
        target="reporting.flow_usage",
        arguments={},
        route="GET /api/v1/reporting/flow_usage",
    ),
    Case(
        target="reporting.flow_usage",
        arguments={"per_page": 100, "page": 2},
        route="GET /api/v1/reporting/flow_usage",
        params={"per_page": 100, "page": 2},
    ),
    Case(
        target="reporting.time_saved",
        arguments={},
        route="GET /api/v1/reporting/time_saved",
    ),
    Case(
        target="reporting.time_saved",
        name="a datetime and a string are sent as ISO 8601",
        arguments={
            "start_date": datetime(2026, 11, 1, tzinfo=UTC),
            "end_date": "2026-11-22T00:00:00Z",
            "date_unit": "week",
            "fill_gaps": True,
            "team_id": 3,
            "story_id": 4,
            "action_id": 5,
            "per_page": 50,
            "page": 2,
        },
        route="GET /api/v1/reporting/time_saved",
        params={
            "start_date": "2026-11-01T00:00:00+00:00",
            "end_date": "2026-11-22T00:00:00Z",
            "date_unit": "week",
            "fill_gaps": True,
            "team_id": 3,
            "story_id": 4,
            "action_id": 5,
            "per_page": 50,
            "page": 2,
        },
    ),
    Case(
        target="reporting.time_saved",
        name="false is sent, not left out",
        arguments={"fill_gaps": False},
        route="GET /api/v1/reporting/time_saved",
        params={"fill_gaps": False},
    ),
]


@pytest.mark.parametrize("case", CASES, ids=case_id)
def test_request(tines, router, case):
    assert_sent(tines=tines, router=router, case=case)


def test_every_method_and_argument_has_a_case(tines):
    assert_covers(tines=tines, area="reporting", cases=CASES)
