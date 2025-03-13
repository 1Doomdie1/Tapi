import unittest
from os              import getenv
from time            import time_ns
from dotenv          import load_dotenv
from tapi            import TemplatesAPI
from tapi.utils.http import disable_ssl_verification


class test_TemplatesAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()

        if getenv("SSL_VERIFICATION") == "0":
            disable_ssl_verification()

        self._del_tem_id      = None
        self.template_id      = int(getenv("TEMPLATE_ID"))
        self.tem_to_update_id = int(getenv("TEMPLATE_TO_UPDATE_ID"))
        self.template_api     = TemplatesAPI(getenv("DOMAIN"), getenv("API_KEY"))

    def tearDown(self):
        if self._del_tem_id:
            self.template_api.delete(template_id = self._del_tem_id)

    def test_create(self):
        resp = self.template_api.create(
            name          = "Create Template Unit Test",
            description   = "Created With Tapi :)",
            agent_type    = "Agents::EventTransformationAgent",
            vendor        = "API",
            product       = "API",
            agent_options = {
                "mode": "extract",
                "matchers": [
                    {
                        "path": "{{.text}}",
                        "regexp": "\\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,4}\\b",
                        "to": "email_addresses"
                    },
                    {
                        "path": "{{.text}}",
                        "regexp": "https?:\\/\\/[\\S]+",
                        "to": "urls"
                    }
                ],
                "message": "This is an optional message"
            }
        )

        body = resp.get("body")
        self._del_tem_id = body.get("id")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("name"), "Create Template Unit Test")
        self.assertEqual(body.get("description"), "Created With Tapi :)")
        self.assertEqual(body.get("agent_type"), "Agents::EventTransformationAgent")
        self.assertEqual(body.get("vendor"), "API")
        self.assertEqual(body.get("product"), "API")

    def test_get(self):
        resp = self.template_api.get(
            template_id = self.template_id
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("id"), self.template_id)
        self.assertEqual(body.get("name"), "Template to get")
        self.assertEqual(body.get("description"), "")
        self.assertEqual(body.get("agent_type"), "Agents::EventTransformationAgent")
        self.assertEqual(body.get("vendor"), "")
        self.assertEqual(body.get("product"), "API")

    @unittest.skip("I am not exactly sure how this is suppose to work")
    def test_update(self):
        rng = time_ns() // 1000
        resp = self.template_api.update(
            template_id   = self.tem_to_update_id,
            name          = "Name+Update",
            description   = f"Updated at: {rng}",
            agent_type    = "Agents::EmailAgent",
            vendor        = "API",
            product       = "API",
            agent_options = {
                "mode": "extract",
                "matchers": [
                    {
                        "path": "{{.text}}",
                        "regexp": "\\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,4}\\b",
                        "to": "email_addresses"
                    },
                    {
                        "path": "{{.text}}",
                        "regexp": "https?:\\/\\/[\\S]+",
                        "to": "urls"
                    }
                ],
                "message": "This is an optional message+Update"
            }
        )

        self.assertEqual(resp.get("status_code"), 200)

    def test_list(self):
        resp = self.template_api.list()

        body = resp.get("body")
        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("admin/templates")), list)

    def test_delete(self):
        template = self.template_api.create(
            name          = "Delete Template Unit Test",
            description   = "Created With Tapi :)",
            agent_type    = "Agents::EventTransformationAgent",
            vendor        = "API",
            product       = "API",
            agent_options = {
                "mode": "extract",
                "matchers": [
                    {
                        "path": "{{.text}}",
                        "regexp": "\\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,4}\\b",
                        "to": "email_addresses"
                    },
                    {
                        "path": "{{.text}}",
                        "regexp": "https?:\\/\\/[\\S]+",
                        "to": "urls"
                    }
                ],
                "message": "This is an optional message"
            }
        )

        template_id = template.get("body").get("id")

        resp = self.template_api.delete(template_id = template_id)

        self.assertEqual(resp.get("status_code"), 204)
