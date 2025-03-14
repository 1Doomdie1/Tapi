import unittest
from os                            import getenv
from tapi                          import DraftsAPI
from dotenv                        import load_dotenv
from tapi.utils.testing_decorators import premium_feature
from tapi.utils.http               import disable_ssl_verification


class test_ChangeRequestAPI(unittest.TestCase):

    def setUp(self):
        load_dotenv()

        if getenv("SSL_VERIFICATION") == "0":
            disable_ssl_verification()

        self._del_draft_id  = None
        self.draft_story_id = int(getenv("CHANGE_REQUEST_STORY_ID"))
        self.drafts_api     = DraftsAPI(getenv("DOMAIN"), getenv("API_KEY"))

    def tearDown(self):
        if self._del_draft_id:
            self.drafts_api.delete(self.draft_story_id, self._del_draft_id)

    @premium_feature
    def test_create(self):
        resp = self.drafts_api.create(
            story_id = self.draft_story_id,
            name     = "Create Draft Unit Test"
        )

        body = resp.get("body")
        self._del_draft_id = body.get("id")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("name"), "Create Draft Unit Test")

    @premium_feature
    def test_list(self):
        resp = self.drafts_api.list(story_id = self.draft_story_id)

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("drafts")), list)

    @premium_feature
    def test_delete(self):
        draft = self.drafts_api.create(
            story_id=self.draft_story_id,
            name="Create Draft Unit Test"
        )

        draft_id = draft.get("body").get("id")

        resp = self.drafts_api.delete(
            story_id = self.draft_story_id,
            draft_id = draft_id
        )

        self.assertEqual(resp.get("status_code"), 204)

