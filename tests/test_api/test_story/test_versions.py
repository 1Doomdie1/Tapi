import unittest
from os     import getenv
from dotenv import load_dotenv
from tapi   import VersionsAPI
from tapi.utils.testing_decorators import premium_test


class test_VersionsAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.version_id   = None
        self.story_id     = int(getenv("VERSIONS_API_STORY_ID"))
        self.versions_api = VersionsAPI(getenv("DOMAIN"), getenv("API_KEY"))

    def tearDown(self):
        if self.version_id:
            self.versions_api.delete(
                story_id   = self.story_id,
                version_id = self.version_id
            )

    @premium_test
    def test_create(self):
        resp = self.versions_api.create(
            story_id = self.story_id,
            name     = "Create Version Unit Test"
        )

        self.version_id = resp.get("body").get("story_version").get("id")

        self.assertEqual(resp.get("status_code"),                           200)
        self.assertEqual(resp.get("body").get("story_version").get("name"), "Create Version Unit Test")

    @premium_test
    def test_get(self):
        create_version = self.versions_api.create(
            story_id = self.story_id,
            name     = "Get Version Unit Test"
        )

        self.version_id = create_version.get("body").get("story_version").get("id")

        resp = self.versions_api.get(
            story_id   = self.story_id,
            version_id = self.version_id
        )

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(resp.get("body").get("story_version").get("name"), "Get Version Unit Test")
        self.assertIsNotNone(resp.get("body").get("story_version").get("export_file"))
        self.assertEqual(type(resp.get("body").get("story_version").get("export_file")), dict)

    @premium_test
    def test_update(self):
        create_version = self.versions_api.create(
            story_id = self.story_id,
            name     = "Update Version Unit Test"
        )

        self.version_id = create_version.get("body").get("story_version").get("id")

        resp = self.versions_api.update(
            name       = "New Version Unit Test Name",
            story_id   = self.story_id,
            version_id = self.version_id
        )

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(resp.get("body").get("story_version").get("name"), "New Version Unit Test Name")

    @premium_test
    def test_list(self):
        create_version = self.versions_api.create(
            story_id = self.story_id,
            name     = "List Version Unit Test"
        )

        self.version_id = create_version.get("body").get("story_version").get("id")

        resp = self.versions_api.list(
            story_id=self.story_id
        )

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(resp.get("body").get("story_versions")), list)
        self.assertGreaterEqual(len(resp.get("body").get("story_versions")), 1)

    @premium_test
    def test_delete(self):
        create_version = self.versions_api.create(
            story_id = self.story_id,
            name     = "Delete Version Unit Test"
        )

        version_id = create_version.get("body").get("story_version").get("id")

        resp = self.versions_api.delete(
            story_id   = self.story_id,
            version_id = version_id
        )

        self.assertEqual(resp.get("status_code"), 200)
