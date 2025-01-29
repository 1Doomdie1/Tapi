import unittest
from os          import getenv
from dotenv      import load_dotenv
from tapi        import CaseActionsAPI
from utils.types import CaseActionType


class test_CaseActionsAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.case_id         = int(getenv("CASE_ID"))
        self.action_id       = None
        self.case_action_api = CaseActionsAPI(getenv("DOMAIN"), getenv("API_KEY"))

    def tearDown(self):
        if self.action_id:
            self.case_action_api.delete(
                case_id = self.case_id,
                id      = self.action_id
            )

    def test_create(self):
        resp = self.case_action_api.create(
            case_id     = self.case_id,
            url         = "https://example.tines.com",
            label       = "Create Action Unit Test",
            action_type = CaseActionType.PAGE,
            action_text = "Open"
        )
        body = resp.get("body")
        self.action_id = body.get("id")

        self.assertEqual(resp.get("status_code"), 201)
        self.assertEqual(body.get("url"), "https://example.tines.com")
        self.assertEqual(body.get("label"), "Create Action Unit Test")
        self.assertEqual(body.get("action_type"), CaseActionType.PAGE)
        self.assertEqual(body.get("action_text"), "Open")

    def test_get(self):
        action = self.case_action_api.create(
            case_id     = self.case_id,
            url         = "https://example.tines.com",
            label       = "Get Action Unit Test",
            action_type = CaseActionType.PAGE,
            action_text = "Open"
        )

        self.action_id = action.get("body").get("id")

        resp = self.case_action_api.get(
            case_id = self.case_id,
            id      = self.action_id
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("url"), "https://example.tines.com")
        self.assertEqual(body.get("label"), "Get Action Unit Test")
        self.assertEqual(body.get("action_type"), CaseActionType.PAGE)
        self.assertEqual(body.get("action_text"), "Open")

    def test_update(self):
        action = self.case_action_api.create(
            case_id=self.case_id,
            url         = "https://example.tines.com",
            label       = "Update Action Unit Test",
            action_type = CaseActionType.PAGE,
            action_text = "Open"
        )

        self.action_id = action.get("body").get("id")

        resp = self.case_action_api.update(
            case_id     = self.case_id,
            id          = self.action_id,
            url         = "https://google.com",
            label       = "New Updated Action Unit Test",
            action_text = "GoTo"
        )

        body = resp.get("body")
        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("url"), "https://google.com")
        self.assertEqual(body.get("label"), "New Updated Action Unit Test")
        self.assertEqual(body.get("action_text"), "GoTo")

    def test_list(self):
        action = self.case_action_api.create(
            case_id     = self.case_id,
            url         = "https://example.tines.com",
            label       = "List Action Unit Test",
            action_type = CaseActionType.PAGE,
            action_text = "Open"
        )

        self.action_id = action.get("body").get("id")

        resp = self.case_action_api.list(
            case_id = self.case_id
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("actions")), list)
        self.assertGreaterEqual(len(body.get("actions")), 1)

    def test_delete(self):
        action = self.case_action_api.create(
            case_id     = self.case_id,
            url         = "https://example.tines.com",
            label       = "Delete Action Unit Test",
            action_type = CaseActionType.PAGE,
            action_text = "Open"
        )

        action_id = action.get("body").get("id")

        resp = self.case_action_api.delete(
            case_id = self.case_id,
            id      = action_id
        )

        self.assertEqual(resp.get("status_code"), 204)

    def tests_batch_update(self):
        actions = [
            {
                "url": "https://example.tines.com",
                "label": "Complete request",
                "action_type": "page",
                "action_text": "Open"
            },
            {
                "url": "https://tenant.tines.com/webhook/abc",
                "label": "Claim case",
                "action_type": "webhook",
                "action_text": "Run"
            }
        ]

        resp = self.case_action_api.batch_update(
            case_id = self.case_id,
            actions = actions
        )

        self.assertEqual(resp.get("status_code"), 200)


