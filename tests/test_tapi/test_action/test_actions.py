import unittest
from os               import getenv
from time             import time_ns
from tapi             import ActionsAPI
from tapi.utils.types import AgentType
from dotenv           import load_dotenv

class test_ActionsAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.story_id    = int(getenv("ACTION_STORY_ID"))
        self.action_id   = int(getenv("ACTION_ID"))
        self.actions_api = ActionsAPI(getenv("DOMAIN"), getenv("API_KEY"))

    def test_create(self):
        resp = self.actions_api.create(
            type     = AgentType.EVENT_TRANSFORM,
            name     = "Event Transform Action Unit Test",
            options  = {
                "mode": "message_only",
                "payload": "=ARRAY(1, 2, 3, 4)"
            },
            position = {"x": 0, "y": 100},
            story_id = self.story_id
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 201)
        self.assertEqual(body.get("type"), AgentType.EVENT_TRANSFORM)
        self.assertEqual(type(body.get("options")), dict)

    def test_get(self):
        resp = self.actions_api.get(
            action_id = self.action_id
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("type"), AgentType.EVENT_TRANSFORM)
        self.assertEqual(body.get("name"), "Action To Get")

    def test_update(self):
        rng = time_ns() // 1000


        resp = self.actions_api.update(
            action_id   = self.action_id,
            description = f"Updated description: {rng}"
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("description"), f"Updated description: {rng}")

    def test_list(self):
        resp = self.actions_api.list(
            story_id = self.story_id
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("agents")), list)

    def test_delete(self):
        action = self.actions_api.create(
            type     = AgentType.EVENT_TRANSFORM,
            name     = "Event Transform Action To Delete",
            options  = {
                "mode": "message_only"
            },
            position = {"x": 0, "y": 0},
            story_id = self.story_id
        )

        action_id = action.get("body").get("id")

        resp = self.actions_api.delete(
            action_id = action_id
        )

        self.assertEqual(resp.get("status_code"), 204)

    def test_clear_memory(self):
        resp = self.actions_api.clear_memory(
            action_id = self.action_id
        )

        self.assertEqual(resp.get("status_code"), 200)