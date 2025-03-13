import unittest
from os                            import getenv
from tapi                          import GroupsAPI
from dotenv                        import load_dotenv
from tapi.utils.http               import disable_ssl_verification


class test_GroupsAPI(unittest.TestCase):

    def setUp(self):
        load_dotenv()

        if getenv("SSL_VERIFICATION") == "0":
            disable_ssl_verification()

        self.groups_api = GroupsAPI(getenv("DOMAIN"), getenv("API_KEY"))
        self.group_id       = int(getenv("GROUP_ID"))
        self.group_run_guid = getenv("GROUP_RUN_GUID")

    def test_list_run_events(self):
        resp = self.groups_api.list_run_events(
            group_id       = self.group_id,
            group_run_guid = self.group_run_guid
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("group_run_events")), list)

    def test_list_runs(self):
        resp = self.groups_api.list_runs(group_id = self.group_id)

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("group_runs")), list)