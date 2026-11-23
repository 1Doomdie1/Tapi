import pytest

from tapi import Response
from tests.live.helpers import all_items, check, throwaway, wait_until_gone

pytestmark = pytest.mark.writes

ALWAYS = [{"name": "Always true", "formula": "=TRUE"}]
HOOK = "https://example.invalid/tapi-live-check"
UNKNOWN = 999999999
SERVER_CHECKED = {
    "number": "5",
    "email": "a@example.com",
    "url": "https://example.com",
    "ip_address": "1.2.3.4",
    "boolean": "true",
}


class Made:
    def __init__(self, *, live, fallbacks):
        self._live = live
        self._fallbacks = fallbacks
        self.cases = []
        self.fields = []
        self.statuses = []
        self.templates = []
        self.webhooks = []

    def case(self, **arguments):
        created = check(reply=self._live.cases.create(**arguments), status=201)
        self.cases.append(created["case_id"])
        return created

    def field(self, **arguments):
        created = check(reply=self._live.cases.fields.create(**arguments), status=201)
        self.fields.append(created["team_case_input"]["id"])
        return created["team_case_input"]

    def status(self, **arguments):
        created = check(reply=self._live.cases.statuses.create(**arguments), status=201)
        self.statuses.append((created["id"], created["parent_status"].upper()))
        return created

    def template(self, **arguments):
        created = check(reply=self._live.cases.templates.create(**arguments), status=201)
        self.templates.append(created["id"])
        return created

    def webhook(self, **arguments):
        created = check(reply=self._live.cases.webhooks.create(**arguments), status=201)
        self.webhooks.append(created["webhook"]["id"])
        return created["webhook"]

    def delete_everything(self) -> Response:
        cases, fields = self._live.cases, self._live.cases.fields
        steps = (
            [cases.delete(case_id=item) for item in self.cases],
            [cases.webhooks.delete(webhook_id=item) for item in self.webhooks],
            [cases.templates.delete(template_id=item) for item in self.templates],
            [
                cases.statuses.delete(status_id=item, fallback_status_id=self._fallbacks[parent])
                for item, parent in self.statuses
            ],
            [fields.delete(field_id=item) for item in self.fields],
        )
        replies = [reply for step in steps for reply in step]
        refused = [reply for reply in replies if reply.status_code not in (200, 204, 404)]
        return (refused or replies or [Response(status_code=204, data=None, headers={})])[0]


@pytest.fixture
def default_statuses(live, team_id, no_leftovers):
    listed = all_items(
        method=live.cases.statuses.list,
        key="case_sub_statuses",
        arguments={"team_id": team_id},
    )
    return {item["slug"]: item for item in listed if item["default"]}


@pytest.fixture
def made(live, default_statuses, cleanup):
    fallbacks = {"OPEN": default_statuses["to_do"]["id"], "CLOSED": default_statuses["done"]["id"]}
    registry = Made(live=live, fallbacks=fallbacks)
    cleanup.add(description="the objects of a test", action=registry.delete_everything)
    return registry


def test_a_field_is_created_read_listed_changed_and_deleted(live, team_id, made):
    fields = live.cases.fields
    name = throwaway(kind="field")

    created = made.field(name=name, input_type="string", team_id=team_id)

    assert created["name"] == name
    assert created["input_type"] == "string"
    assert created["sensitive"] is False
    assert created["validation_type"] == "none"
    assert created["validation_options"] == {}
    assert created["team_case_input_group"] is None
    assert isinstance(created["key"], str)
    fetched = check(reply=fields.get(field_id=created["id"]), status=200)
    assert fetched["id"] == created["id"]
    assert set(fetched) == set(created)
    listed = all_items(method=fields.list, key="case_inputs", arguments={"team_id": team_id})
    assert created["id"] in [item["id"] for item in listed]
    assert check(reply=fields.list_values(field_id=created["id"]), status=200)["fields"] == []

    renamed = check(
        reply=fields.update(field_id=created["id"], name=f"{name}-renamed", sensitive=True),
        status=200,
    )
    assert renamed["name"] == f"{name}-renamed"
    assert renamed["sensitive"] is True
    assert (
        fields.create(name=f"{name}-renamed", input_type="string", team_id=team_id).status_code
        == 422
    )
    assert fields.create(name=name, input_type="string", team_id=UNKNOWN).status_code == 404
    assert fields.get(field_id=UNKNOWN).status_code == 404
    assert fields.update(field_id=UNKNOWN, name="x").status_code == 404
    assert fields.delete(field_id=UNKNOWN).status_code == 404
    assert fields.list_values(field_id=UNKNOWN).status_code == 404

    check(reply=fields.delete(field_id=created["id"]), status=204)
    assert wait_until_gone(read=lambda: fields.get(field_id=created["id"])) == 404


def test_the_options_of_a_field_limit_its_values_and_can_be_changed(live, team_id, made):
    case_id = made.case(team_id=team_id, name=throwaway(kind="case"))["case_id"]
    field = made.field(
        name=throwaway(kind="field"),
        input_type="string",
        team_id=team_id,
        validation_type="options",
        validation_options={"options": ["low", "high"]},
    )
    values = live.cases.field_values

    assert field["validation_type"] == "options"
    assert field["validation_options"] == {"options": ["low", "high"]}
    accepted = check(
        reply=values.create(case_id=case_id, input_id=field["id"], value="low"), status=201
    )
    refused = values.create(case_id=case_id, input_id=field["id"], value="medium")
    assert accepted["field"]["value"] == "low"
    assert refused.status_code == 422
    assert "Value must be one of low, high" in str(refused.data)
    listed = check(reply=live.cases.fields.list_values(field_id=field["id"]), status=200)
    assert [item["value"] for item in listed["fields"]] == ["low"]

    changed = check(
        reply=live.cases.fields.update(
            field_id=field["id"], validation_options={"options": ["medium"]}
        ),
        status=200,
    )
    assert changed["validation_options"] == {"options": ["medium"]}
    assert values.create(case_id=case_id, input_id=field["id"], value="x").status_code == 422


def test_a_pattern_limits_the_values_of_a_field_and_none_takes_the_limit_away(live, team_id, made):
    case_id = made.case(team_id=team_id, name=throwaway(kind="case"))["case_id"]
    field = made.field(
        name=throwaway(kind="field"),
        input_type="string",
        team_id=team_id,
        validation_type="regex",
        validation_options={"regex": "^T-[0-9]+$"},
    )
    values = live.cases.field_values

    good = values.create(case_id=case_id, input_id=field["id"], value="T-123")
    bad = values.create(case_id=case_id, input_id=field["id"], value="nope")

    assert good.status_code == 201
    assert bad.status_code == 422
    assert "Value must match ^T-[0-9]+$" in str(bad.data)
    live.cases.fields.update(field_id=field["id"], validation_type="none")
    assert values.create(case_id=case_id, input_id=field["id"], value="nope").status_code == 201


@pytest.mark.parametrize("input_type", sorted(SERVER_CHECKED))
def test_the_values_of_a_field_are_checked_against_its_type(live, team_id, made, input_type):
    case_id = made.case(team_id=team_id, name=throwaway(kind="case"))["case_id"]
    field = made.field(name=throwaway(kind="field"), input_type=input_type, team_id=team_id)

    good = live.cases.field_values.create(
        case_id=case_id, input_id=field["id"], value=SERVER_CHECKED[input_type]
    )
    bad = live.cases.field_values.create(case_id=case_id, input_id=field["id"], value="not valid")

    assert (good.status_code, bad.status_code) == (201, 422)


def test_field_values_are_set_when_a_case_is_created_and_in_bulk(live, team_id, made):
    field = made.field(name=throwaway(kind="field"), input_type="string", team_id=team_id)
    with_value = made.case(
        team_id=team_id,
        name=throwaway(kind="case"),
        field_values={str(field["id"]): "first"},
    )["case_id"]
    without = made.case(team_id=team_id, name=throwaway(kind="case"))["case_id"]

    def value_of(case_id):
        listed = check(reply=live.cases.field_values.list(case_id=case_id), status=200)["fields"]
        return {item["case_input"]["id"]: item["value"] for item in listed}.get(field["id"])

    assert value_of(with_value) == "first"
    assert value_of(without) is None
    update = {"input_id": field["id"], "value": "second"}
    updated = check(
        reply=live.cases.bulk_update_fields(case_ids=[with_value, without], fields=[update]),
        status=201,
    )
    assert sorted(item["case_id"] for item in updated["cases"]) == sorted([with_value, without])
    assert (value_of(with_value), value_of(without)) == ("second", None)
    check(
        reply=live.cases.bulk_update_fields(
            case_ids=[with_value, without], fields=[{**update, "value": "third", "upsert": True}]
        ),
        status=201,
    )
    assert (value_of(with_value), value_of(without)) == ("third", "third")
    again = live.cases.field_values.create(case_id=with_value, input_id=field["id"], value="fourth")
    assert again.status_code == 201
    assert value_of(with_value) == "fourth"
    listed = check(reply=live.cases.fields.list_values(field_id=field["id"]), status=200)
    assert sorted(item["value"] for item in listed["fields"]) == ["fourth", "third"]


def test_a_status_is_created_listed_changed_used_and_deleted(live, team_id, made, default_statuses):
    statuses = live.cases.statuses
    name = throwaway(kind="status")

    assert set(default_statuses) == {"to_do", "in_progress", "done", "canceled"}
    assert default_statuses["to_do"]["parent_status"] == "OPEN"
    assert default_statuses["done"]["parent_status"] == "CLOSED"
    created = made.status(team_id=team_id, name=name, description="First")
    closing = made.status(team_id=team_id, name=f"{name}-closing", parent_status="closed")

    assert created["parent_status"] == "OPEN"
    assert created["default"] is False
    assert created["description"] == "First"
    assert closing["parent_status"].upper() == "CLOSED"
    fetched = check(reply=statuses.get(status_id=created["id"]), status=200)
    assert fetched["id"] == created["id"]
    found = check(
        reply=statuses.list(team_id=team_id, search=name.upper(), parent_status="OPEN"), status=200
    )
    assert [item["id"] for item in found["case_sub_statuses"]] == [created["id"]]
    renamed = check(
        reply=statuses.update(
            status_id=created["id"], name=f"{name}-renamed", description="Second"
        ),
        status=200,
    )
    assert renamed["name"] == f"{name}-renamed"
    assert renamed["slug"] != created["slug"]
    assert renamed["description"] == "Second"
    assert statuses.create(team_id=team_id, name=f"{name}-renamed").status_code == 422
    assert statuses.create(team_id=team_id, name="x", parent_status="BOGUS").status_code == 422
    assert statuses.create(team_id=UNKNOWN, name="x").status_code == 404
    assert statuses.get(status_id=UNKNOWN).status_code == 404
    assert statuses.update(status_id=UNKNOWN, name="x").status_code == 404

    case = made.case(team_id=team_id, name=throwaway(kind="case"), sub_status_id=created["id"])
    assert case["sub_status"]["id"] == created["id"]
    fallback = default_statuses["in_progress"]["id"]
    assert statuses.delete(status_id=created["id"], fallback_status_id=UNKNOWN).status_code == 404
    other_parent = statuses.delete(
        status_id=created["id"], fallback_status_id=default_statuses["done"]["id"]
    )
    assert other_parent.status_code == 422
    assert "Fallback status must be of the same parent status" in str(other_parent.data)
    check(reply=statuses.delete(status_id=created["id"], fallback_status_id=fallback), status=204)
    assert wait_until_gone(read=lambda: statuses.get(status_id=created["id"])) == 404
    moved = check(reply=live.cases.get(case_id=case["case_id"]), status=200)
    assert moved["sub_status"]["id"] == fallback


def test_a_template_is_created_read_listed_changed_exported_imported_previewed_and_used(
    live, team_id, made
):
    templates = live.cases.templates
    name = throwaway(kind="template")
    options = {
        "name": "From the template",
        "description": "Described",
        "priority": "high",
        "tasks": [{"description": "Check the logs"}],
        "metadata": {"source": "template"},
        "closure_conditions": ALWAYS,
    }

    created = made.template(team_id=team_id, name=name, emoji=":mag:", options=options)

    assert {"id", "name", "emoji", "team", "created_at", "updated_at"} <= set(created)
    assert created["name"] == name
    fetched = check(reply=templates.get(template_id=created["id"]), status=200)
    assert fetched["id"] == created["id"]
    found = check(reply=templates.list(team_id=team_id, search=name), status=200)
    assert created["id"] in [item["id"] for item in found["case_templates"]]

    changed = check(
        reply=templates.update(
            template_id=created["id"], name=f"{name}-renamed", options={"priority": "low"}
        ),
        status=200,
    )
    assert changed["name"] == f"{name}-renamed"
    exported = check(reply=templates.export(template_id=created["id"]), status=200)
    exported_options = exported["templates"][0]["options"]
    assert {"schema_version", "exported_at", "templates"} <= set(exported)
    assert exported_options["priority"] == "low"
    assert exported_options["case_name"] == "From the template"
    assert len(exported_options["team_case_tasks"]) == 1

    imported = check(reply=templates.import_(team_id=team_id, data=exported), status=201)
    made.templates.extend(item["id"] for item in imported["case_templates"])
    assert len(imported["case_templates"]) == 1
    assert imported["case_templates"][0]["name"] != f"{name}-renamed"
    assert templates.import_(team_id=team_id, data={}).status_code == 422
    preview = check(reply=templates.preview(template_id=created["id"]), status=200)
    assert preview["name"] == "From the template"
    assert len(preview["tasks"]) == 1

    case = made.case(team_id=team_id, name=throwaway(kind="case"), template_id=created["id"])
    assert case["priority"] == "LOW"
    assert case["metadata"] == {"source": "template"}
    assert len(case["tasks"]) == 1
    assert len(case["closure_conditions"]) == 1
    unknown = live.cases.create(
        team_id=team_id, name=throwaway(kind="case"), template_id="no-such-template"
    )
    assert unknown.status_code == 404

    assert templates.create(team_id=team_id, name=f"{name}-renamed").status_code == 422
    assert templates.create(team_id=UNKNOWN, name="x").status_code == 404
    refused = templates.create(team_id=team_id, name="x", options={"priority": "BOGUS"})
    assert refused.status_code == 400
    assert templates.get(template_id=UNKNOWN).status_code == 404
    assert templates.update(template_id=UNKNOWN, name="x").status_code == 404
    check(reply=templates.delete(template_id=created["id"]), status=204)
    assert wait_until_gone(read=lambda: templates.get(template_id=created["id"])) == 404
    assert check(reply=live.cases.get(case_id=case["case_id"]), status=200)["priority"] == "LOW"


def test_a_webhook_is_created_read_listed_changed_and_deleted(live, team_id, made):
    webhooks = live.cases.webhooks

    created = made.webhook(team_id=team_id, url=HOOK)

    assert created["url"] == HOOK
    assert created["notifications"] == ["ALL"]
    assert created["name"] is None
    assert {"id", "name", "notifications", "team", "url", "version_number"} <= set(created)
    fetched = check(reply=webhooks.get(webhook_id=created["id"]), status=200)
    assert fetched["webhook"]["id"] == created["id"]
    listed = all_items(method=webhooks.list, key="webhooks", arguments={"team_id": team_id})
    assert created["id"] in [item["id"] for item in listed]

    changed = check(
        reply=webhooks.update(
            webhook_id=created["id"],
            url=f"{HOOK}/changed",
            name="Renamed",
            notifications=["SLA_EXCEEDED", "TASK_CREATED"],
        ),
        status=200,
    )["webhook"]
    assert changed["url"] == f"{HOOK}/changed"
    assert changed["name"] == "Renamed"
    assert changed["notifications"] == ["SLA_EXCEEDED", "TASK_CREATED"]
    emptied = check(reply=webhooks.update(webhook_id=created["id"], name=""), status=200)
    assert emptied["webhook"]["name"] in ("", None)
    nothing = webhooks.update(webhook_id=created["id"])
    assert nothing.status_code == 422
    assert "At least one of url, name, version_number, or notifications" in str(nothing.data)
    assert webhooks.update(webhook_id=created["id"], url="not a url").status_code == 422
    assert webhooks.update(webhook_id=created["id"], notifications=["BOGUS"]).status_code == 422
    assert webhooks.create(team_id=team_id, url="not a url").status_code == 422
    assert webhooks.create(team_id=UNKNOWN, url=HOOK).status_code == 404
    assert webhooks.get(webhook_id=UNKNOWN).status_code == 404
    assert webhooks.update(webhook_id=UNKNOWN, name="x").status_code == 404
    assert webhooks.delete(webhook_id=UNKNOWN).status_code == 404

    check(reply=webhooks.delete(webhook_id=created["id"]), status=204)
    assert wait_until_gone(read=lambda: webhooks.get(webhook_id=created["id"])) == 404
