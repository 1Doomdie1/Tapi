import unittest
from os                            import getenv
from dotenv                        import load_dotenv
from tapi                          import AuditLogsAPI
from tapi.utils.types              import AuditLogType
from tapi.utils.testing_decorators import premium_feature
from tapi.utils.http               import disable_ssl_verification

class test_AuditLogsAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()

        if getenv("SSL_VERIFICATION") == "0":
            disable_ssl_verification()

        self.audt_logs_api = AuditLogsAPI(getenv("DOMAIN"), getenv("API_KEY"))

    @premium_feature
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
