import unittest
from os              import getenv
from dotenv          import load_dotenv
from tapi            import ReportingAPI
from tapi.utils.http import disable_ssl_verification


class test_ReportingAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()

        if getenv("SSL_VERIFICATION") == "0":
            disable_ssl_verification()

        self.reporting_api = ReportingAPI(getenv("DOMAIN"), getenv("API_KEY"))

    def test_action_performance(self):
        resp = self.reporting_api.action_performance()

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("action_performance")), list)

    def test_time_saved(self):
        resp = self.reporting_api.time_saved()

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(resp.get("body").get("time_saved")), list)