import unittest
from os                            import getenv
from dotenv                        import load_dotenv
from tapi                          import CaseFilesAPI
from tapi.utils.testing_decorators import premium_feature
from tapi.utils.http               import disable_ssl_verification


class test_CaseFilesAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()

        if getenv("SSL_VERIFICATION") == "0":
            disable_ssl_verification()

        self.case_id        = int(getenv("CASE_ID"))
        self.case_files_api = CaseFilesAPI(getenv("DOMAIN"), getenv("API_KEY"))

    @premium_feature
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

    @premium_feature
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

    @premium_feature
    def test_list(self):
        resp = self.case_files_api.list(
            case_id=self.case_id
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("files")), list)

    @premium_feature
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

    # @premium_feature
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
