import unittest
from os                            import getenv
from tapi                          import TeamsAPI
from dotenv                        import load_dotenv
from tapi.utils.testing_decorators import premium_feature
from tapi.utils.http               import disable_ssl_verification


class test_TeamsAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()

        if getenv("SSL_VERIFICATION") == "0":
            disable_ssl_verification()

        self.teams_api = TeamsAPI(getenv("DOMAIN"), getenv("API_KEY"))
        self.team_id   = None

    def tearDown(self):
        if self.team_id:
            self.teams_api.delete(
                team_id = self.team_id
            )

    @premium_feature
    def test_create(self):
        resp = self.teams_api.create(
            name = "Create Team Unit Test"
        )

        self.team_id = resp.get("body").get("id")

        self.assertEqual(resp.get("status_code"), 201)
        self.assertEqual(resp.get("body").get("name"), "Create Team Unit Test")

    @premium_feature
    def test_get(self):
        team = self.teams_api.create(
            name = "Get Team Unit Test"
        )

        self.team_id = team.get("body").get("id")

        resp = self.teams_api.get(
            team_id = self.team_id
        )

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(resp.get("body").get("id"), self.team_id)
        self.assertEqual(resp.get("body").get("name"), "Get Team Unit Test")
        self.assertEqual(type(resp.get("body").get("groups")), list)

    @premium_feature
    def test_update(self):
        team = self.teams_api.create(
            name = "Update Team Unit Test"
        )

        self.team_id = team.get("body").get("id")

        resp = self.teams_api.update(
            team_id = self.team_id,
            name    = "New Updated Team Unit Test"
        )

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(resp.get("body").get("id"), self.team_id)
        self.assertEqual(resp.get("body").get("name"), "New Updated Team Unit Test")

    @premium_feature
    def test_list(self):
        team = self.teams_api.create(
            name = "List Team Unit Test"
        )

        self.team_id = team.get("body").get("id")

        resp = self.teams_api.list()

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(resp.get("body").get("teams")), list)
        self.assertGreaterEqual(len(resp.get("body").get("teams")), 1)

    @premium_feature
    def test_delete(self):
        team = self.teams_api.create(
            name="Delete Team Unit Test"
        )

        team_id = team.get("body").get("id")

        resp = self.teams_api.delete(
            team_id = team_id
        )

        self.assertEqual(resp.get("status_code"), 204)
        self.assertEqual(resp.get("body"), "")
