import unittest
from os              import getenv
from tapi            import RunsAPI
from dotenv          import load_dotenv
from tapi.utils.http import disable_ssl_verification


class test_RunsAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()

        if getenv("SSL_VERIFICATION") == "0":
            disable_ssl_verification()

        self.story_id       = int(getenv("RUNS_API_STORY_ID"))
        self.story_run_guid = getenv("RUNS_API_STORY_RUN_GUID")
        self.runs_api       = RunsAPI(getenv("DOMAIN"), getenv("API_KEY"))

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
