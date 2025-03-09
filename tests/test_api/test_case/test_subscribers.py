import unittest
from os                            import getenv
from dotenv                        import load_dotenv
from tapi.utils.testing_decorators import premium_feature
from tapi                          import CaseSubscribersAPI
from tapi.utils.http               import disable_ssl_verification


class test_CaseFilesAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()

        if getenv("SSL_VERIFICATION") == "0":
            disable_ssl_verification()

        self.case_id              = int(getenv("CASE_ID"))
        self.case_sub_email       = getenv("CASE_SUBSCRIBER_EMAIL")
        self.case_subscribers_api = CaseSubscribersAPI(getenv("DOMAIN"), getenv("API_KEY"))

    @premium_feature
    def test_create(self):
        resp = self.case_subscribers_api.create(
            case_id    = self.case_id,
            user_email = self.case_sub_email
        )

        self.assertEqual(resp.get("status_code"), 201)

    @premium_feature
    def test_list(self):
        resp = self.case_subscribers_api.list(
            case_id = self.case_id
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("subscribers")), list)

    @premium_feature
    def test_delete(self):
        subscriber = self.case_subscribers_api.create(
            case_id    = self.case_id,
            user_email = self.case_sub_email
        )

        user_id = subscriber.get("body").get("id")

        resp = self.case_subscribers_api.delete(
            case_id       = self.case_id,
            subscriber_id = user_id
        )

        self.assertEqual(resp.get("status_code"), 204)

    @premium_feature
    def test_batch_create(self):
        resp = self.case_subscribers_api.batch_create(
            case_id = self.case_id,
            user_emails = [self.case_sub_email]
        )

        self.assertEqual(resp.get("status_code"), 201)
