import unittest
from os                            import getenv
from tapi                          import CasesAPI
from dotenv                        import load_dotenv
from tapi.utils.testing_decorators import premium_feature
from tapi.utils.http               import disable_ssl_verification
from tapi.utils.types              import CasePriority, CaseStatus


class test_CasesAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()

        if getenv("SSL_VERIFICATION") == "0":
            disable_ssl_verification()

        self.team_id   = int(getenv("TEAM_ID"))
        self.case_id   = None
        self.cases_api = CasesAPI(getenv("DOMAIN"), getenv("API_KEY"))

    def tearDown(self):
        if self.case_id:
            self.cases_api.delete(self.case_id)

    @premium_feature
    def test_create(self):
        resp = self.cases_api.create(
            team_id     = self.team_id,
            name        = "Create Case Unit test",
            description = "Created with Tapi :)"
        )

        body         = resp.get("body")
        self.case_id = body.get("case_id")

        self.assertEqual(resp.get("status_code"), 201)
        self.assertEqual(body.get("name"), "Create Case Unit test")
        self.assertEqual(body.get("description"), "Created with Tapi :)")
        self.assertEqual(body.get("status"), CaseStatus.OPEN)
        self.assertEqual(body.get("priority"), CasePriority.LOW)

    @premium_feature
    def test_get(self):
        case = self.cases_api.create(
            team_id     = self.team_id,
            name        = "Get Case Unit test",
            description = "Created with Tapi :)"
        )

        self.case_id = case.get("body").get("case_id")

        resp = self.cases_api.get(
            case_id = self.case_id
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("case_id"), self.case_id)
        self.assertEqual(body.get("name"), "Get Case Unit test")
        self.assertEqual(body.get("description"), "Created with Tapi :)")

    @premium_feature
    def test_download(self):
        resp = self.cases_api.download(
            case_id = 26
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body), bytes)

    @premium_feature
    def test_update(self):
        case = self.cases_api.create(
            team_id     = self.team_id,
            name        = "Update Case Unit test",
            description = "Created with Tapi :)"
        )

        self.case_id = case.get("body").get("case_id")

        resp = self.cases_api.update(
            case_id     = self.case_id,
            name        = "New Updated Case Unit test",
            description = "Created with Tapi :) :)",
            priority    = CasePriority.HIGH
        )

        body = resp.get("body")
        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("name"), "New Updated Case Unit test")
        self.assertEqual(body.get("description"), "Created with Tapi :) :)")
        self.assertEqual(body.get("priority"), CasePriority.HIGH)

    @premium_feature
    def test_list(self):
        case = self.cases_api.create(
            team_id     = self.team_id,
            name        = "List Case Unit test",
            description = "Created with Tapi :)"
        )

        self.case_id = case.get("body").get("case_id")

        resp = self.cases_api.list(
            per_page = 5
        )

        body = resp.get("body")
        self.assertEqual(resp.get("status_code"), 200)
        self.assertGreaterEqual(len(body.get("cases")), 1)
        self.assertLessEqual(len(body.get("cases")), 5)

    @premium_feature
    def test_delete(self):
        case = self.cases_api.create(
            team_id     = self.team_id,
            name        = "Delete Case Unit test",
            description = "Created with Tapi :)"
        )

        case_id = case.get("body").get("case_id")

        resp = self.cases_api.delete(
            case_id = case_id
        )

        self.assertEqual(resp.get("status_code"), 204)
