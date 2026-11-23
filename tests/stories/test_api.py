from datetime import UTC, datetime

import pytest

from tests.support import Case, assert_covers, assert_sent, case_id, wire

STORIES = "/api/v1/stories"
STORY = f"{STORIES}/7981"
ACTIONS = "/api/v1/actions"
ACTION = f"{ACTIONS}/73563"
GUID = "5466f325-0bc6-47fb-943f-41d1a2a8d6ae"

LIST = {
    "team_id": 3,
    "folder_id": 4,
    "search": "phishing",
    "filter": "HIGH_PRIORITY",
    "order": "NAME_DESC",
    "include_live_activity": False,
    "per_page": 100,
    "page": 2,
}
GET = {"story_mode": "TEST", "draft_id": 12, "include_live_activity": True}
CREATE = {
    "team_id": 1,
    "name": "Simple story",
    "description": "About it",
    "keep_events_for": 604800,
    "folder_id": 5,
    "tags": ("a", "b"),
    "disabled": False,
    "priority": False,
}
UPDATE = {
    "name": "Renamed",
    "description": "About it",
    "add_tag_names": ("a", "b"),
    "remove_tag_names": ("c",),
    "keep_events_for": 3600,
    "disabled": False,
    "locked": False,
    "priority": False,
    "webhook_api_enabled": False,
    "api_entry_action_id": 11,
    "api_exit_action_ids": (12, 13),
    "send_to_story_access_source": "STS",
    "entry_action_id": 14,
    "exit_action_ids": (15,),
    "send_to_story_access": "SPECIFIC_TEAMS",
    "shared_team_slugs": ("red", "blue"),
    "send_to_story_skill_use_requires_confirmation": False,
    "team_id": 2,
    "folder_id": 5,
    "change_control_enabled": False,
    "draft_id": 9,
    "monitor_failures": False,
}
IMPORT = {
    "new_name": "Imported story",
    "data": {"name": "Simple story", "agents": [{"type": "Trigger"}]},
    "team_id": 2,
    "folder_id": 5,
    "mode": "versionReplace",
    "draft_name": "My draft",
}
PENDING = {"search": "Process", "story_mode": "LIVE", "draft_id": 12, "per_page": 100, "page": 2}
PAGING = {"per_page": 100, "page": 2}

STORY_CASES = [
    Case(target="stories.list", arguments={}, route=f"GET {STORIES}"),
    Case(
        target="stories.list",
        name="tags are sent as tags[], and false is sent",
        arguments={**LIST, "tags": ("alerts", "phishing")},
        route=f"GET {STORIES}",
        params={**LIST, "tags[]": ["alerts", "phishing"]},
    ),
    Case(target="stories.get", arguments={"story_id": 7981}, route=f"GET {STORY}"),
    Case(
        target="stories.get", arguments={"story_id": 7981, **GET}, route=f"GET {STORY}", params=GET
    ),
    Case(
        target="stories.create",
        arguments={"team_id": 1},
        route=f"POST {STORIES}",
        body={"team_id": 1},
    ),
    Case(
        target="stories.create",
        name="a tuple of tags is sent as a list, and false is sent",
        arguments=CREATE,
        route=f"POST {STORIES}",
        body=wire(arguments=CREATE),
    ),
    Case(
        target="stories.update",
        name="required arguments send an empty JSON body",
        arguments={"story_id": 7981},
        route=f"PATCH {STORY}",
        body={},
    ),
    Case(
        target="stories.update",
        name="tuples are sent as lists, and false is sent",
        arguments={"story_id": 7981, **UPDATE},
        route=f"PATCH {STORY}",
        body=wire(arguments=UPDATE),
    ),
    Case(target="stories.delete", arguments={"story_id": 7981}, route=f"DELETE {STORY}"),
    Case(
        target="stories.batch_delete",
        name="the IDs are sent as a list in the body of a DELETE",
        arguments={"ids": (3, 4, 5)},
        route=f"DELETE {STORIES}/batch",
        body={"ids": [3, 4, 5]},
    ),
    Case(target="stories.export", arguments={"story_id": 7981}, route=f"GET {STORY}/export"),
    Case(
        target="stories.export",
        arguments={
            "story_id": 7981,
            "randomize_urls": True,
            "clear_recipients": True,
            "draft_id": 12,
        },
        route=f"GET {STORY}/export",
        params={"randomize_urls": True, "clear_recipients": True, "draft_id": 12},
    ),
    Case(
        target="stories.import_",
        arguments={key: IMPORT[key] for key in ("new_name", "data", "team_id")},
        route=f"POST {STORIES}/import",
        body={key: IMPORT[key] for key in ("new_name", "data", "team_id")},
    ),
    Case(target="stories.import_", arguments=IMPORT, route=f"POST {STORIES}/import", body=IMPORT),
    Case(target="stories.diagram", arguments={"story_id": 7981}, route=f"GET {STORY}/diagram"),
    Case(
        target="stories.diagram",
        arguments={"story_id": 7981, "format": "svg", "content": "actions", "draft_id": 12},
        route=f"GET {STORY}/diagram",
        params={"format": "svg", "content": "actions", "draft_id": 12},
    ),
    Case(
        target="stories.disable",
        name="false is sent, not left out",
        arguments={"story_id": 7981, "disabled": False},
        route=f"POST {STORY}/disable",
        body={"disabled": False},
    ),
    Case(
        target="stories.list_pending_actions",
        arguments={"story_id": 7981},
        route=f"GET {STORY}/pending_actions",
    ),
    Case(
        target="stories.list_pending_actions",
        arguments={"story_id": 7981, **PENDING},
        route=f"GET {STORY}/pending_actions",
        params=PENDING,
    ),
]

DRAFT_CASES = [
    Case(
        target="stories.drafts.list", arguments={"story_id": 99}, route=f"GET {STORIES}/99/drafts"
    ),
    Case(
        target="stories.drafts.list",
        arguments={"story_id": 99, **PAGING},
        route=f"GET {STORIES}/99/drafts",
        params=PAGING,
    ),
    Case(
        target="stories.drafts.create",
        arguments={"story_id": 99, "name": "My draft"},
        route=f"POST {STORIES}/99/drafts",
        body={"name": "My draft"},
    ),
    Case(
        target="stories.drafts.delete",
        arguments={"story_id": 99, "draft_id": 100},
        route=f"DELETE {STORIES}/99/drafts/100",
    ),
]

OWNER_AND_RECIPIENT_CASES = [
    Case(
        target="stories.owners.add",
        arguments={"story_id": 99, "user_id": 2},
        route=f"POST {STORIES}/99/owners",
        body={"user_id": 2},
    ),
    Case(
        target="stories.owners.remove",
        arguments={"story_id": 99, "user_id": 2},
        route=f"DELETE {STORIES}/99/owners",
        body={"user_id": 2},
    ),
    Case(
        target="stories.recipients.add",
        arguments={"story_id": 99, "address": "alice@example.com"},
        route=f"POST {STORIES}/99/recipients",
        body={"address": "alice@example.com"},
    ),
    Case(
        target="stories.recipients.add",
        arguments={"story_id": 99, "address": "alice@example.com", "draft_id": 12},
        route=f"POST {STORIES}/99/recipients",
        body={"address": "alice@example.com", "draft_id": 12},
    ),
    Case(
        target="stories.recipients.remove",
        arguments={"story_id": 99, "address": "alice@example.com"},
        route=f"DELETE {STORIES}/99/recipients",
        body={"address": "alice@example.com"},
    ),
    Case(
        target="stories.recipients.remove",
        arguments={"story_id": 99, "address": "alice@example.com", "draft_id": 12},
        route=f"DELETE {STORIES}/99/recipients",
        body={"address": "alice@example.com", "draft_id": 12},
    ),
]

RUN_CASES = [
    Case(target="stories.runs.list", arguments={"story_id": 155}, route=f"GET {STORIES}/155/runs"),
    Case(
        target="stories.runs.list",
        name="a datetime and an ISO 8601 string",
        arguments={
            "story_id": 155,
            "story_mode": "TEST",
            "draft_id": 12,
            "since": datetime(2026, 1, 1, tzinfo=UTC),
            "until": "2026-02-01T00:00:00Z",
            **PAGING,
        },
        route=f"GET {STORIES}/155/runs",
        params={
            "story_mode": "TEST",
            "draft_id": 12,
            "since": "2026-01-01T00:00:00+00:00",
            "until": "2026-02-01T00:00:00Z",
            **PAGING,
        },
    ),
    Case(
        target="stories.runs.list_events",
        arguments={"story_id": 155, "story_run_guid": GUID},
        route=f"GET {STORIES}/155/runs/{GUID}",
    ),
    Case(
        target="stories.runs.list_events",
        arguments={
            "story_id": 155,
            "story_run_guid": GUID,
            "story_mode": "LIVE",
            "draft_id": 12,
            **PAGING,
        },
        route=f"GET {STORIES}/155/runs/{GUID}",
        params={"story_mode": "LIVE", "draft_id": 12, **PAGING},
    ),
    Case(
        target="stories.runs.get_summary",
        arguments={"story_id": 155, "story_run_guid": GUID},
        route=f"GET {STORIES}/155/runs/{GUID}/summary",
    ),
    Case(
        target="stories.runs.get_summary",
        arguments={"story_id": 155, "story_run_guid": GUID, "story_mode": "TEST", "draft_id": 12},
        route=f"GET {STORIES}/155/runs/{GUID}/summary",
        params={"story_mode": "TEST", "draft_id": 12},
    ),
    Case(
        target="stories.groups.list_runs",
        arguments={"group_id": 200},
        route="GET /api/v1/groups/200/runs",
    ),
    Case(
        target="stories.groups.list_runs",
        arguments={"group_id": 200, **PAGING},
        route="GET /api/v1/groups/200/runs",
        params=PAGING,
    ),
    Case(
        target="stories.groups.list_run_events",
        arguments={"group_id": 200, "group_run_guid": GUID},
        route=f"GET /api/v1/groups/200/runs/{GUID}",
    ),
    Case(
        target="stories.groups.list_run_events",
        arguments={"group_id": 200, "group_run_guid": GUID, **PAGING},
        route=f"GET /api/v1/groups/200/runs/{GUID}",
        params=PAGING,
    ),
]

VERSION_CASES = [
    Case(
        target="stories.versions.list",
        arguments={"story_id": 99},
        route=f"GET {STORIES}/99/versions",
    ),
    Case(
        target="stories.versions.list",
        arguments={"story_id": 99, "draft_id": 12, **PAGING},
        route=f"GET {STORIES}/99/versions",
        params={"draft_id": 12, **PAGING},
    ),
    Case(
        target="stories.versions.create",
        name="required arguments send an empty JSON body",
        arguments={"story_id": 99},
        route=f"POST {STORIES}/99/versions",
        body={},
    ),
    Case(
        target="stories.versions.create",
        arguments={"story_id": 99, "name": "Test version", "draft_id": 12},
        route=f"POST {STORIES}/99/versions",
        body={"name": "Test version", "draft_id": 12},
    ),
    Case(
        target="stories.versions.get",
        arguments={"story_id": 99, "version_id": 889},
        route=f"GET {STORIES}/99/versions/889",
    ),
    Case(
        target="stories.versions.update",
        arguments={"story_id": 99, "version_id": 889, "name": "Renamed"},
        route=f"POST {STORIES}/99/versions/889",
        body={"name": "Renamed"},
    ),
    Case(
        target="stories.versions.delete",
        arguments={"story_id": 99, "version_id": 889},
        route=f"DELETE {STORIES}/99/versions/889",
    ),
]

CHANGE_REQUEST = f"{STORIES}/154/change_request"
REQUEST_FIELDS = {"change_request_id": 21, "comment": "Add error handling"}
PROMOTE = {
    "change_request_id": 21,
    "bypass_approval": False,
    "bypass_approval_reason": "Break glass",
    "delete_draft": False,
}

CHANGE_CONTROL_CASES = [
    Case(
        target="stories.change_control.create",
        name="required arguments send an empty JSON body",
        arguments={"story_id": 154},
        route=f"POST {CHANGE_REQUEST}",
        body={},
    ),
    Case(
        target="stories.change_control.create",
        arguments={
            "story_id": 154,
            "title": "Change",
            "description": "Mentions <@user-1>",
            "draft_id": 12,
        },
        route=f"POST {CHANGE_REQUEST}",
        body={"title": "Change", "description": "Mentions <@user-1>", "draft_id": 12},
    ),
    Case(
        target="stories.change_control.view",
        arguments={"story_id": 154},
        route=f"GET {CHANGE_REQUEST}/view",
    ),
    Case(
        target="stories.change_control.view",
        arguments={"story_id": 154, "draft_id": 12},
        route=f"GET {CHANGE_REQUEST}/view",
        params={"draft_id": 12},
    ),
    Case(
        target="stories.change_control.generate_description",
        arguments={"story_id": 154, "draft_id": 12},
        route=f"GET {CHANGE_REQUEST}/ai_description",
        params={"draft_id": 12},
    ),
    Case(
        target="stories.change_control.approve",
        arguments={"story_id": 154, "change_request_id": 21},
        route=f"POST {CHANGE_REQUEST}/approve",
        body={"change_request_id": 21},
    ),
    *[
        Case(
            target=f"stories.change_control.{verb}",
            arguments={"story_id": 154, **arguments},
            route=f"POST {CHANGE_REQUEST}/{verb}",
            body=arguments,
        )
        for verb in ("cancel", "reject")
        for arguments in ({"change_request_id": 21}, REQUEST_FIELDS)
    ],
    Case(
        target="stories.change_control.promote",
        arguments={"story_id": 154, "change_request_id": 21},
        route=f"POST {CHANGE_REQUEST}/promote",
        body={"change_request_id": 21},
    ),
    Case(
        target="stories.change_control.promote",
        arguments={"story_id": 154, **PROMOTE},
        route=f"POST {CHANGE_REQUEST}/promote",
        body=PROMOTE,
    ),
]

ACTION_SHARED = {
    "description": "About it",
    "options": {"mode": "extract"},
    "position": {"x": 100, "y": 200},
    "source_ids": (100, 102),
    "links_to_sources": [{"source_id": 10}, {"source_id": 11, "type": "NO_MATCH"}],
    "receiver_ids": (7,),
    "links_to_receivers": [{"receiver_id": 12, "type": "FAILURE"}],
    "schedule": {"cron": "*/5 * * * *", "timezone": "Europe/Dublin"},
    "disabled": False,
    "monitor_failures": False,
    "monitor_all_events": False,
    "monitor_no_events_emitted": 86400,
}
ACTION_CREATE = {
    "type": "Agents::HTTPRequestAgent",
    "name": "Fetch",
    **ACTION_SHARED,
    "story_id": 807,
    "group_id": 5,
    "draft_id": 12345,
}
ACTION_UPDATE = {"name": "Renamed", **ACTION_SHARED, "num_runs_to_save": 25}
ACTION_LIST = {
    "story_id": 807,
    "story_mode": "TEST",
    "team_id": 3,
    "group_id": 5,
    "action_type": "Agents::LLMAgent",
    "draft_id": 12,
    "include_live_activity": False,
    **PAGING,
}
ACTION_EVENTS = {
    "since_id": 10,
    "until_id": 20,
    "since": datetime(2026, 1, 1, tzinfo=UTC),
    "until": "2026-02-01T00:00:00Z",
    "show_reemitted_events_only": False,
    "exclude_previous_event_payloads": False,
    **PAGING,
}

ACTION_CASES = [
    Case(target="stories.actions.list", arguments={}, route=f"GET {ACTIONS}"),
    Case(
        target="stories.actions.list",
        arguments=ACTION_LIST,
        route=f"GET {ACTIONS}",
        params=ACTION_LIST,
    ),
    Case(target="stories.actions.get", arguments={"action_id": 73563}, route=f"GET {ACTION}"),
    Case(
        target="stories.actions.get",
        arguments={"action_id": 73563, "include_live_activity": True},
        route=f"GET {ACTION}",
        params={"include_live_activity": True},
    ),
    Case(
        target="stories.actions.create",
        arguments={"type": "Agents::HTTPRequestAgent", "name": "Fetch"},
        route=f"POST {ACTIONS}",
        body={"type": "Agents::HTTPRequestAgent", "name": "Fetch"},
    ),
    Case(
        target="stories.actions.create",
        name="tuples are sent as lists, and a single schedule stays an object",
        arguments=ACTION_CREATE,
        route=f"POST {ACTIONS}",
        body=wire(arguments=ACTION_CREATE),
    ),
    Case(
        target="stories.actions.update",
        name="required arguments send an empty JSON body",
        arguments={"action_id": 73563},
        route=f"PATCH {ACTION}",
        body={},
    ),
    Case(
        target="stories.actions.update",
        name="tuples are sent as lists, and a single schedule stays an object",
        arguments={"action_id": 73563, **ACTION_UPDATE},
        route=f"PATCH {ACTION}",
        body=wire(arguments=ACTION_UPDATE),
    ),
    Case(
        target="stories.actions.update",
        name="a sequence of schedules is sent as a list",
        arguments={
            "action_id": 73563,
            "schedule": ({"cron": "0 0 1 1 *", "timezone": "Europe/Dublin"},),
        },
        route=f"PATCH {ACTION}",
        body={"schedule": [{"cron": "0 0 1 1 *", "timezone": "Europe/Dublin"}]},
    ),
    Case(target="stories.actions.delete", arguments={"action_id": 73563}, route=f"DELETE {ACTION}"),
    Case(
        target="stories.actions.list_events",
        arguments={"action_id": 73563},
        route=f"GET {ACTION}/events",
    ),
    Case(
        target="stories.actions.list_events",
        name="a datetime and an ISO 8601 string, and false is sent",
        arguments={"action_id": 73563, **ACTION_EVENTS},
        route=f"GET {ACTION}/events",
        params={**ACTION_EVENTS, "since": "2026-01-01T00:00:00+00:00"},
    ),
    Case(
        target="stories.actions.list_logs",
        arguments={"action_id": 73563},
        route=f"GET {ACTION}/logs",
    ),
    Case(
        target="stories.actions.list_logs",
        name="levels are sent as level[]",
        arguments={"action_id": 73563, "levels": (2, 4), **PAGING},
        route=f"GET {ACTION}/logs",
        params={"level[]": [2, 4], **PAGING},
    ),
    Case(
        target="stories.actions.delete_events",
        arguments={"action_id": 73563},
        route=f"DELETE {ACTION}/remove_events",
    ),
    Case(
        target="stories.actions.delete_events",
        name="false is sent, not left out",
        arguments={"action_id": 73563, "async_deletion": False},
        route=f"DELETE {ACTION}/remove_events",
        params={"async_deletion": False},
    ),
    Case(
        target="stories.actions.delete_logs",
        arguments={"action_id": 73563},
        route=f"DELETE {ACTION}/remove_logs",
    ),
    Case(
        target="stories.actions.clear_memory",
        arguments={"action_id": 73563},
        route=f"DELETE {ACTION}/clear_memory",
    ),
]

EVENTS = "/api/v1/events"
EVENT_LIST = {
    "team_id": 3,
    "story_id": 807,
    "agent_id": 73563,
    "story_mode": "test",
    "include_groups": False,
    "since_id": 10,
    "until_id": 20,
    "show_reemitted_events_only": False,
    "exclude_previous_event_payloads": False,
    **PAGING,
}

EVENT_CASES = [
    Case(target="stories.events.list", arguments={}, route=f"GET {EVENTS}"),
    Case(
        target="stories.events.list",
        name="a datetime and an ISO 8601 string, and false is sent",
        arguments={
            **EVENT_LIST,
            "since": datetime(2026, 1, 1, tzinfo=UTC),
            "until": "2026-02-01T00:00:00Z",
        },
        route=f"GET {EVENTS}",
        params={
            **EVENT_LIST,
            "since": "2026-01-01T00:00:00+00:00",
            "until": "2026-02-01T00:00:00Z",
        },
    ),
    Case(
        target="stories.events.get",
        arguments={"event_id": 1785421735},
        route=f"GET {EVENTS}/1785421735",
    ),
    Case(
        target="stories.events.get",
        arguments={"event_id": 1785421735, "exclude_previous_event_payloads": True},
        route=f"GET {EVENTS}/1785421735",
        params={"exclude_previous_event_payloads": True},
    ),
    Case(
        target="stories.events.reemit",
        arguments={"event_id": 1785421735},
        route=f"POST {EVENTS}/1785421735/reemit",
    ),
]

LINK_CASES = [
    Case(
        target="stories.links.delete",
        name="a tuple of links is sent as a list of objects",
        arguments={
            "links": (
                {"source_id": 123, "receiver_id": 456},
                {"source_id": 456, "receiver_id": 789},
            )
        },
        route="DELETE /api/v1/links",
        body={
            "links": [
                {"source_id": 123, "receiver_id": 456},
                {"source_id": 456, "receiver_id": 789},
            ]
        },
    ),
]

NOTES = "/api/v1/notes"
NOTE = f"{NOTES}/21405"
NOTE_LIST = {"story_id": 813, "mode": "LIVE", "team_id": 3, "group_id": 5, "draft_id": 12, **PAGING}

NOTE_CASES = [
    Case(target="stories.notes.list", arguments={}, route=f"GET {NOTES}"),
    Case(target="stories.notes.list", arguments=NOTE_LIST, route=f"GET {NOTES}", params=NOTE_LIST),
    Case(target="stories.notes.get", arguments={"note_id": 21405}, route=f"GET {NOTE}"),
    Case(
        target="stories.notes.create",
        name="a story and a group are not required by tapi",
        arguments={"content": "# Header"},
        route=f"POST {NOTES}",
        body={"content": "# Header"},
    ),
    Case(
        target="stories.notes.create",
        arguments={
            "story_id": 813,
            "group_id": 5,
            "content": "# Header\n - item 1",
            "position": {"x": 0, "y": 10},
            "draft_id": 12,
        },
        route=f"POST {NOTES}",
        body={
            "story_id": 813,
            "group_id": 5,
            "content": "# Header\n - item 1",
            "position": {"x": 0, "y": 10},
            "draft_id": 12,
        },
    ),
    Case(
        target="stories.notes.update",
        name="required arguments send an empty JSON body",
        arguments={"note_id": 21405},
        route=f"PATCH {NOTE}",
        body={},
    ),
    Case(
        target="stories.notes.update",
        arguments={"note_id": 21405, "content": "# Header", "position": {"x": 10, "y": 10}},
        route=f"PATCH {NOTE}",
        body={"content": "# Header", "position": {"x": 10, "y": 10}},
    ),
    Case(target="stories.notes.delete", arguments={"note_id": 21405}, route=f"DELETE {NOTE}"),
]

CASES = [
    *STORY_CASES,
    *EVENT_CASES,
    *LINK_CASES,
    *NOTE_CASES,
    *DRAFT_CASES,
    *OWNER_AND_RECIPIENT_CASES,
    *RUN_CASES,
    *VERSION_CASES,
    *CHANGE_CONTROL_CASES,
    *ACTION_CASES,
]


@pytest.mark.parametrize("case", CASES, ids=case_id)
def test_request(tines, router, case):
    assert_sent(tines=tines, router=router, case=case)


def test_every_method_and_argument_has_a_case(tines):
    assert_covers(tines=tines, area="stories", cases=CASES)
