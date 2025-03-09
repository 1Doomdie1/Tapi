import unittest
from os                            import getenv
from time                          import time_ns
from tapi                          import RecordTypesAPI
from dotenv                        import load_dotenv
from tapi.utils.testing_decorators import premium_feature
from tapi.utils.http               import disable_ssl_verification


class test_RecordTypesAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()

        if getenv("SSL_VERIFICATION") == "0":
            disable_ssl_verification()

        self._del_rec_t_id    = None
        self.team_id          = int(getenv("TEAM_ID"))
        self.record_type_id   = int(getenv("RECORD_TYPE_ID"))
        self.record_types_api = RecordTypesAPI(getenv("DOMAIN"), getenv("API_KEY"))

    def tearDown(self):
        if self._del_rec_t_id:
            self.record_types_api.delete(record_type_id = self._del_rec_t_id)

    @premium_feature
    def test_create(self):
        resp = self.record_types_api.create(
            name     = "Unit Test Type",
            team_id  = self.team_id,
            fields   = [
                {"name": "Column", "result_type": "TEXT"}
            ],
            editable = True
        )

        body = resp.get("body")
        self._del_rec_t_id = body.get("id")

        self.assertEqual(resp.get("status_code"), 201)
        self.assertEqual(body.get("name"), "Unit Test Type")
        self.assertEqual(body.get("editable"), True)
        self.assertEqual(body.get("ttl"), None)
        self.assertEqual(body.get("team_id"), self.team_id)

    @premium_feature
    def test_get(self):
        resp = self.record_types_api.get(
            record_type_id = self.record_type_id
        )

        body = resp.get("body")
        self.assertEqual(body, {
            "id": self.record_type_id,
            "name": "Record Unit Test",
            "editable": True,
            "ttl_days": None,
            "team_id": self.team_id,
            "record_fields": [
                {
                    "id": 3205,
                    "name": "TestFor",
                    "result_type": "TEXT",
                    "fixed_values": []
                }
            ],
            "default_record_fields": [
                {
                    "id": 3203,
                    "name": "Story name",
                    "result_type": "TEXT",
                    "fixed_values": []
                },
                {
                    "id": 3204,
                    "name": "Timestamp",
                    "result_type": "TIMESTAMP",
                    "fixed_values": []
                }
            ]
        }
    )

    @premium_feature
    def test_list(self):
        resp = self.record_types_api.list(
            team_id = self.team_id
        )

        body = resp.get("body")
        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(body.get("record_types")), list)

    @premium_feature
    def test_delete(self):
        rec_type = self.record_types_api.create(
            name     = "Unit Test Type",
            team_id  = self.team_id,
            fields   = [
                {"name": "Column", "result_type": "TEXT"}
            ],
            editable = True
        )

        rec_id = rec_type.get("body").get("id")

        resp = self.record_types_api.delete(record_type_id=rec_id)

        self.assertEqual(resp.get("status_code"), 204)