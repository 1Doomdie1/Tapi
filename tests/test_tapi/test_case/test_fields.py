import unittest
from os     import getenv
from dotenv import load_dotenv
from tapi   import CaseFieldsAPI


class test_CaseFieldsAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.case_id         = int(getenv("CASE_ID"))
        self.input_id        = int(getenv("CASE_INPUT_ID"))
        self.case_fields_api = CaseFieldsAPI(getenv("DOMAIN"), getenv("API_KEY"))

    def test_create(self):
        resp = self.case_fields_api.create(
            case_id  = self.case_id,
            input_id = self.input_id,
            value    = 1
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 201)
        self.assertEqual(body.get("field").get("value"), "1")

    def test_get(self):
        resp = self.case_fields_api.get(
            case_id  = self.case_id,
            field_id = int(getenv("CASE_FIELD_ID"))
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("case_id"), self.case_id)
        self.assertEqual(body.get("field").get("id"), int(getenv("CASE_FIELD_ID")))

    def test_update(self):
        resp = self.case_fields_api.update(
            case_id  = self.case_id,
            field_id = int(getenv("CASE_FIELD_ID")),
            value    = "2"
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("field").get("value"), "2")

    def test_list(self):
        resp = self.case_fields_api.list(
            case_id = self.case_id
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("fields")), list)

    def test_delete(self):
        field = self.case_fields_api.create(
            case_id  = self.case_id,
            input_id = int(getenv("CASE_DELETE_INPUT_ID")),
            value    = "5"
        )

        field_id = field.get("body").get("field").get("id")

        resp = self.case_fields_api.delete(
            case_id  = self.case_id,
            field_id = field_id
        )

        self.assertEqual(resp.get("status_code"), 204)

