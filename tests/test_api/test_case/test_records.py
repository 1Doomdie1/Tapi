import unittest
from os     import getenv
from dotenv import load_dotenv
from tapi   import CaseRecordsAPI
from tapi.utils.testing_decorators import premium_test


class test_CaseFilesAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.case_id          = int(getenv("CASE_ID"))
        self.record_id        = int(getenv("CASE_RECORD_ID"))
        self.delete_record_id = int(getenv("CASE_DELETE_RECORD_ID"))
        self.case_records_api = CaseRecordsAPI(getenv("DOMAIN"), getenv("API_KEY"))

    @premium_test
    def test_create(self):
        resp = self.case_records_api.create(
            case_id   = self.case_id,
            record_id = self.record_id
        )

        self.assertEqual(resp.get("status_code"), 201)

    @premium_test
    def test_get(self):
        resp = self.case_records_api.get(
            case_id   = self.case_id,
            record_id = self.record_id
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("record").get("id"), self.record_id)
        self.assertEqual(body.get("record").get("record_type"), {"id": 1419, "name": "Record Unit Test"})

    @premium_test
    def test_list(self):
        resp = self.case_records_api.list(
            case_id = self.case_id
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("records")), list)

    @premium_test
    def test_delete(self):
        record = self.case_records_api.create(
            case_id   = self.case_id,
            record_id = self.delete_record_id
        )

        record_id = record.get("body").get("record").get("id")

        resp = self.case_records_api.delete(
            case_id   = self.case_id,
            record_id = record_id
        )

        self.assertEqual(resp.get("status_code"), 204)