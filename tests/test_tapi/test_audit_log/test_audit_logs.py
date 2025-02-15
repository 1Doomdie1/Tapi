import unittest
from os               import getenv
from tapi             import AuditLogsAPI
from dotenv           import load_dotenv
from tapi.utils.types import AuditLogType

class test_AuditLogsAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.audt_logs_api = AuditLogsAPI(getenv("DOMAIN"), getenv("API_KEY"))

    def test_list(self):
        resp = self.audt_logs_api.list(
            operation_name = [
                AuditLogType.STORY_CREATION
            ],
            per_page       = 1
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("audit_logs")), list)
        self.assertEqual(body.get("audit_logs")[0].get("operation_name"), AuditLogType.STORY_CREATION)
