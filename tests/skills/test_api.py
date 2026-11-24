import pytest

from tests.support import Case, assert_covers, assert_sent, case_id

CASES = [
    Case(target="skills.list", arguments={}, route="GET /api/v1/skills"),
    Case(
        target="skills.list",
        arguments={"team_id": 3, "search": "triage", "per_page": 50, "page": 2},
        route="GET /api/v1/skills",
        params={"team_id": 3, "search": "triage", "per_page": 50, "page": 2},
    ),
    Case(
        target="skills.get",
        name="the team goes in the query",
        arguments={"skill_name": "triage-alerts", "team_id": 3},
        route="GET /api/v1/skills/triage-alerts",
        params={"team_id": 3},
    ),
    Case(
        target="skills.create",
        arguments={
            "team_id": 3,
            "name": "triage-alerts",
            "description": "Triage alerts.",
            "body": "# Triage",
        },
        route="POST /api/v1/skills",
        body={
            "team_id": 3,
            "name": "triage-alerts",
            "description": "Triage alerts.",
            "body": "# Triage",
        },
    ),
    Case(
        target="skills.create",
        arguments={
            "team_id": 3,
            "name": "triage-alerts",
            "description": "Triage alerts.",
            "body": "# Triage",
            "license": "Apache-2.0",
            "compatibility": "Tines 2026",
            "metadata": {"source_repo": "runbooks"},
        },
        route="POST /api/v1/skills",
        body={
            "team_id": 3,
            "name": "triage-alerts",
            "description": "Triage alerts.",
            "body": "# Triage",
            "license": "Apache-2.0",
            "compatibility": "Tines 2026",
            "metadata": {"source_repo": "runbooks"},
        },
    ),
    Case(
        target="skills.update",
        name="the team goes in the body, not in the query",
        arguments={"skill_name": "triage-alerts", "team_id": 3},
        route="PATCH /api/v1/skills/triage-alerts",
        body={"team_id": 3},
    ),
    Case(
        target="skills.update",
        name="an empty metadata object is sent, to clear it",
        arguments={
            "skill_name": "triage-alerts",
            "team_id": 3,
            "name": "triage",
            "description": "New description.",
            "body": "# New",
            "license": "MIT",
            "compatibility": "Any",
            "metadata": {},
        },
        route="PATCH /api/v1/skills/triage-alerts",
        body={
            "team_id": 3,
            "name": "triage",
            "description": "New description.",
            "body": "# New",
            "license": "MIT",
            "compatibility": "Any",
            "metadata": {},
        },
    ),
    Case(
        target="skills.delete",
        name="the team goes in the query",
        arguments={"skill_name": "triage-alerts", "team_id": 3},
        route="DELETE /api/v1/skills/triage-alerts",
        params={"team_id": 3},
    ),
]


@pytest.mark.parametrize("case", CASES, ids=case_id)
def test_request(tines, router, case):
    assert_sent(tines=tines, router=router, case=case)


def test_every_method_and_argument_has_a_case(tines):
    assert_covers(tines=tines, area="skills", cases=CASES)
