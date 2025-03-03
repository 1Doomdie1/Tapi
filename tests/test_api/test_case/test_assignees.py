import unittest
from os     import getenv
from dotenv import load_dotenv
from tapi   import CaseAssigneesAPI


class test_CaseAssigneesAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.case_id            = int(getenv("CASE_ID"))
        self.case_assignees_api = CaseAssigneesAPI(getenv("DOMAIN"), getenv("API_KEY"))

    @premium_test
    def test_list(self):
        resp = self.case_assignees_api.list(
            case_id = self.case_id
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("assignees")), list)