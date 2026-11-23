import pytest

from tapi import Response
from tests.live.helpers import check
from tests.support import resolve

PLAN_DEPENDENT = {
    "info.web_stats",
    "info.worker_stats",
    "ai.providers.list",
    "ai.usage.get",
    "audit_logs.list",
    "apps.list",
    "apps.get",
}
UNAVAILABLE = (402, 403, 404, 422)

LISTS = [
    pytest.param("info.get", {}, "stack", False, id="info.get"),
    pytest.param("info.web_stats", {}, None, False, id="info.web_stats"),
    pytest.param("info.worker_stats", {}, None, False, id="info.worker_stats"),
    pytest.param("ai.providers.list", {}, "ai_providers", False, id="ai.providers.list"),
    pytest.param("ai.usage.get", {}, None, False, id="ai.usage.get"),
    pytest.param("audit_logs.list", {"per_page": 1}, "audit_logs", True, id="audit_logs.list"),
    pytest.param("credentials.list", {"per_page": 1}, "user_credentials", True, id="credentials"),
    pytest.param("folders.list", {"per_page": 1}, "folders", True, id="folders.list"),
    pytest.param("resources.list", {"per_page": 1}, "global_resources", True, id="resources"),
    pytest.param("tags.list", {"per_page": 1}, "tags", True, id="tags.list"),
    pytest.param("teams.list", {"per_page": 1}, "teams", True, id="teams.list"),
    pytest.param("apps.list", {"per_page": 1}, "apps", True, id="apps.list"),
    pytest.param("cases.list", {"per_page": 1}, "cases", True, id="cases.list"),
    pytest.param(
        "change_requests.list",
        {"per_page": 1},
        "change_requests",
        True,
        id="change_requests.list",
    ),
    pytest.param("workbench.list", {"per_page": 1}, "conversations", True, id="workbench.list"),
    pytest.param("cases.fields.list", {"per_page": 1}, "case_inputs", True, id="fields.list"),
    pytest.param("cases.webhooks.list", {"per_page": 1}, "webhooks", True, id="webhooks.list"),
    pytest.param("stories.list", {"per_page": 1}, "stories", True, id="stories.list"),
    pytest.param("stories.actions.list", {"per_page": 1}, "agents", True, id="actions.list"),
    pytest.param("stories.events.list", {"per_page": 1}, "events", True, id="events.list"),
    pytest.param("stories.notes.list", {"per_page": 1}, "annotations", True, id="notes.list"),
]

FIRST_ITEMS = [
    pytest.param("tags.list", "tags", "tags.get", "tag_id", True, id="tags"),
    pytest.param("folders.list", "folders", "folders.get", "folder_id", True, id="folders"),
    pytest.param(
        "resources.list", "global_resources", "resources.get", "resource_id", True, id="resources"
    ),
    pytest.param(
        "credentials.list",
        "user_credentials",
        "credentials.get",
        "credential_id",
        True,
        id="credentials",
    ),
    pytest.param("teams.list", "teams", "teams.get", "team_id", True, id="teams"),
    pytest.param("apps.list", "apps", "apps.get", "app_id", False, id="apps"),
    pytest.param("stories.list", "stories", "stories.get", "story_id", True, id="stories"),
    pytest.param(
        "stories.actions.list", "agents", "stories.actions.get", "action_id", True, id="actions"
    ),
    pytest.param(
        "stories.notes.list", "annotations", "stories.notes.get", "note_id", True, id="notes"
    ),
    pytest.param(
        "stories.events.list", "events", "stories.events.get", "event_id", True, id="events"
    ),
    pytest.param(
        "change_requests.list",
        "change_requests",
        "change_requests.get",
        "change_request_id",
        True,
        id="change_requests",
    ),
    pytest.param(
        "cases.fields.list", "case_inputs", "cases.fields.get", "field_id", True, id="fields"
    ),
    pytest.param(
        "cases.webhooks.list", "webhooks", "cases.webhooks.get", "webhook_id", False, id="webhooks"
    ),
]

STORY_READS = [
    pytest.param("stories.versions.list", "story_versions", id="versions.list"),
    pytest.param("stories.runs.list", "story_runs", id="runs.list"),
    pytest.param("stories.list_pending_actions", "pending_actions", id="list_pending_actions"),
    pytest.param("stories.export", None, id="export"),
]


def skip_when_unavailable(*, target: str, reply: Response) -> None:
    if target in PLAN_DEPENDENT and reply.status_code in UNAVAILABLE:
        pytest.skip(f"{target} is not available on this tenant ({reply.status_code})")


@pytest.mark.parametrize(("target", "arguments", "key", "paginated"), LISTS)
def test_a_read_answers_with_its_documented_shape(live, target, arguments, key, paginated):
    reply = resolve(tines=live, target=target)(**arguments)
    skip_when_unavailable(target=target, reply=reply)

    data = check(reply=reply, status=200)

    assert isinstance(data, dict)
    if key is not None:
        assert key in data
    if paginated:
        assert isinstance(data[key], list)
        assert "next_page_number" in data["meta"]


@pytest.mark.parametrize(
    ("list_target", "key", "get_target", "id_parameter", "has_id"), FIRST_ITEMS
)
def test_the_first_item_of_a_list_can_be_read_by_its_id(
    live, list_target, key, get_target, id_parameter, has_id
):
    listed = resolve(tines=live, target=list_target)(per_page=1)
    skip_when_unavailable(target=get_target, reply=listed)
    items = check(reply=listed, status=200)[key]
    if not items:
        pytest.skip(f"{list_target} is empty on this tenant")

    reply = resolve(tines=live, target=get_target)(**{id_parameter: items[0]["id"]})
    skip_when_unavailable(target=get_target, reply=reply)
    data = check(reply=reply, status=200)

    assert isinstance(data, dict)
    if has_id:
        assert data["id"] == items[0]["id"]


@pytest.fixture(scope="module")
def story_id(live):
    stories = check(reply=live.stories.list(per_page=1), status=200)["stories"]
    if not stories:
        pytest.skip("the test tenant has no stories")
    return stories[0]["id"]


@pytest.mark.parametrize(("target", "key"), STORY_READS)
def test_the_reads_of_a_story_answer_with_their_documented_shape(live, story_id, target, key):
    data = check(reply=resolve(tines=live, target=target)(story_id=story_id), status=200)

    assert isinstance(data, dict)
    if key is not None:
        assert isinstance(data[key], list)


def test_search_answers_with_a_page_of_cases(live):
    reply = live.cases.search(page={"size": 1}, include_total=True)

    data = check(reply=reply, status=200)

    assert isinstance(data["cases"], list)
    assert isinstance(data["total"], int)


@pytest.fixture(scope="module")
def case_id(live):
    cases = check(reply=live.cases.list(per_page=1), status=200)["cases"]
    if not cases:
        pytest.skip("the test tenant has no cases")
    return cases[0]["case_id"]


def test_the_first_case_can_be_read_by_its_id(live, case_id):
    data = check(reply=live.cases.get(case_id=case_id), status=200)

    assert data["case_id"] == case_id


@pytest.mark.parametrize(
    ("target", "key"),
    [
        pytest.param("cases.activities.list", "activities", id="activities.list"),
        pytest.param("cases.assignees.list", "assignees", id="assignees.list"),
    ],
)
def test_the_reads_of_a_case_answer_with_their_documented_shape(live, case_id, target, key):
    data = check(reply=resolve(tines=live, target=target)(case_id=case_id), status=200)

    assert isinstance(data[key], list)
    assert "next_page_number" in data["meta"]


@pytest.mark.parametrize(
    ("list_target", "key", "get_target", "id_parameter"),
    [
        pytest.param(
            "cases.statuses.list",
            "case_sub_statuses",
            "cases.statuses.get",
            "status_id",
            id="statuses",
        ),
        pytest.param(
            "cases.templates.list",
            "case_templates",
            "cases.templates.get",
            "template_id",
            id="templates",
        ),
    ],
)
def test_the_first_status_or_template_of_a_team_can_be_read_by_its_id(
    live, team_id, list_target, key, get_target, id_parameter
):
    listed = resolve(tines=live, target=list_target)(team_id=team_id, per_page=1)
    items = check(reply=listed, status=200)[key]
    if not items:
        pytest.skip(f"{list_target} is empty on this tenant")

    data = check(
        reply=resolve(tines=live, target=get_target)(**{id_parameter: items[0]["id"]}), status=200
    )

    assert data["id"] == items[0]["id"]


def test_change_requests_report_what_is_not_found_or_not_valid(live):
    unknown_team = live.change_requests.list(team_ids=[999999999])
    bad_status = live.change_requests.list(statuses=["BOGUS"])
    unknown_id = live.change_requests.get(change_request_id=999999999)

    assert (unknown_team.status_code, unknown_id.status_code) == (404, 404)
    assert unknown_id.data == ["StoryChangeRequest not found"]
    assert bad_status.status_code == 422
    assert "PENDING" in str(bad_status.data)


def test_the_first_conversation_can_be_read_by_its_guid(live):
    listed = check(reply=live.workbench.list(per_page=1), status=200)["conversations"]
    if not listed:
        pytest.skip("the test tenant has no workbench conversations")

    data = check(reply=live.workbench.get(conversation_id=listed[0]["guid"]), status=200)

    assert data["guid"] == listed[0]["guid"]
    assert {"status", "usage", "steps"} <= set(data)
    assert isinstance(data["steps"], list)
    assert {step["role"] for step in data["steps"]} <= {"user", "assistant", "tool"}


def test_workbench_reports_what_is_not_found_or_not_valid(live):
    unknown = live.workbench.get(conversation_id="00000000-0000-0000-0000-000000000000")
    bad_type = live.workbench.list(conversation_type="bogus")
    bad_range = live.workbench.list(
        created_after="2026-11-22T00:00:00Z", created_before="2020-01-01T00:00:00Z"
    )

    assert (unknown.status_code, unknown.data) == (404, ["Conversation not found"])
    assert (bad_type.status_code, bad_range.status_code) == (400, 400)
    assert bad_range.data == ["created_after must be before created_before"]


def test_the_members_of_a_team_can_be_listed(live, team_id):
    data = check(reply=live.teams.members.list(team_id=team_id), status=200)

    assert isinstance(data["members"], list)
    assert "next_page_number" in data["meta"]
