import unittest
from os              import getenv
from time            import time_ns
from tapi            import FoldersAPI
from dotenv          import load_dotenv
from tapi.utils.http import disable_ssl_verification


class test_EventsAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()

        if getenv("SSL_VERIFICATION") == "0":
            disable_ssl_verification()

        self._del_folder_id = None
        self.folder_id      = int(getenv("FOLDER_ID"))
        self.team_id        = int(getenv("TEAM_ID"))
        self.folders_api    = FoldersAPI(getenv("DOMAIN"), getenv("API_KEY"))

    def tearDown(self):
        if self._del_folder_id:
            self.folders_api.delete(self._del_folder_id)

    def test_create(self):
        resp = self.folders_api.create(
            name         = "Unit Test Folder",
            content_type = "STORY",
            team_id      = self.team_id
        )

        body = resp.get("body")
        self._del_folder_id = body.get("id")

        self.assertEqual(resp.get("status_code"), 201)
        self.assertEqual(body.get("name"), "Unit Test Folder")
        self.assertEqual(body.get("content_type"), "STORY")
        self.assertEqual(body.get("team_id"), self.team_id)
        self.assertEqual(body.get("size"), 0)

    def test_get(self):
        resp = self.folders_api.get(folder_id = self.folder_id)

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("id"), self.folder_id)
        self.assertEqual(body.get("name"), "WDWWT")
        self.assertEqual(body.get("content_type"), "STORY")
        self.assertEqual(body.get("team_id"), self.team_id)

    def test_update(self):
        rng = time_ns() // 1000
        folder = self.folders_api.create(
            name         = "To change",
            content_type = "STORY",
            team_id      = self.team_id
        )

        resp = self.folders_api.update(
            folder_id = folder.get("body").get("id"),
            name      = f"Updated At: {rng}"
        )

        body                = resp.get("body")
        self._del_folder_id = body.get("id")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("name"), f"Updated At: {rng}")
        self.assertEqual(body.get("content_type"), "STORY")
        self.assertEqual(body.get("team_id"), self.team_id)
        self.assertEqual(body.get("size"), 0)

    def test_list(self):
        resp = self.folders_api.list()

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("folders")), list)

    def test_delete(self):
        folder = self.folders_api.create(
            name         = "To Delete",
            content_type = "STORY",
            team_id      = self.team_id
        )

        resp = self.folders_api.delete(folder_id=folder.get("body").get("id"))

        self.assertEqual(resp.get("status_code"), 204)
