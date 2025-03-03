import unittest
from os     import getenv
from dotenv import load_dotenv
from tapi   import ChangeRequestAPI
from tapi.utils.testing_decorators import premium_test


class test_ChangeRequestAPI(unittest.TestCase):

    def setUp(self):
        load_dotenv()
        self.team_id            = getenv("TEAM_ID")
        self.story_id           = int(getenv("CHANGE_REQUEST_STORY_ID"))
        self.change_request_api = ChangeRequestAPI(getenv("DOMAIN"), getenv("API_KEY"))
        self.change_request_id  = None

    def tearDown(self):
        if self.change_request_id: self.change_request_api.cancel(
            story_id          = self.story_id,
            change_request_id = self.change_request_id
        )

    @premium_test
    def test_create(self):
        resp = self.change_request_api.create(
            story_id    = self.story_id,
            title       = "Create Change Request Test Title",
            description = "Created with Tapi :)"
        )

        self.change_request_id = resp.get("body").get("change_request").get("id")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(resp.get("body").get("id")), int)
        self.assertEqual(type(resp.get("body").get("change_request")), dict)

    @premium_test
    def test_approve(self):
        request = self.change_request_api.create(
            story_id    = self.story_id,
            title       = "Approve Change Request Test Title",
            description = "Created with Tapi :)"
        )

        request_id = request.get("body").get("change_request").get("id")

        resp = self.change_request_api.approve(
            story_id          = self.story_id,
            change_request_id = request_id
        )

        self.change_request_id = request.get("body").get("change_request").get("id")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertIsNotNone(resp.get("body").get("change_request"))
        self.assertIsNotNone(resp.get("body").get("id"))
        self.assertEqual(resp.get("body").get("change_request").get("status"), "APPROVED")

    @premium_test
    def test_cancel(self):
        request = self.change_request_api.create(
            story_id    = self.story_id,
            title       = "Cancel Change Request Test Title",
            description = "Created with Tapi :)"
        )

        request_id = request.get("body").get("change_request").get("id")

        resp = self.change_request_api.cancel(
            story_id          = self.story_id,
            change_request_id = request_id
        )
        self.assertEqual(resp.get("status_code"), 200)
        self.assertIsNone(resp.get("body").get("change_request"))
        self.assertIsNotNone(resp.get("body").get("id"))
        self.assertEqual(type(resp.get("body").get("id")), int)

    @premium_test
    def test_promote(self):
        create_request = self.change_request_api.create(
            story_id    = self.story_id,
            title       = "Promote Change Request Test Title",
            description = "Created with Tapi :)"
        )

        create_request_id = create_request.get("body").get("change_request").get("id")

        approve_request = self.change_request_api.approve(
            story_id          = self.story_id,
            change_request_id = create_request_id
        )

        approve_request_id = approve_request.get("body").get("change_request").get("id")

        resp = self.change_request_api.promote(
            story_id          = self.story_id,
            change_request_id = approve_request_id
        )

        self.assertEqual(resp.get("status_code"),200)
        self.assertEqual(resp.get("body").get("name"), "Testing")
        self.assertEqual(resp.get("body").get("id"), self.story_id)

    @premium_test
    def test_view(self):
        resp = self.change_request_api.view(
            story_id = self.story_id
        )

        self.assertEqual(resp.get("status_code"),200)
        if resp.get("body").get("change_request"):
            self.assertIsNotNone(resp.get("body").get("change_request").get("id"))
            self.assertEqual(type(resp.get("body").get("change_request").get("story_diff")), list)