import unittest
from os     import getenv
from dotenv import load_dotenv
from tapi   import CaseFilesAPI


class test_CaseFilesAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.case_id        = int(getenv("CASE_ID"))
        self.case_files_api = CaseFilesAPI(getenv("DOMAIN"), getenv("API_KEY"))

    def test_create(self):
        resp = self.case_files_api.create(
            case_id       = self.case_id,
            filename      = "Create File Unit Test.txt",
            file_contents = "aGVsbyB0aGVyZQ==",
            value         = "Testing comment"
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 201)
        self.assertEqual(body.get("activity_type"), "FILE_ATTACHED_AND_COMMENTED")
        self.assertEqual(body.get("value"), "Testing comment")
        self.assertEqual(body.get("file").get("filename"), "Create File Unit Test.txt")

    def test_get(self):
        resp = self.case_files_api.get(
            case_id = self.case_id,
            file_id = int(getenv("CASE_FILE_ID"))
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("id"), int(getenv("CASE_FILE_ID")))
        self.assertEqual(body.get("case_id"), self.case_id)
        self.assertEqual(body.get("value"), "Testing comment")
        self.assertEqual(body.get("file").get("filename"), "Create File Unit Test")

    def test_list(self):
        resp = self.case_files_api.list(
            case_id=self.case_id
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("files")), list)

    def test_delete(self):
        file = self.case_files_api.create(
            case_id       = self.case_id,
            filename      = "Download File Unit Test",
            file_contents = "QmFzZTY0IGVuY29kZWQgZlsZSBjb250ZW50cw==",
            value         = "Testing comment"
        )

        file_id = file.get("body").get("id")

        resp = self.case_files_api.delete(
            case_id = self.case_id,
            file_id = file_id
        )

        self.assertEqual(resp.get("status_code"), 204)

    # Endpoint need to be fixed by Tines, first
    # def test_download(self):
    #     resp = self.case_files_api.download(
    #         case_id = self.case_id,
    #         file_id = int(getenv("CASE_FILE_ID"))
    #     )
    #
    #     body = resp.get("body")
    #
    #     self.assertEqual(resp.get("status_code"), 200)
    #     self.assertEqual(body.get("filename"), "Create File Unit Test")
