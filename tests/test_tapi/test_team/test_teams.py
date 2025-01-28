import unittest
from utils.types import Role
from os          import getenv
from dotenv      import load_dotenv
from tapi        import TeamsAPI, MembersAPI


class test_TeamsAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.teams_api = TeamsAPI(getenv("DOMAIN"), getenv("API_KEY"))
        self.team_id   = None

    def tearDown(self):
        if self.team_id:
            self.teams_api.delete(
                team_id = self.team_id
            )

    def test_create(self):
        resp = self.teams_api.create(
            name = "Create Team Unit Test"
        )

        self.team_id = resp.get("body").get("id")

        self.assertEqual(resp.get("status_code"), 201)
        self.assertEqual(resp.get("body").get("name"), "Create Team Unit Test")

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

    def test_list(self):
        team = self.teams_api.create(
            name = "List Team Unit Test"
        )

        self.team_id = team.get("body").get("id")

        resp = self.teams_api.list()

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(resp.get("body").get("teams")), list)
        self.assertGreaterEqual(len(resp.get("body").get("teams")), 1)

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

class test_MembersAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.team_id     = int(getenv("TEAM_ID"))
        self.members_api = MembersAPI(getenv("DOMAIN"), getenv("API_KEY"))

    def test_list(self):
        resp = self.members_api.list(
            team_id = self.team_id
        )

        self.assertEqual(resp.get("status_code"), 200)
        self.assertGreaterEqual(len(resp.get("body").get("members")), 1)

    def test_remove(self):
        member = self.members_api.invite(
            team_id = self.team_id,
            email   = getenv("MEMBER_TO_INVITE_EMAIL")
        )

        member_id = member.get("body").get("id")

        resp = self.members_api.remove(
            team_id = self.team_id,
            user_id = member_id
        )

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(resp.get("body").get("deleted_id"), member_id)

    def test_invite(self):
        resp = self.members_api.invite(
            team_id = self.team_id,
            email   = getenv("MEMBER_TO_INVITE_EMAIL")
        )

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(resp.get("body").get("email"), getenv("MEMBER_TO_INVITE_EMAIL"))
        self.assertEqual(resp.get("body").get("role"), Role.VIEWER)

    def test_resent_invite(self):
        member = self.members_api.invite(
            team_id = self.team_id,
            email   = getenv("MEMBER_TO_INVITE_EMAIL")
        )

        member_id = member.get("body").get("id")

        resp = self.members_api.resend_invite(
            team_id = self.team_id,
            user_id = member_id
        )

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(resp.get("body").get("email"), getenv("MEMBER_TO_INVITE_EMAIL"))
