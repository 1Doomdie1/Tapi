from datetime import UTC, datetime

import pytest

from tests.support import Case, assert_covers, assert_sent, case_id

CASES_PATH = "/api/v2/cases"
CASE = f"{CASES_PATH}/5"
PAGING = {"per_page": 100, "page": 2}

FILTERS = {
    "status": "OPEN",
    "priority": ("HIGH", "LOW"),
    "assignees": [1, "unassigned"],
    "tags": ("a", "b"),
    "assigned_to_me": True,
    "metadata": {"source": "email"},
    "and_fields": ({"key": "owner", "value": "a"},),
    "record_field": {"id": 3, "value": "x"},
    "start_date": datetime(2026, 1, 1, tzinfo=UTC),
    "end_date": "2026-02-01T00:00:00Z",
    "relative_date": "7 days",
    "case_ids": range(1, 3),
}
FILTERS_BODY = {
    **FILTERS,
    "priority": ["HIGH", "LOW"],
    "tags": ["a", "b"],
    "and_fields": [{"key": "owner", "value": "a"}],
    "start_date": "2026-01-01T00:00:00+00:00",
    "case_ids": [1, 2],
}

CREATE = {
    "team_id": 3,
    "name": "Suspicious login",
    "template_id": "phishing-investigation",
    "description": "Reported by <@user-2435>",
    "priority": "HIGH",
    "status": "OPEN",
    "sub_status_id": 7,
    "author_email": "analyst@example.com",
    "assignee_emails": ("a@example.com", "b@example.com"),
    "tag_names": ("phishing",),
    "opened_at": datetime(2026, 1, 1, tzinfo=UTC),
    "resolved_at": "2026-01-02T00:00:00Z",
    "metadata": {"source": "email"},
    "closure_conditions": ({"name": "Has an assignee", "formula": "=SIZE(assignees) > 0"},),
    "field_values": {"12": "high"},
    "tasks": ({"description": "Check the logs", "assignee_ids": (4,)},),
    "blocks": (
        {
            "title": "Notes",
            "block_type": "note",
            "elements": ({"content": "Start here", "note_type": "text", "color": "gold"},),
            "hidden": False,
        },
    ),
}
CREATE_BODY = {
    **CREATE,
    "assignee_emails": ["a@example.com", "b@example.com"],
    "tag_names": ["phishing"],
    "opened_at": "2026-01-01T00:00:00+00:00",
    "closure_conditions": [{"name": "Has an assignee", "formula": "=SIZE(assignees) > 0"}],
    "tasks": [{"description": "Check the logs", "assignee_ids": [4]}],
    "blocks": [
        {
            "title": "Notes",
            "block_type": "note",
            "elements": [{"content": "Start here", "note_type": "text", "color": "gold"}],
            "hidden": False,
        }
    ],
}

UPDATE = {
    "name": "Renamed",
    "team_id": 4,
    "description": "New text",
    "priority": "LOW",
    "status": "CLOSED",
    "sub_status_id": 8,
    "author_email": "analyst@example.com",
    "assignee_emails": ("a@example.com",),
    "add_assignee_emails": ("b@example.com",),
    "remove_assignee_emails": ("c@example.com",),
    "add_tag_names": ("one", "two"),
    "remove_tag_names": ("three",),
    "opened_at": datetime(2026, 1, 1),
    "resolved_at": "2026-01-02T00:00:00Z",
    "closure_conditions": ({"name": "Resolved", "formula": "=TRUE"},),
}
UPDATE_BODY = {
    **UPDATE,
    "assignee_emails": ["a@example.com"],
    "add_assignee_emails": ["b@example.com"],
    "remove_assignee_emails": ["c@example.com"],
    "add_tag_names": ["one", "two"],
    "remove_tag_names": ["three"],
    "opened_at": "2026-01-01T00:00:00+00:00",
    "closure_conditions": [{"name": "Resolved", "formula": "=TRUE"}],
}

SEARCH = {
    "filter": {
        "op": "AND",
        "nodes": [
            {"field": "status", "operator": "IS", "value": "open"},
            {
                "op": "NESTED",
                "path": "task",
                "filter": {"field": "text", "operator": "CONTAINS_ALL", "value": "x"},
            },
        ],
    },
    "sort": ({"field": "created_at", "direction": "DESC"},),
    "page": {"size": 50, "token": "abc"},
    "include_total": True,
    "timezone": "Europe/Dublin",
}

CASE_CASES = [
    Case(target="cases.list", arguments={}, route=f"GET {CASES_PATH}"),
    Case(
        target="cases.list",
        name="filters are sent as a JSON body, with dates and sequences converted",
        arguments={"team_id": 3, "filters": FILTERS, "order": "PRIORITY_DESC", **PAGING},
        route=f"GET {CASES_PATH}",
        params={"team_id": 3, "order": "PRIORITY_DESC", **PAGING},
        body={"filters": FILTERS_BODY},
    ),
    Case(target="cases.get", arguments={"case_id": 5}, route=f"GET {CASE}"),
    Case(
        target="cases.get",
        arguments={"case_id": 5, "resolve_mentions": True},
        route=f"GET {CASE}",
        params={"resolve_mentions": True},
    ),
    Case(
        target="cases.create",
        arguments={"team_id": 3, "name": "Suspicious login"},
        route=f"POST {CASES_PATH}",
        body={"team_id": 3, "name": "Suspicious login"},
    ),
    Case(
        target="cases.create",
        name="tuples are sent as lists and datetimes as ISO 8601",
        arguments=CREATE,
        route=f"POST {CASES_PATH}",
        body=CREATE_BODY,
    ),
    Case(
        target="cases.update",
        name="required arguments send an empty JSON body",
        arguments={"case_id": 5},
        route=f"PATCH {CASE}",
        body={},
    ),
    Case(
        target="cases.update",
        name="a naive datetime is sent as UTC",
        arguments={"case_id": 5, **UPDATE},
        route=f"PATCH {CASE}",
        body=UPDATE_BODY,
    ),
    Case(target="cases.delete", arguments={"case_id": 5}, route=f"DELETE {CASE}"),
    Case(
        target="cases.append_description",
        arguments={"case_id": 5, "description": "More details"},
        route=f"POST {CASE}/description",
        body={"description": "More details"},
    ),
    Case(
        target="cases.search",
        name="required arguments send an empty JSON body",
        arguments={},
        route="POST /api/v3/cases/search",
        body={},
    ),
    Case(
        target="cases.search",
        name="a group with a nested filter, a tuple of sorts and a page token",
        arguments=SEARCH,
        route="POST /api/v3/cases/search",
        body={**SEARCH, "sort": [{"field": "created_at", "direction": "DESC"}]},
    ),
    Case(
        target="cases.bulk_update_fields",
        name="tuples are sent as lists",
        arguments={
            "case_ids": (1, 2),
            "fields": ({"input_id": 4, "value": "x", "upsert": True},),
        },
        route=f"POST {CASES_PATH}/bulk/fields",
        body={"case_ids": [1, 2], "fields": [{"input_id": 4, "value": "x", "upsert": True}]},
    ),
    Case(target="cases.get_pdf", arguments={"case_id": 5}, route=f"GET {CASE}/pdf"),
]

ACTIVITY_CASES = [
    Case(target="cases.activities.list", arguments={"case_id": 5}, route=f"GET {CASE}/activities"),
    Case(
        target="cases.activities.list",
        name="activity types are sent as activity_type[]",
        arguments={
            "case_id": 5,
            "activity_types": ("CREATED", "COMMENTED"),
            **PAGING,
            "resolve_mentions": True,
        },
        route=f"GET {CASE}/activities",
        params={
            "activity_type[]": ["CREATED", "COMMENTED"],
            **PAGING,
            "resolve_mentions": True,
        },
    ),
    Case(
        target="cases.activities.get",
        arguments={"case_id": 5, "activity_id": 9},
        route=f"GET {CASE}/activities/9",
    ),
    Case(
        target="cases.activities.get",
        arguments={"case_id": 5, "activity_id": 9, "resolve_mentions": True},
        route=f"GET {CASE}/activities/9",
        params={"resolve_mentions": True},
    ),
    Case(target="cases.assignees.list", arguments={"case_id": 5}, route=f"GET {CASE}/assignees"),
    Case(
        target="cases.assignees.list",
        arguments={"case_id": 5, **PAGING},
        route=f"GET {CASE}/assignees",
        params=PAGING,
    ),
]

COMMENT_CASES = [
    Case(target="cases.comments.list", arguments={"case_id": 5}, route=f"GET {CASE}/comments"),
    Case(
        target="cases.comments.list",
        arguments={"case_id": 5, **PAGING},
        route=f"GET {CASE}/comments",
        params=PAGING,
    ),
    Case(
        target="cases.comments.get",
        arguments={"case_id": 5, "comment_id": 8},
        route=f"GET {CASE}/comments/8",
    ),
    Case(
        target="cases.comments.create",
        arguments={"case_id": 5, "value": "Looks bad"},
        route=f"POST {CASE}/comments",
        body={"value": "Looks bad"},
    ),
    Case(
        target="cases.comments.create",
        arguments={"case_id": 5, "value": "Looks bad", "author_email": "a@example.com"},
        route=f"POST {CASE}/comments",
        body={"value": "Looks bad", "author_email": "a@example.com"},
    ),
    Case(
        target="cases.comments.update",
        arguments={"case_id": 5, "comment_id": 8, "value": "Looks fine"},
        route=f"PATCH {CASE}/comments/8",
        body={"value": "Looks fine"},
    ),
    Case(
        target="cases.comments.delete",
        arguments={"case_id": 5, "comment_id": 8},
        route=f"DELETE {CASE}/comments/8",
    ),
    Case(
        target="cases.comments.add_reaction",
        arguments={"case_id": 5, "comment_id": 8, "value": "+1"},
        route=f"POST {CASE}/comments/8/reactions",
        body={"value": "+1"},
    ),
    Case(
        target="cases.comments.remove_reaction",
        name="the reaction is sent as the body of a DELETE",
        arguments={"case_id": 5, "comment_id": 8, "value": "eyes"},
        route=f"DELETE {CASE}/comments/8/reactions",
        body={"value": "eyes"},
    ),
]

NOTE = {
    "title": "Findings",
    "content": "# Header",
    "color": "gold",
    "position": 0,
    "sensitive": True,
    "hidden": False,
    "author_email": "a@example.com",
}
NOTE_CASES = [
    Case(target="cases.notes.list", arguments={"case_id": 5}, route=f"GET {CASE}/notes"),
    Case(
        target="cases.notes.list",
        arguments={"case_id": 5, **PAGING, "resolve_mentions": True},
        route=f"GET {CASE}/notes",
        params={**PAGING, "resolve_mentions": True},
    ),
    Case(
        target="cases.notes.get",
        arguments={"case_id": 5, "note_id": 3},
        route=f"GET {CASE}/notes/3",
    ),
    Case(
        target="cases.notes.get",
        arguments={"case_id": 5, "note_id": 3, "resolve_mentions": True},
        route=f"GET {CASE}/notes/3",
        params={"resolve_mentions": True},
    ),
    Case(
        target="cases.notes.create",
        arguments={"case_id": 5, "title": "Findings"},
        route=f"POST {CASE}/notes",
        body={"title": "Findings"},
    ),
    Case(
        target="cases.notes.create",
        name="false is sent, not left out",
        arguments={"case_id": 5, **NOTE},
        route=f"POST {CASE}/notes",
        body=NOTE,
    ),
    Case(
        target="cases.notes.update",
        name="required arguments send an empty JSON body",
        arguments={"case_id": 5, "note_id": 3},
        route=f"PATCH {CASE}/notes/3",
        body={},
    ),
    Case(
        target="cases.notes.update",
        arguments={"case_id": 5, "note_id": 3, **NOTE},
        route=f"PATCH {CASE}/notes/3",
        body=NOTE,
    ),
    Case(
        target="cases.notes.delete",
        arguments={"case_id": 5, "note_id": 3},
        route=f"DELETE {CASE}/notes/3",
    ),
    Case(
        target="cases.notes.append_content",
        arguments={"case_id": 5, "note_id": 3, "content": "More"},
        route=f"POST {CASE}/notes/3/content",
        body={"content": "More"},
    ),
    Case(
        target="cases.notes.append_content",
        arguments={"case_id": 5, "note_id": 3, "content": "More", "author_email": "a@example.com"},
        route=f"POST {CASE}/notes/3/content",
        body={"content": "More", "author_email": "a@example.com"},
    ),
]

TASK_CASES = [
    Case(target="cases.tasks.list", arguments={"case_id": 5}, route=f"GET {CASE}/tasks"),
    Case(
        target="cases.tasks.list",
        arguments={"case_id": 5, **PAGING},
        route=f"GET {CASE}/tasks",
        params=PAGING,
    ),
    Case(
        target="cases.tasks.get",
        arguments={"case_id": 5, "task_id": 2},
        route=f"GET {CASE}/tasks/2",
    ),
    Case(
        target="cases.tasks.create",
        arguments={"case_id": 5, "description": "Check the logs"},
        route=f"POST {CASE}/tasks",
        body={"description": "Check the logs"},
    ),
    Case(
        target="cases.tasks.create",
        name="a tuple of emails is sent as a list",
        arguments={
            "case_id": 5,
            "description": "Check the logs",
            "assignee_emails": ("a@example.com", "b@example.com"),
        },
        route=f"POST {CASE}/tasks",
        body={
            "description": "Check the logs",
            "assignee_emails": ["a@example.com", "b@example.com"],
        },
    ),
    Case(
        target="cases.tasks.batch_create",
        name="a tuple of tasks is sent as a list",
        arguments={
            "case_id": 5,
            "tasks": (
                {"description": "One"},
                {"description": "Two", "assignee_emails": ["a@example.com"]},
            ),
        },
        route=f"POST {CASE}/tasks/batch",
        body={
            "tasks": [
                {"description": "One"},
                {"description": "Two", "assignee_emails": ["a@example.com"]},
            ]
        },
    ),
    Case(
        target="cases.tasks.update",
        name="required arguments send an empty JSON body",
        arguments={"case_id": 5, "task_id": 2},
        route=f"PATCH {CASE}/tasks/2",
        body={},
    ),
    Case(
        target="cases.tasks.update",
        name="false is sent, not left out",
        arguments={
            "case_id": 5,
            "task_id": 2,
            "description": "Done",
            "completed": False,
            "assignee_emails": ("a@example.com",),
        },
        route=f"PATCH {CASE}/tasks/2",
        body={"description": "Done", "completed": False, "assignee_emails": ["a@example.com"]},
    ),
    Case(
        target="cases.tasks.delete",
        arguments={"case_id": 5, "task_id": 2},
        route=f"DELETE {CASE}/tasks/2",
    ),
]

FIELD_VALUE_CASES = [
    Case(target="cases.field_values.list", arguments={"case_id": 5}, route=f"GET {CASE}/fields"),
    Case(
        target="cases.field_values.list",
        arguments={"case_id": 5, **PAGING},
        route=f"GET {CASE}/fields",
        params=PAGING,
    ),
    Case(
        target="cases.field_values.get",
        arguments={"case_id": 5, "field_id": 6},
        route=f"GET {CASE}/fields/6",
    ),
    Case(
        target="cases.field_values.create",
        arguments={"case_id": 5, "input_id": 12, "value": "high"},
        route=f"POST {CASE}/fields",
        body={"input_id": 12, "value": "high"},
    ),
    Case(
        target="cases.field_values.update",
        arguments={"case_id": 5, "field_id": 6, "value": "low|medium"},
        route=f"PATCH {CASE}/fields/6",
        body={"value": "low|medium"},
    ),
    Case(
        target="cases.field_values.delete",
        arguments={"case_id": 5, "field_id": 6},
        route=f"DELETE {CASE}/fields/6",
    ),
]

METADATA_CASES = [
    Case(target="cases.metadata.list", arguments={"case_id": 5}, route=f"GET {CASE}/metadata"),
    Case(
        target="cases.metadata.get",
        arguments={"case_id": 5, "key": "source"},
        route=f"GET {CASE}/metadata/source",
    ),
    Case(
        target="cases.metadata.create",
        arguments={"case_id": 5, "metadata": {"source": "email"}},
        route=f"POST {CASE}/metadata",
        body={"metadata": {"source": "email"}},
    ),
    Case(
        target="cases.metadata.update",
        name="the only verb of the operation is PUT",
        arguments={"case_id": 5, "metadata": {"source": "chat"}},
        route=f"PUT {CASE}/metadata",
        body={"metadata": {"source": "chat"}},
    ),
    Case(
        target="cases.metadata.delete",
        name="the keys are sent as the body of a DELETE",
        arguments={"case_id": 5, "metadata": ("source", "owner")},
        route=f"DELETE {CASE}/metadata",
        body={"metadata": ["source", "owner"]},
    ),
]

FILE_CASES = [
    Case(target="cases.files.list", arguments={"case_id": 5}, route=f"GET {CASE}/files"),
    Case(
        target="cases.files.list",
        arguments={"case_id": 5, **PAGING},
        route=f"GET {CASE}/files",
        params=PAGING,
    ),
    Case(
        target="cases.files.get",
        arguments={"case_id": 5, "file_id": 4},
        route=f"GET {CASE}/files/4",
    ),
    Case(
        target="cases.files.create",
        arguments={"case_id": 5, "filename": "log.txt", "file_contents": "aGVsbG8="},
        route=f"POST {CASE}/files",
        body={"filename": "log.txt", "file_contents": "aGVsbG8="},
    ),
    Case(
        target="cases.files.create",
        arguments={
            "case_id": 5,
            "filename": "log.txt",
            "file_contents": "aGVsbG8=",
            "value": "Attached",
            "author_email": "a@example.com",
            "team_case_block_id": 42,
        },
        route=f"POST {CASE}/files",
        body={
            "filename": "log.txt",
            "file_contents": "aGVsbG8=",
            "value": "Attached",
            "author_email": "a@example.com",
            "team_case_block_id": 42,
        },
    ),
    Case(
        target="cases.files.delete",
        arguments={"case_id": 5, "file_id": 4},
        route=f"DELETE {CASE}/files/4",
    ),
    Case(
        target="cases.files.download",
        arguments={"case_id": 5, "file_id": 4},
        route=f"GET {CASE}/files/4/download",
    ),
    Case(
        target="cases.files.info",
        arguments={"case_id": 5, "file_id": 4},
        route=f"GET {CASE}/files/4/info",
    ),
]

BLOCK = f"{CASE}/blocks/blk_abc"
ELEMENT = f"{CASE}/blocks/12/elements/9"
BLOCK_CASES = [
    Case(target="cases.blocks.list", arguments={"case_id": 5}, route=f"GET {CASE}/blocks"),
    Case(
        target="cases.blocks.list",
        arguments={"case_id": 5, "block_type": "note", "block_group_id": "blk_grp", **PAGING},
        route=f"GET {CASE}/blocks",
        params={"block_type": "note", "block_group_id": "blk_grp", **PAGING},
    ),
    Case(
        target="cases.blocks.get",
        name="a slug can take the place of the ID",
        arguments={"case_id": 5, "block_id": "blk_abc"},
        route=f"GET {BLOCK}",
    ),
    Case(
        target="cases.blocks.create",
        arguments={"case_id": 5, "title": "Notes", "block_type": "note"},
        route=f"POST {CASE}/blocks",
        body={"title": "Notes", "block_type": "note"},
    ),
    Case(
        target="cases.blocks.create",
        name="false is sent, and a tuple of elements is sent as a list",
        arguments={
            "case_id": 5,
            "title": "Notes",
            "block_type": "note",
            "color": "gold",
            "elements": ({"content": "Start", "note_type": "text"},),
            "position": 0,
            "hidden": False,
            "default_collapsed": False,
            "block_group_id": "blk_grp",
            "author_email": "a@example.com",
        },
        route=f"POST {CASE}/blocks",
        body={
            "title": "Notes",
            "block_type": "note",
            "color": "gold",
            "elements": [{"content": "Start", "note_type": "text"}],
            "position": 0,
            "hidden": False,
            "default_collapsed": False,
            "block_group_id": "blk_grp",
            "author_email": "a@example.com",
        },
    ),
    Case(
        target="cases.blocks.update",
        name="required arguments send an empty JSON body",
        arguments={"case_id": 5, "block_id": 12},
        route=f"PATCH {CASE}/blocks/12",
        body={},
    ),
    Case(
        target="cases.blocks.update",
        name="false is sent, not left out",
        arguments={
            "case_id": 5,
            "block_id": "blk_abc",
            "title": "Renamed",
            "color": "primary",
            "position": 2,
            "hidden": False,
            "default_collapsed": False,
            "block_group_id": 7,
        },
        route=f"PATCH {BLOCK}",
        body={
            "title": "Renamed",
            "color": "primary",
            "position": 2,
            "hidden": False,
            "default_collapsed": False,
            "block_group_id": 7,
        },
    ),
    Case(
        target="cases.blocks.delete",
        arguments={"case_id": 5, "block_id": "blk_abc"},
        route=f"DELETE {BLOCK}",
    ),
    Case(
        target="cases.blocks.delete",
        name="false is sent, not left out",
        arguments={"case_id": 5, "block_id": "blk_abc", "include_children": False},
        route=f"DELETE {BLOCK}",
        params={"include_children": False},
    ),
    Case(
        target="cases.blocks.get_element",
        arguments={"case_id": 5, "block_id": 12, "element_id": 9},
        route=f"GET {ELEMENT}",
    ),
    Case(
        target="cases.blocks.update_element",
        name="required arguments send an empty JSON body",
        arguments={"case_id": 5, "block_id": 12, "element_id": 9},
        route=f"PATCH {ELEMENT}",
        body={},
    ),
    Case(
        target="cases.blocks.update_element",
        name="false is sent, not left out",
        arguments={
            "case_id": 5,
            "block_id": 12,
            "element_id": 9,
            "content": "New",
            "sensitive": False,
            "author_email": "a@example.com",
            "annotation": "Note",
        },
        route=f"PATCH {ELEMENT}",
        body={
            "content": "New",
            "sensitive": False,
            "author_email": "a@example.com",
            "annotation": "Note",
        },
    ),
    Case(
        target="cases.blocks.append_element_content",
        arguments={"case_id": 5, "block_id": 12, "element_id": 9, "content": "More"},
        route=f"POST {ELEMENT}/content",
        body={"content": "More"},
    ),
    Case(
        target="cases.blocks.append_element_content",
        arguments={
            "case_id": 5,
            "block_id": 12,
            "element_id": 9,
            "content": "More",
            "author_email": "a@example.com",
        },
        route=f"POST {ELEMENT}/content",
        body={"content": "More", "author_email": "a@example.com"},
    ),
]

LINKED_CASE_CASES = [
    Case(
        target="cases.linked_cases.list",
        arguments={"case_id": 5},
        route=f"GET {CASE}/linked_cases",
    ),
    Case(
        target="cases.linked_cases.list",
        arguments={"case_id": 5, **PAGING},
        route=f"GET {CASE}/linked_cases",
        params=PAGING,
    ),
    Case(
        target="cases.linked_cases.create",
        arguments={"case_id": 5, "id": 6},
        route=f"POST {CASE}/linked_cases",
        body={"id": 6},
    ),
    Case(
        target="cases.linked_cases.batch_create",
        name="a tuple of IDs is sent as a list",
        arguments={"case_id": 5, "ids": (6, 7)},
        route=f"POST {CASE}/linked_cases/batch",
        body={"ids": [6, 7]},
    ),
    Case(
        target="cases.linked_cases.delete",
        arguments={"case_id": 5, "linked_case_id": 6},
        route=f"DELETE {CASE}/linked_cases/6",
    ),
]

RECORD_CASES = [
    Case(target="cases.records.list", arguments={"case_id": 5}, route=f"GET {CASE}/records"),
    Case(
        target="cases.records.list",
        arguments={"case_id": 5, **PAGING},
        route=f"GET {CASE}/records",
        params=PAGING,
    ),
    Case(
        target="cases.records.get",
        arguments={"case_id": 5, "record_id": 3},
        route=f"GET {CASE}/records/3",
    ),
    Case(
        target="cases.records.create",
        arguments={"case_id": 5, "record_id": 3},
        route=f"POST {CASE}/records",
        body={"record_id": 3},
    ),
    Case(
        target="cases.records.delete",
        arguments={"case_id": 5, "record_id": 3},
        route=f"DELETE {CASE}/records/3",
    ),
]

SUBSCRIBER_CASES = [
    Case(
        target="cases.subscribers.list",
        arguments={"case_id": 5},
        route=f"GET {CASE}/subscribers",
    ),
    Case(
        target="cases.subscribers.list",
        arguments={"case_id": 5, **PAGING},
        route=f"GET {CASE}/subscribers",
        params=PAGING,
    ),
    Case(
        target="cases.subscribers.create",
        arguments={"case_id": 5, "user_email": "a@example.com"},
        route=f"POST {CASE}/subscribers",
        body={"user_email": "a@example.com"},
    ),
    Case(
        target="cases.subscribers.batch_create",
        name="a tuple of emails is sent as a list",
        arguments={"case_id": 5, "user_emails": ("a@example.com", "b@example.com")},
        route=f"POST {CASE}/subscribers/batch",
        body={"user_emails": ["a@example.com", "b@example.com"]},
    ),
    Case(
        target="cases.subscribers.delete",
        arguments={"case_id": 5, "subscriber_id": 8},
        route=f"DELETE {CASE}/subscribers/8",
    ),
]

CASE_ACTION = {
    "url": "https://example.com/hook",
    "label": "Notify",
    "action_type": "webhook",
    "action_text": "Send",
    "query_params": {"channel": "soc"},
}
ACTION_CASES = [
    Case(target="cases.actions.list", arguments={"case_id": 5}, route=f"GET {CASE}/actions"),
    Case(
        target="cases.actions.list",
        arguments={"case_id": 5, **PAGING},
        route=f"GET {CASE}/actions",
        params=PAGING,
    ),
    Case(
        target="cases.actions.get",
        arguments={"case_id": 5, "action_id": 2},
        route=f"GET {CASE}/actions/2",
    ),
    Case(
        target="cases.actions.create",
        arguments={
            "case_id": 5,
            "url": "https://example.com/hook",
            "label": "Notify",
            "action_type": "webhook",
        },
        route=f"POST {CASE}/actions",
        body={"url": "https://example.com/hook", "label": "Notify", "action_type": "webhook"},
    ),
    Case(
        target="cases.actions.create",
        arguments={"case_id": 5, **CASE_ACTION},
        route=f"POST {CASE}/actions",
        body=CASE_ACTION,
    ),
    Case(
        target="cases.actions.update",
        name="required arguments send an empty JSON body",
        arguments={"case_id": 5, "action_id": 2},
        route=f"PATCH {CASE}/actions/2",
        body={},
    ),
    Case(
        target="cases.actions.update",
        arguments={"case_id": 5, "action_id": 2, **CASE_ACTION},
        route=f"PATCH {CASE}/actions/2",
        body=CASE_ACTION,
    ),
    Case(
        target="cases.actions.delete",
        arguments={"case_id": 5, "action_id": 2},
        route=f"DELETE {CASE}/actions/2",
    ),
    Case(
        target="cases.actions.batch_update",
        name="the only verb of the operation is PUT, and a tuple is sent as a list",
        arguments={"case_id": 5, "actions": (CASE_ACTION,)},
        route=f"PUT {CASE}/actions/batch",
        body={"actions": [CASE_ACTION]},
    ),
]

FIELD = {
    "name": "Severity",
    "input_type": "string",
    "team_id": 3,
    "sensitive": False,
    "validation_type": "options",
    "validation_options": {"options": ["low", "high"]},
    "group_name": "Triage",
}
FIELD_CASES = [
    Case(target="cases.fields.list", arguments={}, route="GET /api/v1/case_inputs"),
    Case(
        target="cases.fields.list",
        arguments={"team_id": 3, **PAGING},
        route="GET /api/v1/case_inputs",
        params={"team_id": 3, **PAGING},
    ),
    Case(target="cases.fields.get", arguments={"field_id": 4}, route="GET /api/v1/case_inputs/4"),
    Case(
        target="cases.fields.create",
        arguments={"name": "Severity", "input_type": "string", "team_id": 3},
        route="POST /api/v1/case_inputs",
        body={"name": "Severity", "input_type": "string", "team_id": 3},
    ),
    Case(
        target="cases.fields.create",
        name="false is sent, and the options are sent as an object",
        arguments=FIELD,
        route="POST /api/v1/case_inputs",
        body=FIELD,
    ),
    Case(
        target="cases.fields.create",
        name="a pattern is sent as an object with a regex key",
        arguments={
            "name": "Ticket",
            "input_type": "string",
            "team_id": 3,
            "validation_type": "regex",
            "validation_options": {"regex": "^T-[0-9]+$"},
        },
        route="POST /api/v1/case_inputs",
        body={
            "name": "Ticket",
            "input_type": "string",
            "team_id": 3,
            "validation_type": "regex",
            "validation_options": {"regex": "^T-[0-9]+$"},
        },
    ),
    Case(
        target="cases.fields.update",
        name="required arguments send an empty JSON body, to a v2 route",
        arguments={"field_id": 4},
        route="PATCH /api/v2/case_inputs/4",
        body={},
    ),
    Case(
        target="cases.fields.update",
        name="false is sent, not left out",
        arguments={
            "field_id": 4,
            "name": "Renamed",
            "sensitive": False,
            "validation_type": "options",
            "validation_options": {"options": ["a"]},
            "group_name": "Triage",
        },
        route="PATCH /api/v2/case_inputs/4",
        body={
            "name": "Renamed",
            "sensitive": False,
            "validation_type": "options",
            "validation_options": {"options": ["a"]},
            "group_name": "Triage",
        },
    ),
    Case(
        target="cases.fields.delete",
        arguments={"field_id": 4},
        route="DELETE /api/v2/case_inputs/4",
    ),
    Case(
        target="cases.fields.list_values",
        arguments={"field_id": 4},
        route="GET /api/v1/case_inputs/4/fields",
    ),
    Case(
        target="cases.fields.list_values",
        arguments={"field_id": 4, **PAGING},
        route="GET /api/v1/case_inputs/4/fields",
        params=PAGING,
    ),
]

STATUS_PATH = "/api/v1/case_sub_statuses"
STATUS_CASES = [
    Case(
        target="cases.statuses.list",
        arguments={"team_id": 3},
        route=f"GET {STATUS_PATH}",
        params={"team_id": 3},
    ),
    Case(
        target="cases.statuses.list",
        arguments={"team_id": 3, "parent_status": "OPEN", "search": "wait", **PAGING},
        route=f"GET {STATUS_PATH}",
        params={"team_id": 3, "parent_status": "OPEN", "search": "wait", **PAGING},
    ),
    Case(target="cases.statuses.get", arguments={"status_id": 7}, route=f"GET {STATUS_PATH}/7"),
    Case(
        target="cases.statuses.create",
        arguments={"team_id": 3, "name": "Waiting"},
        route=f"POST {STATUS_PATH}",
        body={"team_id": 3, "name": "Waiting"},
    ),
    Case(
        target="cases.statuses.create",
        arguments={
            "team_id": 3,
            "name": "Waiting",
            "parent_status": "OPEN",
            "description": "Waiting for the user",
        },
        route=f"POST {STATUS_PATH}",
        body={
            "team_id": 3,
            "name": "Waiting",
            "parent_status": "OPEN",
            "description": "Waiting for the user",
        },
    ),
    Case(
        target="cases.statuses.update",
        name="required arguments send an empty JSON body",
        arguments={"status_id": 7},
        route=f"PATCH {STATUS_PATH}/7",
        body={},
    ),
    Case(
        target="cases.statuses.update",
        arguments={"status_id": 7, "name": "Blocked", "description": "Blocked by a vendor"},
        route=f"PATCH {STATUS_PATH}/7",
        body={"name": "Blocked", "description": "Blocked by a vendor"},
    ),
    Case(
        target="cases.statuses.delete",
        name="the fallback status goes in the query of a DELETE",
        arguments={"status_id": 7, "fallback_status_id": 8},
        route=f"DELETE {STATUS_PATH}/7",
        params={"fallback_status_id": 8},
    ),
]

TEMPLATE_PATH = "/api/v1/case_templates"
TEMPLATE_OPTIONS = {
    "name": "Phishing: <<email>>",
    "description": "Check the report",
    "status": "OPEN",
    "priority": "HIGH",
    "sub_status_id": 7,
    "assignee_emails": ("a@example.com",),
    "tag_names": ("phishing",),
    "team_case_buttons": (
        {"button_type": "webhook", "url": "https://example.com/hook", "label": "Notify"},
    ),
    "tasks": ({"description": "Check the logs"},),
    "closure_conditions": ({"name": "Resolved", "formula": "=TRUE"},),
    "field_values": {"12": "high"},
    "metadata": {"source": "email"},
}
TEMPLATE_OPTIONS_BODY = {
    **TEMPLATE_OPTIONS,
    "assignee_emails": ["a@example.com"],
    "tag_names": ["phishing"],
    "team_case_buttons": [
        {"button_type": "webhook", "url": "https://example.com/hook", "label": "Notify"}
    ],
    "tasks": [{"description": "Check the logs"}],
    "closure_conditions": [{"name": "Resolved", "formula": "=TRUE"}],
}
TEMPLATE_CASES = [
    Case(
        target="cases.templates.list",
        arguments={"team_id": 3},
        route=f"GET {TEMPLATE_PATH}",
        params={"team_id": 3},
    ),
    Case(
        target="cases.templates.list",
        arguments={"team_id": 3, "search": "phish", **PAGING},
        route=f"GET {TEMPLATE_PATH}",
        params={"team_id": 3, "search": "phish", **PAGING},
    ),
    Case(
        target="cases.templates.get",
        arguments={"template_id": 12},
        route=f"GET {TEMPLATE_PATH}/12",
    ),
    Case(
        target="cases.templates.create",
        arguments={"team_id": 3, "name": "Phishing"},
        route=f"POST {TEMPLATE_PATH}",
        body={"team_id": 3, "name": "Phishing"},
    ),
    Case(
        target="cases.templates.create",
        name="tuples inside the options are sent as lists",
        arguments={
            "team_id": 3,
            "name": "Phishing",
            "emoji": ":mag:",
            "options": TEMPLATE_OPTIONS,
        },
        route=f"POST {TEMPLATE_PATH}",
        body={
            "team_id": 3,
            "name": "Phishing",
            "emoji": ":mag:",
            "options": TEMPLATE_OPTIONS_BODY,
        },
    ),
    Case(
        target="cases.templates.update",
        name="required arguments send an empty JSON body",
        arguments={"template_id": 12},
        route=f"PATCH {TEMPLATE_PATH}/12",
        body={},
    ),
    Case(
        target="cases.templates.update",
        arguments={
            "template_id": 12,
            "name": "Renamed",
            "emoji": ":fire:",
            "options": {"priority": "LOW"},
        },
        route=f"PATCH {TEMPLATE_PATH}/12",
        body={"name": "Renamed", "emoji": ":fire:", "options": {"priority": "LOW"}},
    ),
    Case(
        target="cases.templates.delete",
        arguments={"template_id": 12},
        route=f"DELETE {TEMPLATE_PATH}/12",
    ),
    Case(
        target="cases.templates.export",
        arguments={"template_id": 12},
        route=f"GET {TEMPLATE_PATH}/12/export",
    ),
    Case(
        target="cases.templates.import_",
        arguments={"team_id": 3, "data": {"schema_version": 1, "templates": []}},
        route=f"POST {TEMPLATE_PATH}/import",
        body={"team_id": 3, "data": {"schema_version": 1, "templates": []}},
    ),
    Case(
        target="cases.templates.preview",
        arguments={"template_id": 12},
        route=f"GET {TEMPLATE_PATH}/12/preview",
    ),
]

WEBHOOK_PATH = "/api/v1/case_webhooks"
WEBHOOK_CASES = [
    Case(target="cases.webhooks.list", arguments={}, route=f"GET {WEBHOOK_PATH}"),
    Case(
        target="cases.webhooks.list",
        arguments={"team_id": 3, **PAGING},
        route=f"GET {WEBHOOK_PATH}",
        params={"team_id": 3, **PAGING},
    ),
    Case(
        target="cases.webhooks.get",
        arguments={"webhook_id": 5},
        route=f"GET {WEBHOOK_PATH}/5",
    ),
    Case(
        target="cases.webhooks.create",
        arguments={"team_id": 3, "url": "https://example.com/hook"},
        route=f"POST {WEBHOOK_PATH}",
        body={"team_id": 3, "url": "https://example.com/hook"},
    ),
    Case(
        target="cases.webhooks.create",
        name="a tuple of notifications is sent as a list",
        arguments={
            "team_id": 3,
            "url": "https://example.com/hook",
            "name": "SOC",
            "notifications": ("CREATED", "COMMENTED"),
        },
        route=f"POST {WEBHOOK_PATH}",
        body={
            "team_id": 3,
            "url": "https://example.com/hook",
            "name": "SOC",
            "notifications": ["CREATED", "COMMENTED"],
        },
    ),
    Case(
        target="cases.webhooks.update",
        name="required arguments send an empty JSON body",
        arguments={"webhook_id": 5},
        route=f"PATCH {WEBHOOK_PATH}/5",
        body={},
    ),
    Case(
        target="cases.webhooks.update",
        name="an empty name is sent, not left out",
        arguments={
            "webhook_id": 5,
            "url": "https://example.com/new",
            "name": "",
            "notifications": ["ALL"],
        },
        route=f"PATCH {WEBHOOK_PATH}/5",
        body={"url": "https://example.com/new", "name": "", "notifications": ["ALL"]},
    ),
    Case(
        target="cases.webhooks.delete",
        arguments={"webhook_id": 5},
        route=f"DELETE {WEBHOOK_PATH}/5",
    ),
]

CASES = [
    *CASE_CASES,
    *ACTIVITY_CASES,
    *COMMENT_CASES,
    *NOTE_CASES,
    *TASK_CASES,
    *FIELD_VALUE_CASES,
    *METADATA_CASES,
    *FILE_CASES,
    *BLOCK_CASES,
    *LINKED_CASE_CASES,
    *RECORD_CASES,
    *SUBSCRIBER_CASES,
    *ACTION_CASES,
    *FIELD_CASES,
    *STATUS_CASES,
    *TEMPLATE_CASES,
    *WEBHOOK_CASES,
]


@pytest.mark.parametrize("case", CASES, ids=case_id)
def test_request(tines, router, case):
    assert_sent(tines=tines, router=router, case=case)


def test_every_method_and_argument_has_a_case(tines):
    assert_covers(tines=tines, area="cases", cases=CASES)
