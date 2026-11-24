import base64

import pytest

from tests.live.helpers import all_items, check, throwaway, wait_for, wait_until_gone

pytestmark = pytest.mark.writes

ALWAYS = [{"name": "Always true", "formula": "=TRUE"}]
NEEDS_AN_ASSIGNEE = [{"name": "Has an assignee", "formula": "=SIZE(team_case.assignees) > 0"}]


@pytest.fixture
def case(live, team_id, cleanup):
    created = check(
        reply=live.cases.create(
            team_id=team_id,
            name=throwaway(kind="case"),
            description="First line",
            priority="high",
            status="open",
            metadata={"source": "live-check"},
            closure_conditions=ALWAYS,
            tasks=[{"description": "Check the logs"}],
        ),
        status=201,
    )
    cleanup.add(
        description=f"case {created['case_id']}",
        action=lambda: live.cases.delete(case_id=created["case_id"]),
    )
    return created


def test_a_case_is_created_read_listed_updated_closed_and_deleted(live, team_id, case):
    case_id = case["case_id"]

    assert case["priority"] == "HIGH"
    assert case["status"] == "OPEN"
    assert case["description"] == "First line"
    assert case["metadata"] == {"source": "live-check"}
    assert len(case["closure_conditions"]) == 1
    assert len(case["tasks"]) == 1
    fetched = check(reply=live.cases.get(case_id=case_id), status=200)
    assert fetched["case_id"] == case_id
    assert set(fetched) == set(case)
    listed = all_items(method=live.cases.list, key="cases", arguments={"team_id": team_id})
    assert case_id in [item["case_id"] for item in listed]

    renamed = check(
        reply=live.cases.update(case_id=case_id, name=f"{case['name']}-renamed"), status=200
    )
    assert renamed["name"] == f"{case['name']}-renamed"
    assert (
        check(reply=live.cases.update(case_id=case_id, priority="low"), status=200)["priority"]
        == "LOW"
    )
    closed = check(reply=live.cases.update(case_id=case_id, status="CLOSED"), status=200)
    assert closed["status"] == "CLOSED"
    assert closed["resolved_at"] is not None
    reopened = check(reply=live.cases.update(case_id=case_id, status="OPEN"), status=200)
    assert reopened["resolved_at"] is None
    appended = check(
        reply=live.cases.append_description(case_id=case_id, description="Appended text"),
        status=200,
    )
    assert appended["description"].endswith("Appended text")

    check(reply=live.cases.delete(case_id=case_id), status=204)
    assert wait_until_gone(read=lambda: live.cases.get(case_id=case_id)) == 404


def test_a_case_cannot_be_closed_while_a_closure_condition_is_not_met(live, team_id, cleanup):
    created = check(
        reply=live.cases.create(
            team_id=team_id,
            name=throwaway(kind="case"),
            closure_conditions=NEEDS_AN_ASSIGNEE,
        ),
        status=201,
    )
    case_id = created["case_id"]
    cleanup.add(description=f"case {case_id}", action=lambda: live.cases.delete(case_id=case_id))

    reply = live.cases.update(case_id=case_id, status="CLOSED")

    assert reply.status_code == 422
    assert reply.data == ["Cannot close case as all case requirements have not been met"]
    assert check(reply=live.cases.get(case_id=case_id), status=200)["status"] == "OPEN"


def test_list_filters_and_search_find_the_case(live, team_id, case):
    case_id = case["case_id"]
    by_id = check(
        reply=live.cases.list(filters={"case_ids": [case_id], "status": "OPEN"}), status=200
    )
    closed = check(
        reply=live.cases.list(filters={"case_ids": [case_id], "status": "CLOSED"}), status=200
    )
    by_metadata = check(
        reply=live.cases.list(filters={"metadata": {"source": "live-check"}}, team_id=team_id),
        status=200,
    )

    assert [item["case_id"] for item in by_id["cases"]] == [case_id]
    assert closed["cases"] == []
    assert case_id in [item["case_id"] for item in by_metadata["cases"]]

    def search_by_name():
        return live.cases.search(
            filter={"field": "name", "operator": "CONTAINS", "value": case["name"]},
            include_total=True,
        )

    assert wait_for(condition=lambda: search_by_name().data.get("total") == 1)
    found = check(reply=search_by_name(), status=200)
    assert [item["case_id"] for item in found["cases"]] == [case_id]
    assert "assignees" in found["cases"][0]
    assert "tasks" not in found["cases"][0]


def test_the_activities_of_a_case_can_be_listed_filtered_and_read(live, case):
    case_id = case["case_id"]
    live.cases.update(case_id=case_id, description="Changed")

    everything = check(reply=live.cases.activities.list(case_id=case_id), status=200)
    created_only = check(
        reply=live.cases.activities.list(case_id=case_id, activity_types=["CREATED"]),
        status=200,
    )
    one = check(
        reply=live.cases.activities.get(
            case_id=case_id, activity_id=everything["activities"][0]["id"]
        ),
        status=200,
    )

    types = {activity["activity_type"] for activity in everything["activities"]}
    assert {"CREATED", "DESCRIPTION_UPDATED"} <= types
    assert {activity["activity_type"] for activity in created_only["activities"]} == {"CREATED"}
    assert one["case_id"] == case_id
    assert isinstance(
        check(reply=live.cases.assignees.list(case_id=case_id), status=200)["assignees"], list
    )


def test_the_pdf_of_a_case_is_returned_as_bytes(live, case):
    reply = live.cases.get_pdf(case_id=case["case_id"])

    assert reply.status_code == 200
    assert reply.headers["content-type"] == "application/pdf"
    assert isinstance(reply.data, bytes)
    assert reply.data.startswith(b"%PDF")


@pytest.mark.parametrize(
    ("arguments", "status"),
    [
        pytest.param({"priority": "BOGUS"}, 422, id="a priority that does not exist"),
        pytest.param({"status": "BOGUS"}, 422, id="a status that does not exist"),
        pytest.param({"opened_at": "not a date"}, 422, id="an opened_at that is not a date"),
        pytest.param({"team_id": 999999999}, 404, id="a team that does not exist"),
    ],
)
def test_a_case_with_an_invalid_value_is_refused(live, team_id, arguments, status):
    reply = live.cases.create(**{"team_id": team_id, "name": throwaway(kind="case"), **arguments})

    assert reply.status_code == status


def test_a_comment_is_created_read_listed_changed_reacted_to_and_deleted(live, case):
    case_id = case["case_id"]
    created = check(
        reply=live.cases.comments.create(case_id=case_id, value="First comment"), status=201
    )
    comment_id = created["id"]

    assert created["activity_type"] == "COMMENTED"
    assert created["value"] == "First comment"
    fetched = check(
        reply=live.cases.comments.get(case_id=case_id, comment_id=comment_id), status=200
    )
    assert fetched["value"] == "First comment"
    listed = check(reply=live.cases.comments.list(case_id=case_id), status=200)
    assert comment_id in [item["id"] for item in listed["comments"]]

    edited = check(
        reply=live.cases.comments.update(case_id=case_id, comment_id=comment_id, value="Edited"),
        status=200,
    )
    assert edited["value"] == "Edited"
    blank = live.cases.comments.update(case_id=case_id, comment_id=comment_id, value="")
    assert blank.status_code == 422

    reacted = check(
        reply=live.cases.comments.add_reaction(case_id=case_id, comment_id=comment_id, value="+1"),
        status=201,
    )
    assert ":+1:" in [reaction["emoji"] for reaction in reacted["reactions"]]
    refused = live.cases.comments.add_reaction(
        case_id=case_id, comment_id=comment_id, value="smile"
    )
    assert refused.status_code == 422

    check(reply=live.cases.comments.delete(case_id=case_id, comment_id=comment_id), status=204)
    gone = live.cases.comments.get(case_id=case_id, comment_id=comment_id)
    assert gone.status_code == 404


def test_a_note_is_created_read_listed_changed_extended_and_deleted(live, case):
    case_id = case["case_id"]
    created = check(
        reply=live.cases.notes.create(case_id=case_id, title="Findings", color="gold", hidden=True),
        status=201,
    )
    note_id = created["id"]

    assert created["title"] == "Findings"
    assert created["color"] == "gold"
    assert created["hidden"] is True
    assert created["sensitive"] is False
    fetched = check(reply=live.cases.notes.get(case_id=case_id, note_id=note_id), status=200)
    assert fetched["id"] == note_id
    listed = check(reply=live.cases.notes.list(case_id=case_id), status=200)
    assert note_id in [item["id"] for item in listed["notes"]]

    changed = check(
        reply=live.cases.notes.update(
            case_id=case_id, note_id=note_id, content="Body", color="blue"
        ),
        status=200,
    )
    assert changed["content"] == "Body"
    assert changed["color"] == "blue"
    extended = check(
        reply=live.cases.notes.append_content(
            case_id=case_id, note_id=note_id, content=" and more"
        ),
        status=200,
    )
    assert extended["content"].endswith(" and more")
    refused = live.cases.notes.create(case_id=case_id, title="Colour", color="purple")
    assert refused.status_code == 422

    check(reply=live.cases.notes.delete(case_id=case_id, note_id=note_id), status=204)
    assert live.cases.notes.get(case_id=case_id, note_id=note_id).status_code == 404


def test_tasks_are_created_listed_completed_and_deleted(live, case):
    case_id = case["case_id"]
    created = check(
        reply=live.cases.tasks.create(case_id=case_id, description="Check the logs"), status=201
    )["task"]
    batch = check(
        reply=live.cases.tasks.batch_create(
            case_id=case_id, tasks=[{"description": "One"}, {"description": "Two"}]
        ),
        status=201,
    )

    assert created["completed"] is False
    assert [task["description"] for task in batch["tasks"]] == ["One", "Two"]
    listed = check(reply=live.cases.tasks.list(case_id=case_id), status=200)
    assert created["id"] in [task["id"] for task in listed["tasks"]]
    completed = check(
        reply=live.cases.tasks.update(case_id=case_id, task_id=created["id"], completed=True),
        status=200,
    )
    assert completed["task"]["completed"] is True
    assert check(reply=live.cases.tasks.get(case_id=case_id, task_id=created["id"]), status=200)[
        "task"
    ]["completed"]

    unknown = live.cases.tasks.create(
        case_id=case_id, description="x", assignee_emails=["nobody-live-check@example.invalid"]
    )
    blank = live.cases.tasks.create(case_id=case_id, description=" ")
    too_many = live.cases.tasks.batch_create(
        case_id=case_id, tasks=[{"description": str(number)} for number in range(26)]
    )
    assert (unknown.status_code, blank.status_code, too_many.status_code) == (400, 422, 400)

    check(reply=live.cases.tasks.delete(case_id=case_id, task_id=created["id"]), status=204)
    assert live.cases.tasks.get(case_id=case_id, task_id=created["id"]).status_code == 404


def test_metadata_is_created_changed_read_and_deleted(live, case):
    case_id = case["case_id"]
    metadata = live.cases.metadata

    created = check(reply=metadata.create(case_id=case_id, metadata={"a": "1", "b": 2}), status=201)
    clash = metadata.create(case_id=case_id, metadata={"a": "x", "c": "3"})

    assert created["metadata"] == {"source": "live-check", "a": "1", "b": 2}
    assert clash.status_code == 409
    assert "c" not in check(reply=metadata.list(case_id=case_id), status=200)["metadata"]
    assert check(reply=metadata.get(case_id=case_id, key="a"), status=200)["metadata"] == {"a": "1"}
    assert metadata.get(case_id=case_id, key="nope").status_code == 404

    updated = check(
        reply=metadata.update(case_id=case_id, metadata={"a": "10", "d": "4"}), status=200
    )
    assert updated["metadata"]["a"] == "10"
    assert updated["metadata"]["d"] == "4"
    check(reply=metadata.delete(case_id=case_id, metadata=["d"]), status=204)
    assert "d" not in check(reply=metadata.list(case_id=case_id), status=200)["metadata"]
    nested = metadata.create(case_id=case_id, metadata={"x": {"y": 1}})
    assert nested.status_code == 422


def test_the_field_values_of_a_case_without_fields_are_empty_and_unknown_ones_are_not_found(
    live, case
):
    case_id = case["case_id"]
    values = live.cases.field_values

    listed = check(reply=values.list(case_id=case_id), status=200)

    assert listed["fields"] == []
    assert values.create(case_id=case_id, input_id=999999999, value="x").status_code == 404
    assert values.get(case_id=case_id, field_id=999999999).status_code == 404
    assert values.update(case_id=case_id, field_id=999999999, value="x").status_code == 404
    assert values.delete(case_id=case_id, field_id=999999999).status_code == 404


@pytest.fixture
def other_case(live, team_id, cleanup):
    created = check(
        reply=live.cases.create(team_id=team_id, name=throwaway(kind="case")), status=201
    )
    cleanup.add(
        description=f"case {created['case_id']}",
        action=lambda: live.cases.delete(case_id=created["case_id"]),
    )
    return created


def test_a_file_is_attached_read_listed_downloaded_and_deleted(live, case):
    case_id = case["case_id"]
    text = "hello from a live check"
    contents = base64.b64encode(text.encode()).decode()

    created = check(
        reply=live.cases.files.create(
            case_id=case_id, filename="check.txt", file_contents=contents, value="With a comment"
        ),
        status=201,
    )
    file_id = created["id"]

    assert created["activity_type"] == "FILE_ATTACHED_AND_COMMENTED"
    assert created["file"]["filename"] == "check.txt"
    assert (
        check(reply=live.cases.files.get(case_id=case_id, file_id=file_id), status=200)["id"]
        == file_id
    )
    listed = check(reply=live.cases.files.list(case_id=case_id), status=200)
    assert file_id in [item["id"] for item in listed["files"]]
    downloaded = live.cases.files.download(case_id=case_id, file_id=file_id)
    assert downloaded.status_code == 200
    assert downloaded.data == text
    info = check(reply=live.cases.files.info(case_id=case_id, file_id=file_id), status=200)
    assert info["filename"] == "check.txt"
    assert info["sizeinbytes"] == len(text)

    check(reply=live.cases.files.delete(case_id=case_id, file_id=file_id), status=204)
    assert live.cases.files.get(case_id=case_id, file_id=file_id).status_code == 404
    assert (
        live.cases.files.create(case_id=case_id, filename="x", file_contents=contents).status_code
        == 201
    )


def test_blocks_and_their_elements_are_created_read_changed_and_deleted(live, case):
    case_id = case["case_id"]
    note = [{"content": "Start here", "note_type": "text"}]

    block = check(
        reply=live.cases.blocks.create(
            case_id=case_id, title="Notes", block_type="note", elements=note, color="primary"
        ),
        status=201,
    )["block"]
    block_id = block["id"]
    element_id = block["elements"][0]["element_id"]

    assert block["color"] == "white"
    assert block["slug"].startswith("blk_")
    by_slug = check(
        reply=live.cases.blocks.get(case_id=case_id, block_id=block["slug"]), status=200
    )
    assert by_slug["block"]["id"] == block_id
    listed = check(reply=live.cases.blocks.list(case_id=case_id, block_type="note"), status=200)
    assert block_id in [item["id"] for item in listed["blocks"]]
    renamed = check(
        reply=live.cases.blocks.update(
            case_id=case_id, block_id=block_id, title="Renamed", position=0
        ),
        status=200,
    )
    assert renamed["block"]["title"] == "Renamed"

    element = check(
        reply=live.cases.blocks.get_element(
            case_id=case_id, block_id=block_id, element_id=element_id
        ),
        status=200,
    )
    assert element["content"] == "Start here"
    changed = check(
        reply=live.cases.blocks.update_element(
            case_id=case_id, block_id=block_id, element_id=element_id, content="Changed"
        ),
        status=200,
    )
    assert changed["content"] == "Changed"
    extended = check(
        reply=live.cases.blocks.append_element_content(
            case_id=case_id, block_id=block_id, element_id=element_id, content=" and more"
        ),
        status=200,
    )
    assert extended["content"].endswith(" and more")
    wrong = live.cases.blocks.get_element(
        case_id=case_id, block_id=block_id, element_id=block["elements"][0]["id"]
    )
    assert wrong.status_code == 404

    refused = [
        live.cases.blocks.create(case_id=case_id, title="No element", block_type="note"),
        live.cases.blocks.create(
            case_id=case_id, title="Bad", block_type="note", elements=note, position=-1
        ),
    ]
    assert [reply.status_code for reply in refused] == [422, 400]

    check(reply=live.cases.blocks.delete(case_id=case_id, block_id=block_id), status=204)
    assert live.cases.blocks.get(case_id=case_id, block_id=block_id).status_code == 404


def test_the_blocks_of_a_group_stay_when_it_is_deleted_unless_children_are_included(live, case):
    case_id = case["case_id"]
    note = [{"content": "Child", "note_type": "text"}]
    blocks = live.cases.blocks

    def group_with_child(title):
        group = check(
            reply=blocks.create(case_id=case_id, title=title, block_type="block_group"), status=201
        )["block"]
        child = check(
            reply=blocks.create(
                case_id=case_id,
                title=f"{title} child",
                block_type="note",
                elements=note,
                block_group_id=group["slug"],
            ),
            status=201,
        )["block"]
        return group, child

    group, child = group_with_child("Keep")
    assert child["block_group_id"] == group["id"]
    check(reply=blocks.delete(case_id=case_id, block_id=group["id"]), status=204)
    kept = check(reply=blocks.get(case_id=case_id, block_id=child["id"]), status=200)["block"]
    assert kept["block_group_id"] is None

    group, child = group_with_child("Remove")
    check(
        reply=blocks.delete(case_id=case_id, block_id=group["id"], include_children=True),
        status=204,
    )
    assert blocks.get(case_id=case_id, block_id=child["id"]).status_code == 404


def test_cases_are_linked_on_both_sides_and_unlinked(live, case, other_case):
    case_id, other_id = case["case_id"], other_case["case_id"]
    links = live.cases.linked_cases

    created = check(reply=links.create(case_id=case_id, id=other_id), status=201)
    again = links.create(case_id=case_id, id=other_id)

    assert created["linked_case"]["case_id"] == other_id
    assert again.status_code == 201
    mine = check(reply=links.list(case_id=case_id), status=200)["linked_cases"]
    theirs = check(reply=links.list(case_id=other_id), status=200)["linked_cases"]
    assert [link["case_id"] for link in mine] == [other_id]
    assert [link["case_id"] for link in theirs] == [case_id]
    assert links.create(case_id=case_id, id=case_id).status_code == 422
    assert links.create(case_id=case_id, id=999999999).status_code == 404

    check(reply=links.delete(case_id=case_id, linked_case_id=other_id), status=204)
    assert check(reply=links.list(case_id=other_id), status=200)["linked_cases"] == []
    batch = check(reply=links.batch_create(case_id=case_id, ids=[other_id]), status=201)
    assert [link["case_id"] for link in batch["linked_cases"]] == [other_id]
    assert links.batch_create(case_id=case_id, ids=[999999999]).status_code == 404


def test_records_and_subscribers_report_what_is_missing(live, case):
    case_id = case["case_id"]

    records = check(reply=live.cases.records.list(case_id=case_id), status=200)
    subscribers = check(reply=live.cases.subscribers.list(case_id=case_id), status=200)

    assert records["records"] == []
    assert {"id", "user_id", "email"} <= set(subscribers["subscribers"][0])
    assert live.cases.records.create(case_id=case_id, record_id=999999999).status_code == 404
    assert live.cases.records.get(case_id=case_id, record_id=999999999).status_code == 404
    unknown = "nobody-live-check@example.invalid"
    assert live.cases.subscribers.create(case_id=case_id, user_email=unknown).status_code == 404
    assert (
        live.cases.subscribers.batch_create(case_id=case_id, user_emails=[unknown]).status_code
        == 404
    )


def test_the_actions_of_a_case_are_created_changed_replaced_and_deleted(live, case):
    case_id = case["case_id"]
    actions = live.cases.actions

    created = check(
        reply=actions.create(
            case_id=case_id,
            url="https://example.invalid/hook",
            label="Notify",
            action_type="webhook",
            query_params={"channel": "soc"},
        ),
        status=201,
    )
    action_id = created["id"]

    assert created["query_params"] == {"channel": "soc"}
    assert (
        check(reply=actions.get(case_id=case_id, action_id=action_id), status=200)["label"]
        == "Notify"
    )
    listed = check(reply=actions.list(case_id=case_id), status=200)
    assert action_id in [item["id"] for item in listed["actions"]]
    changed = check(
        reply=actions.update(
            case_id=case_id, action_id=action_id, label="Renamed", action_text="Go"
        ),
        status=200,
    )
    assert (changed["label"], changed["action_text"]) == ("Renamed", "Go")
    refused = actions.create(case_id=case_id, url="not a url", label="Bad", action_type="page")
    assert refused.status_code == 422

    replaced = check(
        reply=actions.batch_update(
            case_id=case_id,
            actions=[
                {"url": "https://example.invalid/one", "label": "One", "action_type": "webhook"},
                {"url": "https://example.invalid/two", "label": "Two", "action_type": "page"},
            ],
        ),
        status=200,
    )
    assert [item["label"] for item in replaced["actions"]] == ["One", "Two"]
    assert action_id not in [
        item["id"] for item in check(reply=actions.list(case_id=case_id), status=200)["actions"]
    ]
    first = replaced["actions"][0]["id"]
    check(reply=actions.delete(case_id=case_id, action_id=first), status=204)
    assert actions.get(case_id=case_id, action_id=first).status_code == 404
    check(reply=actions.batch_update(case_id=case_id, actions=[]), status=200)
    assert check(reply=actions.list(case_id=case_id), status=200)["actions"] == []


def test_a_case_that_does_not_exist_is_not_found(live):
    for reply in (
        live.cases.get(case_id=999999999),
        live.cases.update(case_id=999999999, name="x"),
        live.cases.delete(case_id=999999999),
        live.cases.activities.list(case_id=999999999),
    ):
        assert reply.status_code == 404
        assert reply.data == ["TeamCase not found"]
