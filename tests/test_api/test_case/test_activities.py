import unittest
from os                            import getenv
from dotenv                        import load_dotenv
from tapi.utils.testing_decorators import premium_feature
from tapi                          import CaseActivitiesAPI
from tapi.utils.http               import disable_ssl_verification


class test_CaseActivitiesAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()

        if getenv("SSL_VERIFICATION") == "0":
            disable_ssl_verification()

        self.case_id         = int(getenv("CASE_ID"))
        self.case_activities_api = CaseActivitiesAPI(getenv("DOMAIN"), getenv("API_KEY"))

    @premium_feature
    def test_get(self):
        resp = self.case_activities_api.get(
            case_id = self.case_id,
            activity_id = int(getenv("CASE_ACTIVITY_ID"))
        )

        self.assertEqual(resp.get("status_code"), 200)

    @premium_feature
    def test_list(self):
        resp = self.case_activities_api.list(
            case_id = self.case_id
        )

        body = resp.get("body")
        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("activities")), list)
