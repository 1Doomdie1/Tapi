import unittest
from os          import getenv
from random      import randint
from tapi        import NotesAPI
from dotenv      import load_dotenv


class test_NotesAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.note_id   = int(getenv("NOTE_ID"))
        self.story_id  = int(getenv("NOTE_STORY_ID"))
        self.notes_api = NotesAPI(getenv("DOMAIN"), getenv("API_KEY"))

    def test_create(self):
        pos = {
            "x": randint(-100, 100),
            "y": randint(-100, 100)
        }

        resp = self.notes_api.create(
            content  = "# Hello From Tapi\nMy random String :joy:",
            story_id = self.story_id,
            position = pos
        )

        self.assertEqual(resp.get("status_code"), 201)

    def test_get(self):
        resp = self.notes_api.get(
            note_id = self.note_id
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("id"), self.note_id)
        self.assertEqual(body.get("story_id"), self.story_id)
        self.assertEqual(body.get("group_id"), None)

    def test_update(self):
        resp = self.notes_api.update(
            note_id = self.note_id,
            content = f"This is the updated content: {randint(0, 1000)}"
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("id"), self.note_id)
        self.assertTrue(body.get("content").startswith("This is the updated content: "))

    def test_list(self):
        resp = self.notes_api.list()

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("annotations")), list)

    def test_delete(self):
        note = self.notes_api.create(
            content  = "# TO DELETE",
            story_id = self.story_id
        )

        note_id = note.get("body").get("id")

        resp = self.notes_api.delete(
            note_id = note_id
        )

        self.assertEqual(resp.get("status_code"), 204)