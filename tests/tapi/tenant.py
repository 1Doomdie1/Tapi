import unittest

from os           import getenv
from dotenv       import load_dotenv
from tapi.tenant  import TenantAPI


class test_TenantAPI(unittest.TestCase):

    def setUp(self):
        load_dotenv()
        self.tenant_api = TenantAPI(getenv("DOMAIN"), getenv("API_KEY"))

    def test_info(self):
        resp = self.tenant_api.info()

        assert resp.get("status_code")             == 200
        assert resp.get("body").get("stack")       is not None
        assert type(resp.get("body").get("stack")) == dict
