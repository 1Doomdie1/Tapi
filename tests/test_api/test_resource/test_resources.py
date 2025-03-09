import unittest
from os              import getenv
from time            import time_ns
from dotenv          import load_dotenv
from tapi            import ResourcesAPI
from tapi.utils.http import disable_ssl_verification


class test_ResourcesAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()

        if getenv("SSL_VERIFICATION") == "0":
            disable_ssl_verification()

        self._del_resource_id   = None
        self.team_id            = int(getenv("TEAM_ID"))
        self.resource_id        = int(getenv("RESOURCE_ID"))
        self.update_resource_id = int(getenv("UPDATE_RESOURCE_ID"))
        self.resources_api      = ResourcesAPI(getenv("DOMAIN"), getenv("API_KEY"))

    def tearDown(self):
        if self._del_resource_id:
            self.resources_api.delete(resource_id=self._del_resource_id)

    def test_create_text_resource(self):
        resp = self.resources_api.create(
            name    = "Unit Test Create Text",
            value   = "Resource Value",
            team_id = self.team_id
        )

        body = resp.get("body")
        self._del_resource_id = body.get("id")

        self.assertEqual(resp.get("status_code"), 201)
        self.assertEqual(body.get("name"), "Unit Test Create Text")
        self.assertEqual(body.get("value"), "Resource Value")
        self.assertEqual(body.get("read_access"), "TEAM")

    def test_create_json_resource(self):
        resp = self.resources_api.create(
            name    = "Unit Test Create Json",
            value   = '={"key":"value"}',
            team_id = self.team_id
        )

        body = resp.get("body")
        self._del_resource_id = body.get("id")

        self.assertEqual(resp.get("status_code"), 201)
        self.assertEqual(body.get("name"), "Unit Test Create Json")
        self.assertEqual(body.get("value"), '={"key":"value"}')
        self.assertEqual(body.get("read_access"), "TEAM")

    def test_get(self):
        resp = self.resources_api.get(
            resource_id = self.resource_id
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("name"), "my resource")
        self.assertEqual(body.get("value"), "some value")
        self.assertEqual(body.get("read_access"), "TEAM")

    def test_update(self):
        rng = time_ns() // 1000
        resp = self.resources_api.update(
            resource_id = self.update_resource_id,
            value       = f"Updated value: {rng}"
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("value"), f"Updated value: {rng}")

    def test_list(self):
        resp = self.resources_api.list()

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("global_resources")), list)

    def test_remove_element(self):
        resource = self.resources_api.create(
            name    = "Remove Element",
            value   = {"a":"1","b":"2"},
            team_id = self.team_id
        )

        resp = self.resources_api.remove_element(
            resource_id = resource.get("body").get("id"),
            key         = "a"
        )

        body = resource.get("body")
        self._del_resource_id = body.get("id")

        self.assertEqual(resp.get("body"), 1)
        self.assertEqual(resp.get("status_code"), 200)

    def test_append_element(self):
        resource = self.resources_api.create(
            name    = "Append Element",
            value   = "",
            team_id = self.team_id
        )

        resp = self.resources_api.append_element(
            resource_id = resource.get("body").get("id"),
            value       = "added element"
        )

        body = resource.get("body")
        self._del_resource_id = body.get("id")

        self.assertEqual(resp.get("body"), "added element")
        self.assertEqual(resp.get("status_code"), 200)

    def test_replace_element(self):
        resource = self.resources_api.create(
            name    = "Replace Element",
            value   = [1],
            team_id = self.team_id
        )

        resp = self.resources_api.replace_element(
            resource_id = resource.get("body").get("id"),
            value       = "new-value",
            index       = "0"
        )

        body = resource.get("body")
        self._del_resource_id = body.get("id")

        self.assertEqual(resp.get("body"), [1, 'new-value'])
        self.assertEqual(resp.get("status_code"), 200)

    def test_delete(self):
        resource = self.resources_api.create(
            name="Replace Element",
            value=[1],
            team_id=self.team_id
        )

        resp = self.resources_api.delete(
            resource_id=resource.get("body").get("id")
        )

        self.assertEqual(resp.get("status_code"), 204)
