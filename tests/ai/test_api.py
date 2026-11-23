from datetime import UTC, datetime

import pytest

from tests.support import Case, assert_covers, assert_sent, case_id

CASES = [
    Case(target="ai.providers.list", arguments={}, route="GET /api/v1/ai_providers"),
    Case(target="ai.usage.get", arguments={}, route="GET /api/v1/ai_usage"),
    Case(
        target="ai.usage.get",
        name="datetimes are sent as ISO 8601 in UTC, and a zero is sent",
        arguments={
            "relative_date": "7 days",
            "start_date": datetime(2026, 1, 1, tzinfo=UTC),
            "end_date": datetime(2026, 2, 1),
            "team_id": 0,
            "model_id": "model-1",
            "provider_id": 5,
            "feature": "ai_agents",
            "story_id": 7,
            "user_id": 8,
            "action_id": 9,
            "group_by": "model",
        },
        route="GET /api/v1/ai_usage",
        params={
            "relative_date": "7 days",
            "start_date": "2026-01-01T00:00:00+00:00",
            "end_date": "2026-02-01T00:00:00+00:00",
            "team_id": 0,
            "model_id": "model-1",
            "provider_id": 5,
            "feature": "ai_agents",
            "story_id": 7,
            "user_id": 8,
            "action_id": 9,
            "group_by": "model",
        },
    ),
]


@pytest.mark.parametrize("case", CASES, ids=case_id)
def test_request(tines, router, case):
    assert_sent(tines=tines, router=router, case=case)


def test_every_method_and_argument_has_a_case(tines):
    assert_covers(tines=tines, area="ai", cases=CASES)
