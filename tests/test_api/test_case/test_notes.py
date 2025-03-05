import unittest
from os                            import getenv
from time                          import time_ns
from dotenv                        import load_dotenv
from tapi                          import CaseNotesAPI
from tapi.utils.types              import CaseNoteColor
from tapi.utils.testing_decorators import premium_feature
from tapi.utils.http               import disable_ssl_verification


class test_CaseMetadataAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()

        if getenv("SSL_VERIFICATION") == "0":
            disable_ssl_verification()

        self.case_id           = int(getenv("CASE_ID"))
        self.note_to_get_id    = int(getenv("CASE_NOTE_TO_GET"))
        self.note_to_update_id = int(getenv("CASE_NOTE_TO_UPDATE"))
        self.case_notes_api    = CaseNotesAPI(getenv("DOMAIN"), getenv("API_KEY"))

    @premium_feature
    @unittest.skip("Hitting cap limit")
    def test_create(self):
        resp = self.case_notes_api.create(
            case_id = self.case_id,
            title   = "Create Note Unit Test",
            content = "This is a comment created with Tapi :)",
            color   = CaseNoteColor.BLUE
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 201)
        self.assertEqual(body.get("title"), "Create Note Unit Test")
        self.assertEqual(body.get("content"), "This is a comment created with Tapi :)")
        self.assertEqual(body.get("color"), CaseNoteColor.BLUE)

    @premium_feature
    def test_get(self):
        resp = self.case_notes_api.get(
            case_id = self.case_id,
            note_id = self.note_to_get_id
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("title"), "Note to Get")

    @premium_feature
    def test_update(self):
        update_time = time_ns() // 1000

        resp = self.case_notes_api.update(
            case_id = self.case_id,
            note_id = self.note_to_update_id,
            title   = "Updated Title",
            color   = CaseNoteColor.MAGENTA,
            content = f"This content has been updated at: {update_time}"
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(body.get("title"), "Updated Title")
        self.assertEqual(body.get("color"), CaseNoteColor.MAGENTA)
        self.assertEqual(body.get("content"), f"This content has been updated at: {update_time}")

    @premium_feature
    def test_list(self):
        resp = self.case_notes_api.list(
            case_id = self.case_id
        )

        body = resp.get("body")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("notes")), list)

    @premium_feature
    @unittest.skip("Function runs fine but apparently there is a limit on how much metadata a case can have")
    def test_delete(self):
        note = self.case_notes_api.create(
            case_id = self.case_id,
            title   = "Delete me"
        )

        note_id = note.get("body").get("id")

        resp = self.case_notes_api.delete(
            case_id = self.case_id,
            note_id = note_id
        )

        self.assertEqual(resp.get("status_code"), 204)
