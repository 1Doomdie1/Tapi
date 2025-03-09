import unittest
from os                            import getenv
from time                          import time_ns
from tapi                          import RecordsAPI
from dotenv                        import load_dotenv
from tapi.utils.testing_decorators import premium_feature
from tapi.utils.http               import disable_ssl_verification


class test_NotesAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()

        if getenv("SSL_VERIFICATION") == "0":
            disable_ssl_verification()

        self._del_rec_id     = None
        self.record_id       = int(getenv("RECORD_ID"))
        self.record_field_id = getenv("RECORD_FIELD_ID")
        self.record_type_id  = int(getenv("RECORD_TYPE_ID"))
        self.update_rec_id   = int(getenv("UPDATE_RECORD_ID"))
        self.records_api     = RecordsAPI(getenv("DOMAIN"), getenv("API_KEY"))

    def tearDown(self):
        if self._del_rec_id:
            self.records_api.delete(record_id=self._del_rec_id)

    @premium_feature
    def test_create(self):
        resp = self.records_api.create(
            record_type_id = self.record_type_id,
            field_values   = [
                {"field_id": self.record_field_id, "value": "Test value"}
            ]
        )

        body = resp.get("body")
        self._del_rec_id = body.get("id")

        self.assertEqual(resp.get("status_code"), 201)
        self.assertEqual(body.get("record_type"), {"id": 1419, "name": "Record Unit Test"})
        self.assertEqual(body.get("case_ids"), [])
        self.assertEqual(body.get("test_mode"), False)

    @premium_feature
    def test_get(self):
        resp = self.records_api.get(
            record_id = self.record_id
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("id"), self.record_id)
        self.assertEqual(body.get("created_at"), "2025-02-02T22:51:16Z")
        self.assertEqual(body.get("updated_at"), "2025-02-02T22:51:16Z")
        self.assertEqual(body.get("story"), None)
        self.assertEqual(body.get("story_run_guid"), None)
        self.assertEqual(body.get("record_type"), {"id": 1419, "name": "Record Unit Test"})
        self.assertEqual(body.get("records"), [
            {"name": "TestFor", "value": "Case Record 1"},
            {"name": "Timestamp", "value": "2025-02-02 22:51:16"},
            {"name": "Story name", "value": None}
        ])
        self.assertEqual(body.get("parent_id"), None)
        self.assertEqual(body.get("child_record_ids"), [])
        self.assertEqual(body.get("case_ids"), [26])
        self.assertEqual(body.get("parent_record_result_set"), {"id": None})
        self.assertEqual(body.get("parent_record"), {"id": None})
        self.assertEqual(body.get("child_record_result_sets"), [])
        self.assertEqual(body.get("child_records"), [])
        self.assertEqual(body.get("record_artifacts"), [])
        self.assertEqual(body.get("result"), {
            "TestFor": "Case Record 1",
            "Timestamp": "2025-02-02 22:51:16",
            "Story name": None
        })

    @premium_feature
    def test_list(self):
        resp = self.records_api.list(
            record_type_id = self.record_type_id
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("record_results")), list)
        self.assertEqual(len(body.get("record_results")), 2)

    @premium_feature
    def test_update(self):
        rng = time_ns() // 1000
        resp = self.records_api.update(
            record_id    = self.update_rec_id,
            field_values = [
                {"field_id": self.record_field_id, "value": f"Updated value: {rng}"}
            ]
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertIn({"field_id": "3205", "name": "TestFor", "value": f"Updated value: {rng}"}, body.get("records"))

    @premium_feature
    def test_delete(self):
        rec = self.records_api.create(
            record_type_id = self.record_type_id,
            field_values   = [
                {"field_id": self.record_field_id, "value": "Test value"}
            ]
        )
        rec_id = rec.get("body").get("id")
        resp = self.records_api.delete(record_id=rec_id)

        self.assertEqual(resp.get("status_code"), 204)