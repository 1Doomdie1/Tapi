import unittest
from os     import getenv
from tapi   import RunsAPI
from dotenv import load_dotenv


class test_RunsAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.story_id       = int(getenv("RUNS_API_STORY_ID"))
        self.runs_api       = RunsAPI(getenv("DOMAIN"), getenv("API_KEY"))
        self.story_run_guid = getenv("RUNS_API_STORY_RUN_GUID")

    def test_events(self):
        resp = self.runs_api.events(
            story_id       = self.story_id,
            story_run_guid = self.story_run_guid
        )
        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(resp.get("body").get("story_run_events")), list)

    def test_list(self):
        resp = self.runs_api.list(
            story_id = self.story_id
        )

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(resp.get("body").get("story_runs")), list)
