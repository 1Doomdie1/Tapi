import unittest
from os          import getenv
from tapi.client import Client
from dotenv      import load_dotenv


class test_Client(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.DOMAIN  = getenv("DOMAIN")
        self.API_KEY = getenv("API_KEY")

    def test_credentials_set_to_env(self):
        assert self.API_KEY is not None and self.API_KEY != ""
        assert self.DOMAIN is not None and self.DOMAIN != ""

    def test_http_request_with_good_credentials(self):
        client = Client(self.DOMAIN, self.API_KEY)
        req = client._http_request(method="GET", endpoint="/info")

        self.assertEqual(type(req), dict)
        self.assertEqual(req["status_code"], 200)

    def test_http_request_with_bad_api_key(self):
        client = Client(self.DOMAIN, "API_KEY")
        req = client._http_request(method="GET", endpoint="/info")

        self.assertEqual(type(req), dict)
        self.assertEqual(req["status_code"], 401)

    def test_http_request_with_bad_domain(self):
        client = Client("DOMAIN", self.API_KEY)
        req = client._http_request(method="GET", endpoint="/info")

        self.assertEqual(type(req), dict)
        self.assertEqual(req["status_code"], 500)
