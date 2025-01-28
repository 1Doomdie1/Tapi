import unittest

from os     import getenv
from dotenv import load_dotenv
from tapi   import TenantAPI


class test_TenantAPI(unittest.TestCase):

    def setUp(self):
        load_dotenv()
        self.tenant_api = TenantAPI(getenv("DOMAIN"), getenv("API_KEY"))

    def test_info(self):
        resp = self.tenant_api.info()

        self.assertEqual(resp.get("status_code"),200)
        self.assertIsNotNone(resp.get("body").get("stack"))
        self.assertEqual(type(resp.get("body").get("stack")),dict)
