import unittest
from os     import getenv
from tapi   import EventsAPI
from dotenv import load_dotenv

class test_EventsAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.event_id        = int(getenv("EVENT_ID"))
        self.event_action_id = int(getenv("EVENT_ACTION_ID"))
        self.events_api      = EventsAPI(getenv("DOMAIN"), getenv("API_KEY"))

    @unittest.skip("I need to replace this every 7 days with a new event ID")
    def test_get(self):
        resp = self.events_api.get(
            event_id = self.event_id
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("id"), self.event_id)
        self.assertEqual(body.get("payload"), {"re_emit_action_event": {"message": "Re-emitted message"}})

    def test_list(self):
        resp = self.events_api.list()

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("events")), list)

    @unittest.skip("This needs to have a valid event id, which needs to be created manually")
    def test_re_emit(self):
        resp = self.events_api.re_emit(
            event_id = self.event_id
        )

        self.assertEqual(resp.get("status_code"), 204)