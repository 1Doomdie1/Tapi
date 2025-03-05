import unittest
from os     import getenv
from tapi   import TenantAPI
from dotenv import load_dotenv
from tapi.utils.http import disable_ssl_verification


class test_TenantAPI(unittest.TestCase):

    def setUp(self):
        load_dotenv()

        if getenv("SSL_VERIFICATION") == "0":
            disable_ssl_verification()

        self.tenant_api = TenantAPI(getenv("DOMAIN"), getenv("API_KEY"))

    def test_info(self):
        resp = self.tenant_api.info()

        self.assertEqual(resp.get("status_code"),200)
        self.assertIsNotNone(resp.get("body").get("stack"))
        self.assertEqual(type(resp.get("body").get("stack")),dict)
