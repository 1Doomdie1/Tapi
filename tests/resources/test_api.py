import pytest

from tests.support import Case, assert_covers, assert_sent, case_id, wire

LIST = {
    "team_id": 3,
    "folder_id": 4,
    "filter": "UNUSED_IN_ACTIONS",
    "include_referencing_action_ids": True,
    "include_value": True,
    "typed_value": True,
    "per_page": 100,
    "page": 2,
}
GET = {"resource_id": 9, "include_referencing_action_ids": False, "typed_value": True}
CREATE = {
    "name": "allowed_ips",
    "value": "1.2.3.4",
    "team_id": 1,
    "folder_id": 4,
    "read_access": "GLOBAL",
    "shared_team_slugs": ("a", "b"),
    "description": "text",
    "live_resource_id": 5,
    "include_referencing_action_ids": True,
    "typed_value": True,
}
UPDATE = {
    "resource_id": 9,
    "value": "new value",
    "name": "renamed",
    "folder_id": 4,
    "read_access": "TEAM",
    "shared_team_slugs": ("a",),
    "description": "text",
    "test_resource_enabled": True,
    "is_test": False,
    "include_referencing_action_ids": True,
    "typed_value": True,
}
REMOVE = {"resource_id": 9, "key": "k", "index": 0, "if_value": "x", "is_test": True}
REPLACE = {
    "resource_id": 9,
    "value": "new",
    "key": "k",
    "index": 2,
    "if_value": "old",
    "is_test": False,
}
RESOURCE = "/api/v1/global_resources"

CASES = [
    Case(target="resources.list", arguments={}, route=f"GET {RESOURCE}"),
    Case(target="resources.list", arguments=LIST, route=f"GET {RESOURCE}", params=LIST),
    Case(target="resources.get", arguments={"resource_id": 9}, route=f"GET {RESOURCE}/9"),
    Case(
        target="resources.get",
        name="false is sent, not left out",
        arguments=GET,
        route=f"GET {RESOURCE}/9",
        params=wire(arguments=GET, drop=["resource_id"]),
    ),
    Case(
        target="resources.create",
        arguments={"name": "allowed_ips", "value": "1.2.3.4", "team_id": 1},
        route=f"POST {RESOURCE}",
        body={"name": "allowed_ips", "value": "1.2.3.4", "team_id": 1},
    ),
    Case(
        target="resources.create",
        name="a tuple is sent as a list",
        arguments=CREATE,
        route=f"POST {RESOURCE}",
        body=wire(arguments=CREATE),
    ),
    Case(
        target="resources.update",
        arguments={"resource_id": 9, "value": "new value"},
        route=f"PATCH {RESOURCE}/9",
        body={"value": "new value"},
    ),
    Case(
        target="resources.update",
        name="a tuple is sent as a list, and false is sent",
        arguments=UPDATE,
        route=f"PATCH {RESOURCE}/9",
        body=wire(arguments=UPDATE, drop=["resource_id"]),
    ),
    Case(target="resources.delete", arguments={"resource_id": 9}, route=f"DELETE {RESOURCE}/9"),
    Case(
        target="resources.append",
        name="a list is a valid value",
        arguments={"resource_id": 9, "value": [4, 5]},
        route=f"POST {RESOURCE}/9/append",
        body={"value": [4, 5]},
    ),
    Case(
        target="resources.append",
        name="false is sent, not left out",
        arguments={"resource_id": 9, "value": "x", "is_test": False},
        route=f"POST {RESOURCE}/9/append",
        body={"value": "x", "is_test": False},
    ),
    Case(
        target="resources.remove",
        name="required arguments send an empty JSON body",
        arguments={"resource_id": 9},
        route=f"POST {RESOURCE}/9/remove",
        body={},
    ),
    Case(
        target="resources.remove",
        name="an index of 0 is sent",
        arguments=REMOVE,
        route=f"POST {RESOURCE}/9/remove",
        body=wire(arguments=REMOVE, drop=["resource_id"]),
    ),
    Case(
        target="resources.replace",
        arguments={"resource_id": 9, "value": "new"},
        route=f"POST {RESOURCE}/9/replace",
        body={"value": "new"},
    ),
    Case(
        target="resources.replace",
        name="false is sent, not left out",
        arguments=REPLACE,
        route=f"POST {RESOURCE}/9/replace",
        body=wire(arguments=REPLACE, drop=["resource_id"]),
    ),
    Case(
        target="resources.set_locked",
        name="false is sent, not left out",
        arguments={"resource_id": 9, "locked": False},
        route=f"PUT {RESOURCE}/9/locked",
        body={"locked": False},
    ),
]


@pytest.mark.parametrize("case", CASES, ids=case_id)
def test_request(tines, router, case):
    assert_sent(tines=tines, router=router, case=case)


def test_every_method_and_argument_has_a_case(tines):
    assert_covers(tines=tines, area="resources", cases=CASES)
