import unittest
from os              import getenv
from tapi            import UsersAPI
from dotenv          import load_dotenv
from tapi.utils.http import disable_ssl_verification


class test_UsersAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()

        if getenv("SSL_VERIFICATION") == "0":
            disable_ssl_verification()

        self._del_user_id = None
        self.user_api     = UsersAPI(getenv("DOMAIN"), getenv("API_KEY"))

    def tearDown(self):
        if self._del_user_id:
            self.user_api.delete(self._del_user_id)

    def test_create(self):
        resp = self.user_api.create(
            email      = "alice@tines.xyz",
            first_name = "Alice",
            last_name  = "Smith",
            admin      = False
        )

        body = resp.get("body")
        self._del_user_id = body.get("id")

        self.assertEqual(resp.get("status_code"), 201)
        self.assertEqual(body.get("email"), "alice@tines.xyz")
        self.assertEqual(body.get("first_name"), "Alice")
        self.assertEqual(body.get("last_name"), "Smith")
        self.assertEqual(body.get("admin"), False)

    def test_get(self):
        user = self.user_api.create(
            email              = "alice@tines.xyz",
            first_name         = "Alice",
            last_name          = "Smith",
            admin              = False
        )

        user_id = user.get("body").get("id")
        resp = self.user_api.get(user_id = user_id)

        body = resp.get("body")
        self._del_user_id = user_id

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("email"), "alice@tines.xyz")
        self.assertEqual(body.get("first_name"), "Alice")
        self.assertEqual(body.get("last_name"), "Smith")
        self.assertEqual(body.get("admin"), False)

    def test_sign_in_activity(self):
        user = self.user_api.create(email = "alice@tines.xyz")

        user_id = user.get("body").get("id")
        resp = self.user_api.sign_in_activity(user_id = user_id)

        body = resp.get("body")
        self._del_user_id = user_id

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("admin/login_activities")), list)

    def test_update(self):
        user    = self.user_api.create(email = "alice@tines.xyz")
        user_id = user.get("body").get("id")

        resp = self.user_api.update(
            user_id = user_id,
            email   = "alice@tines.abc"
        )

        body = resp.get("body")
        self._del_user_id = user_id

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("email"), "alice@tines.abc")

    def test_list(self):
        resp = self.user_api.list()

        body = resp.get("body")
        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("admin/users")), list)

    def test_delete(self):
        user = self.user_api.create(email="alice@tines.xyz")
        user_id = user.get("body").get("id")

        resp = self.user_api.delete(user_id)

        self.assertEqual(resp.get("status_code"), 204)

    def test_resend_invitation(self):
        user = self.user_api.create(email="alice@tines.xyz")
        user_id = user.get("body").get("id")

        resp = self.user_api.resend_invitation(user_id)
        self._del_user_id = user_id

        self.assertEqual(resp.get("status_code"), 200)

    def test_expire_session(self):
        user = self.user_api.create(email="alice@tines.xyz")
        user_id = user.get("body").get("id")

        resp = self.user_api.expire_session(user_id)
        self._del_user_id = user_id

        self.assertEqual(resp.get("status_code"), 200)