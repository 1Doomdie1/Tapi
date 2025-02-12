import unittest
from os               import getenv
from dotenv           import load_dotenv
from tapi             import ActionEventsAPI

class test_ActionEventsAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.action_id   = int(getenv("ACTION_ID"))
        self.action_events_api = ActionEventsAPI(getenv("DOMAIN"), getenv("API_KEY"))

    def test_list(self):
        resp = self.action_events_api.list(
            action_id = self.action_id
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("events")), list)

    def test_delete(self):
        resp = self.action_events_api.delete(
            action_id = self.action_id
        )

        self.assertEqual(resp.get("status_code"), 200)
