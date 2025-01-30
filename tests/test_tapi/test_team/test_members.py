import unittest
from tapi.utils.types import Role
from os          import getenv
from tapi        import MembersAPI
from dotenv      import load_dotenv


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
