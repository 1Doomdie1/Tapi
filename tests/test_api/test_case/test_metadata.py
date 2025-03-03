import unittest
from os     import getenv
from time   import time_ns
from dotenv import load_dotenv
from tapi   import CaseMetadataAPI
from tapi.utils.testing_decorators import premium_test


class test_CaseMetadataAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.case_id           = int(getenv("CASE_ID"))
        self.case_metadata_api = CaseMetadataAPI(getenv("DOMAIN"), getenv("API_KEY"))

    @premium_test
    def test_create(self):
        rng = time_ns() // 1000
        resp = self.case_metadata_api.create(
            case_id  = self.case_id,
            metadata = {f"key_{rng}": "Create Metadata Unit Test"}
        )

        self.assertEqual(resp.get("status_code"), 201)

    @premium_test
    def test_get(self):
        resp = self.case_metadata_api.get(
            case_id = self.case_id,
            key     = "test"
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertIsNotNone(body.get("metadata").get("test"))

    @premium_test
    def test_update(self):
        resp = self.case_metadata_api.update(
            case_id  = self.case_id,
            metadata = {"name": "New Value Unit Test"}
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("metadata").get("name"), "New Value Unit Test")

    @premium_test
    def test_list(self):
        resp = self.case_metadata_api.list(
            case_id = self.case_id
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("metadata")), dict)

    @premium_test
    def test_delete(self):
        self.case_metadata_api.create(case_id = self.case_id, metadata={"to_delete": "delete me plz"})

        resp = self.case_metadata_api.delete(
            case_id       = self.case_id,
            metadata_keys = ["to_delete"]
        )

        self.assertEqual(resp.get("status_code"), 204)
