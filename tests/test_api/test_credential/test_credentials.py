import unittest
from os     import getenv
from dotenv import load_dotenv
from tapi   import CredentialsAPI
from time   import time_ns

class test_CredentialsAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self._del_cred       = None
        self.cred_id         = int(getenv("CREDENTIAL_ID"))
        self.team_id         = int(getenv("TEAM_ID"))
        self.credentials_api = CredentialsAPI(getenv("DOMAIN"), getenv("API_KEY"))

    def tearDown(self):
        if self._del_cred:
            self.credentials_api.delete(credential_id=self._del_cred)

    def test_create_aws(self):
        resp = self.credentials_api.create_aws(
            name                    = "aws_credential",
            team_id                 = self.team_id,
            aws_authentication_type = "ROLE",
            aws_access_key          = "v_access_key",
            aws_secret_key          = "v_secret_key",
            aws_assumed_role_arn    = "v_role_arn"
        )

        self._del_cred = resp.get("body").get("id")

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"),             201)
        self.assertEqual(body.get("name"),                    "aws_credential")
        self.assertEqual(body.get("mode"),                    "AWS")
        self.assertEqual(body.get("aws_authentication_type"), "ROLE")

    def test_create_http_request(self):
        resp = self.credentials_api.create_http_request(
            name                 = "http_request_credential",
            team_id              = self.team_id,
            http_request_options = {
                "url": "http://www.example.com",
                "content_type": "json",
                "method": "post",
                "payload": {
                    "key": "value",
                    "secret": "I can reference the \\<<secret>> as needed in the payload."
                },
                "headers": {}
            },
            http_request_location_of_token = "\\=credential_name.body.token",
            http_request_secret = "secret_value"
        )

        self._del_cred = resp.get("body").get("id")

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 201)
        self.assertEqual(body.get("name"),        "http_request_credential")
        self.assertEqual(body.get("mode"),        "HTTP_REQUEST_AGENT")


    def test_create_jwt(self):
        resp = self.credentials_api.create_jwt(
            name                          = "jwt_credential",
            team_id                       = self.team_id,
            jwt_algorithm                 = "HS256",
            jwt_payload                   = {"iss": "", "sub": "", "scope": "", "aud": ""},
            jwt_auto_generate_time_claims = True,
            jwt_private_key               = "<private-key>"
        )

        self._del_cred = resp.get("body").get("id")

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 201)
        self.assertEqual(body.get("name"), "jwt_credential")
        self.assertEqual(body.get("mode"), "JWT")

    def test_create_mtls(self):
        resp = self.credentials_api.create_mtls(
            name                    = "mtls_credential",
            team_id                 = self.team_id,
            mtls_client_certificate = "<mtls_client_certificate_text>",
            mtls_client_private_key = "<mtls_client_private_key_text>",
            mtls_root_certificate   = "<mtls_root_certificate_text>"
        )

        self._del_cred = resp.get("body").get("id")

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 201)
        self.assertEqual(body.get("name"), "mtls_credential")
        self.assertEqual(body.get("mode"), "MTLS")

    def test_create_multi_request(self):
        resp = self.credentials_api.create_multi_request(
            name                           = "multi_request_credential",
            team_id                        = self.team_id,
            http_request_location_of_token = "\\=credential_name.body.token",
            credential_requests            = [
                {
                    "options": {
                        "url": "http://www.example.com",
                        "content_type": "json",
                        "method": "post",
                        "payload": {
                            "key": "value",
                            "secret": "I can reference the \\<<secret>> as needed in the payload."
                        },
                        "headers": {}
                    },
                    "http_request_secret": "secret_value"
                },
                {
                    "options": {
                        "url": "http://www.example.com",
                        "content_type": "json",
                        "method": "post",
                        "payload": {
                            "key": "value",
                            "secret": "I can reference \\<<PREVIOUS_STEP>> or the \\<<secret>> as needed in the payload."
                        },
                        "headers": {}
                    },
                    "http_request_secret": "secret_value"
                }
            ]
        )

        self._del_cred = resp.get("body").get("id")

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 201)
        self.assertEqual(body.get("name"), "multi_request_credential")
        self.assertEqual(body.get("mode"), "MULTI_REQUEST")

    def test_create_oauth(self):
        resp = self.credentials_api.create_oauth(
            name                = "oauth_credential",
            team_id             = self.team_id,
            oauth_url           = "https://example.com/auth",
            oauth_token_url     = "https://example.com/token",
            oauth_client_id     = "foo",
            oauth_client_secret = "bar",
            oauth_scope         = "sync",
            oauth_grant_type    = "authorization_code"
        )

        self._del_cred = resp.get("body").get("id")

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 201)
        self.assertEqual(body.get("name"), "oauth_credential")
        self.assertEqual(body.get("mode"), "OAUTH")

    def test_create_text(self):
        resp = self.credentials_api.create_text(
            name    = "text_credential",
            team_id = self.team_id,
            value   = "bar"
        )

        self._del_cred = resp.get("body").get("id")

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 201)
        self.assertEqual(body.get("name"), "text_credential")
        self.assertEqual(body.get("mode"), "TEXT")

    def test_get(self):
        resp = self.credentials_api.get(
            credential_id = self.cred_id
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("mode"), "TEXT")

    def test_update(self):
        update_id = time_ns() // 1000
        resp = self.credentials_api.update(
            mode          = "TEXT",
            credential_id = self.cred_id,
            name          = f"Updated at: {update_id}"
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("name"), f"Updated at: {update_id}")
        self.assertEqual(body.get("mode"), "TEXT")

    def test_list(self):
        resp = self.credentials_api.list()

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("user_credentials")), list)

    def test_delete(self):
        cred_to_delete = self.credentials_api.create_text(
            name    = "To delete",
            team_id = self.team_id,
            value   = "to delete"
        )

        cred_id = cred_to_delete.get("body").get("id")

        resp = self.credentials_api.delete(
            credential_id = cred_id
        )

        self.assertEqual(resp.get("status_code"), 204)