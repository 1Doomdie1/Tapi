import unittest
from os                            import getenv
from time                          import time_ns
from dotenv                        import load_dotenv
from tapi.utils.types              import CaseInputType
from tapi.utils.testing_decorators import premium_feature
from tapi.utils.http               import disable_ssl_verification
from tapi                          import CaseInputsAPI, CaseInputsFieldsAPI


class test_CaseInputsAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()

        if getenv("SSL_VERIFICATION") == "0":
            disable_ssl_verification()

        self.team_id         = int(getenv("TEAM_ID"))
        self.case_inputs_api = CaseInputsAPI(getenv("DOMAIN"), getenv("API_KEY"))

    @premium_feature
    def test_create(self):
        input_id = time_ns() // 1000
        resp = self.case_inputs_api.create(
            name       = f"Create Case Input Unit Test {input_id}",
            input_type = CaseInputType.NUMBER,
            team_id    = self.team_id
        )

        body = resp.get("body")
        self.assertEqual(resp.get("status_code"), 201)
        self.assertEqual(body.get("team_case_input").get("name"), f"Create Case Input Unit Test {input_id}")
        self.assertEqual(body.get("team_case_input").get("input_type"), CaseInputType.NUMBER)

    @premium_feature
    def test_get(self):
        resp = self.case_inputs_api.get(
            case_input_id = int(getenv("CASE_INPUT_ID"))
        )

        self.assertEqual(resp.get("status_code"), 200)

    @premium_feature
    def test_list(self):
        resp = self.case_inputs_api.list(
            team_id = self.team_id
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertLessEqual(len(body.get("case_inputs")), 10)

class test_CaseInputsFieldsAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.case_inputs_fields_api = CaseInputsFieldsAPI(getenv("DOMAIN"), getenv("API_KEY"))

    @premium_feature
    def test_list(self):
        resp = self.case_inputs_fields_api.list(
            case_input_id = int(getenv("CASE_INPUT_ID"))
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("fields")), list)
