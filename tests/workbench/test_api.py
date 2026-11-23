from datetime import UTC, datetime

import pytest

from tests.support import Case, assert_covers, assert_sent, case_id

GUID = "ca68403e-5594-42a4-bec7-879b0b417a83"

CASES = [
    Case(target="workbench.list", arguments={}, route="GET /api/v1/workbench"),
    Case(
        target="workbench.list",
        name="a datetime and a string are sent as ISO 8601",
        arguments={
            "search": "weather",
            "favorited": True,
            "creator_id": 12,
            "conversation_type": "chat_agent",
            "created_after": datetime(2026, 11, 1, tzinfo=UTC),
            "created_before": "2026-11-22T00:00:00Z",
            "per_page": 50,
            "page": 2,
        },
        route="GET /api/v1/workbench",
        params={
            "search": "weather",
            "favorited": True,
            "creator_id": 12,
            "conversation_type": "chat_agent",
            "created_after": "2026-11-01T00:00:00+00:00",
            "created_before": "2026-11-22T00:00:00Z",
            "per_page": 50,
            "page": 2,
        },
    ),
    Case(
        target="workbench.list",
        name="false is sent, not left out",
        arguments={"favorited": False},
        route="GET /api/v1/workbench",
        params={"favorited": False},
    ),
    Case(
        target="workbench.get",
        arguments={"conversation_id": GUID},
        route=f"GET /api/v1/workbench/{GUID}",
    ),
]


@pytest.mark.parametrize("case", CASES, ids=case_id)
def test_request(tines, router, case):
    assert_sent(tines=tines, router=router, case=case)


def test_every_method_and_argument_has_a_case(tines):
    assert_covers(tines=tines, area="workbench", cases=CASES)
