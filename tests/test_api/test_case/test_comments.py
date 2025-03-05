import unittest
from os                            import getenv
from dotenv                        import load_dotenv
from tapi.utils.types              import ReactionType
from tapi.utils.testing_decorators import premium_feature
from tapi.utils.http               import disable_ssl_verification
from tapi                          import CaseCommentsAPI, CaseCommentsReactionsAPI


class test_CaseCommentsAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()

        if getenv("SSL_VERIFICATION") == "0":
            disable_ssl_verification()

        self.case_id           = int(getenv("CASE_ID"))
        self.case_comments_api = CaseCommentsAPI(getenv("DOMAIN"), getenv("API_KEY"))

    @premium_feature
    def test_create(self):
        resp = self.case_comments_api.create(
            case_id = self.case_id,
            value   = "Create Comment Unit Test"
        )

        self.assertEqual(resp.get("status_code"), 201)

    @premium_feature
    def test_get(self):
        comment = self.case_comments_api.create(
            case_id = self.case_id,
            value   = "Get Comment Unit Test"
        )

        comment_id = comment.get("body").get("id")

        resp = self.case_comments_api.get(
            case_id    = self.case_id,
            comment_id = comment_id
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("id"), comment_id)
        self.assertEqual(body.get("value"), "Get Comment Unit Test")

    @premium_feature
    def test_update(self):
        comment = self.case_comments_api.create(
            case_id = self.case_id,
            value   = "Update Comment Unit Test"
        )

        comment_id = comment.get("body").get("id")

        resp = self.case_comments_api.update(
            case_id    = self.case_id,
            comment_id = comment_id,
            value      = "New Updated Comment Unit Test"
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("id"), comment_id)
        self.assertEqual(body.get("value"), "New Updated Comment Unit Test")

    @premium_feature
    def test_list(self):
        resp = self.case_comments_api.list(
            case_id = self.case_id
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("comments")), list)

    @premium_feature
    def test_delete(self):
        comment = self.case_comments_api.create(
            case_id = self.case_id,
            value   = "Delete Comment Unit Test"
        )

        comment_id = comment.get("body").get("id")

        resp = self.case_comments_api.delete(
            case_id    = self.case_id,
            comment_id = comment_id
        )

        self.assertEqual(resp.get("status_code"), 204)

class test_CaseCommentsReactionsAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.case_id                     = int(getenv("CASE_ID"))
        self.case_comments_reactions_api = CaseCommentsReactionsAPI(getenv("DOMAIN"), getenv("API_KEY_2"))

    @premium_feature
    def test_add(self):
        resp = self.case_comments_reactions_api.add(
            case_id    = self.case_id,
            comment_id = int(getenv("CASE_COMMENT_ID")),
            value      = ReactionType.PLUS_ONE
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 201)
        self.assertEqual(type(body.get("reactions")), list)

    @premium_feature
    def test_remove(self):
        reaction = self.case_comments_reactions_api.add(
            case_id=self.case_id,
            comment_id=int(getenv("CASE_COMMENT_ID")),
            value=ReactionType.PLUS_ONE
        )

        resp = self.case_comments_reactions_api.remove(
            case_id = self.case_id,
            comment_id=int(getenv("CASE_COMMENT_ID")),
            value=ReactionType.PLUS_ONE
        )

        self.assertEqual(resp.get("status_code"), 204)