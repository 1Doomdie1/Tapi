from datetime import UTC, datetime

import pytest

from tests.support import Case, assert_covers, assert_sent, case_id

CASES = [
    Case(target="audit_logs.list", arguments={}, route="GET /api/v1/audit_logs"),
    Case(
        target="audit_logs.list",
        name="a datetime and a string, and a tuple, a list and a range",
        arguments={
            "before": datetime(2026, 11, 22, tzinfo=UTC),
            "after": "2026-11-01T00:00:00Z",
            "user_ids": (1, 2),
            "operation_names": ["StoryItemsMovement", "StoryItemsCreation"],
            "team_ids": range(3, 5),
            "per_page": 100,
            "page": 3,
        },
        route="GET /api/v1/audit_logs",
        params={
            "before": "2026-11-22T00:00:00+00:00",
            "after": "2026-11-01T00:00:00Z",
            "user_id[]": [1, 2],
            "operation_name[]": ["StoryItemsMovement", "StoryItemsCreation"],
            "team_id[]": [3, 4],
            "per_page": 100,
            "page": 3,
        },
    ),
    Case(
        target="audit_logs.list",
        name="empty sequences send nothing",
        arguments={"user_ids": [], "operation_names": [], "team_ids": []},
        route="GET /api/v1/audit_logs",
    ),
]


@pytest.mark.parametrize("case", CASES, ids=case_id)
def test_request(tines, router, case):
    assert_sent(tines=tines, router=router, case=case)


def test_every_method_and_argument_has_a_case(tines):
    assert_covers(tines=tines, area="audit_logs", cases=CASES)
