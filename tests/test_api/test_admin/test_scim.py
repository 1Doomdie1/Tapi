import unittest
from os              import getenv
from dotenv          import load_dotenv
from tapi            import SCIMUserGroupMappingAPI
from tapi.utils.http import disable_ssl_verification


class test_SCIMUserGroupMappingAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()

        if getenv("SSL_VERIFICATION") == "0":
            disable_ssl_verification()

        self.scim_api = SCIMUserGroupMappingAPI(getenv("DOMAIN"), getenv("API_KEY"))

    def test_list(self):
        resp = self.scim_api.list()

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("user_group_mapping")), dict)