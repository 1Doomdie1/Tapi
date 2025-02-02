import unittest
from os     import getenv
from dotenv import load_dotenv
from tapi   import LinkedCasesAPI


class test_LinkedCasesAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.case_id           = int(getenv("CASE_ID"))
        self.case_to_link_id_1 = int(getenv("CASE_TO_LINK_ID_1"))
        self.case_to_link_id_2 = int(getenv("CASE_TO_LINK_ID_2"))
        self.linked_cases_api = LinkedCasesAPI(getenv("DOMAIN"), getenv("API_KEY"))

    def test_create(self):
        resp = self.linked_cases_api.create(
            case_id = self.case_id,
            id      = self.case_to_link_id_1
        )

        self.assertEqual(resp.get("status_code"), 201)

    def test_list(self):
        resp = self.linked_cases_api.list(
            case_id = self.case_id
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("linked_cases")), list)

    def test_delete(self):
        resp = self.linked_cases_api.delete(
            case_id = self.case_id,
            linked_case_id = self.case_to_link_id_1
        )

        self.assertEqual(resp.get("status_code"), 204)

    def test_batch_delete(self):
        ids = [
            self.case_to_link_id_1,
            self.case_to_link_id_2
        ]

        for case_to_link_id in ids:
            self.linked_cases_api.create(case_id = self.case_id, id = case_to_link_id)

        resp = self.linked_cases_api.batch_delete(
            case_id = self.case_id,
            ids     = ids
        )

        self.assertEqual(resp.get("status_code"), 201)


