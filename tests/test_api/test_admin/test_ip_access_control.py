import unittest
from os               import getenv
from tapi             import AdminAPI
from dotenv           import load_dotenv
from tapi.utils.http  import disable_ssl_verification


class test_ActionsAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()

        if getenv("SSL_VERIFICATION") == "0":
            disable_ssl_verification()

        self.actions_api = AdminAPI(getenv("DOMAIN"), getenv("API_KEY"))
