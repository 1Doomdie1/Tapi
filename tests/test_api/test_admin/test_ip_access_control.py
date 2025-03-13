import unittest
from os              import getenv
from dotenv          import load_dotenv
from tapi            import IpAccessControlAPI
from tapi.utils.http import disable_ssl_verification


class test_IpAccessControlAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()

        if getenv("SSL_VERIFICATION") == "0":
            disable_ssl_verification()

        self._del_ac_id            = None
        self.ip_access_control_api = IpAccessControlAPI(getenv("DOMAIN"), getenv("API_KEY"))

    def tearDown(self):
        if self._del_ac_id:
            self.ip_access_control_api.delete(id = self._del_ac_id)

    def test_create(self):
        resp = self.ip_access_control_api.create(
            ip = "192.168.0.1",
            description = "Example IP"
        )

        body = resp.get("body")
        self._del_ac_id = body.get("id")

        self.assertEqual(resp.get("status_code"), 201)
        self.assertEqual(body.get("ip"), "192.168.0.1")
        self.assertEqual(body.get("description"), "Example IP")

    def test_get(self):
        ac_ip = self.ip_access_control_api.create(
            ip          = "192.168.0.0",
            description = "IP To Get"
        )

        ac_ip_id = ac_ip.get("body").get("id")
        resp = self.ip_access_control_api.get(id = ac_ip_id)

        self._del_ac_id = ac_ip_id
        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("id"), ac_ip_id)
        self.assertEqual(body.get("ip"), "192.168.0.0")
        self.assertEqual(body.get("description"), "IP To Get")

    def test_update(self):
        ac_ip = self.ip_access_control_api.create(
            ip          = "192.168.0.0",
            description = "IP To Update"
        )

        ac_ip_id = ac_ip.get("body").get("id")
        resp = self.ip_access_control_api.update(
            id          = ac_ip_id,
            ip          = "192.168.0.1",
            description = "Updated Description"
        )

        self._del_ac_id = ac_ip_id
        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("id"), ac_ip_id)
        self.assertEqual(body.get("ip"), "192.168.0.1")
        self.assertEqual(body.get("description"), "Updated Description")

    def test_list(self):
        resp = self.ip_access_control_api.list()

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("admin/ip_access_control_rules")), list)

    def test_delete(self):
        ac_ip = self.ip_access_control_api.create(
            ip          = "192.168.0.0",
            description = "IP To Delete"
        )

        ac_ip_id = ac_ip.get("body").get("id")
        resp = self.ip_access_control_api.delete(
            id = ac_ip_id
        )

        self.assertEqual(resp.get("status_code"), 204)
