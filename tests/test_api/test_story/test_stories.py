import unittest
from os              import getenv
from tapi            import StoriesAPI
from dotenv          import load_dotenv
from tapi.utils.http import disable_ssl_verification


class test_StoriesAPI(unittest.TestCase):

    def setUp(self):
        load_dotenv()

        if getenv("SSL_VERIFICATION") == "0":
            disable_ssl_verification()

        self.stories_api = StoriesAPI(getenv("DOMAIN"), getenv("API_KEY"))
        self.team_id     = int(getenv("TEAM_ID"))
        self.story_id    = None

    def tearDown(self):
        self.stories_api.delete(self.story_id)

    def test_create(self):
        resp = self.stories_api.create(
            team_id     = self.team_id,
            name        = "Unit Test Story Name",
            description = "Unit Test Story Description",
            disabled    = True
        )

        self.story_id = resp.get("body").get("id")

        self.assertEqual(resp.get("status_code"), 201)
        self.assertEqual(resp.get("body").get("name"), "Unit Test Story Name")
        self.assertEqual(resp.get("body").get("description"), "Unit Test Story Description")
        self.assertEqual(resp.get("status_code"), 201)
        self.assertTrue(resp.get("body").get("disabled"))

    def test_get(self):
        create_new_story = self.stories_api.create(
            team_id = self.team_id,
            name    = "Unit Test Story Name"
        )

        self.story_id = create_new_story.get("body").get("id")
        get_story = self.stories_api.get(self.story_id)

        self.assertEqual(get_story.get("status_code"), 200)
        self.assertEqual(get_story.get("body").get("name"), "Unit Test Story Name")

    def test_get_when_story_id_doesnt_exist(self):
        get_story = self.stories_api.get(123)
        self.assertEqual(get_story.get("status_code"), 404)

    def test_update(self):
        create_new_story = self.stories_api.create(
            team_id = self.team_id,
            name    = "Unit Test Story Name"
        )

        self.story_id = create_new_story.get("body").get("id")
        resp1 = self.stories_api.update(story_id = self.story_id, name        = "Updated Unit Test Name")
        resp2 = self.stories_api.update(story_id = self.story_id, description = "Updated Unit Test description")
        resp3 = self.stories_api.update(story_id = self.story_id, disabled    = True)

        self.assertEqual(resp1.get("status_code"), 200)
        self.assertEqual(resp2.get("status_code"), 200)
        self.assertEqual(resp3.get("status_code"), 200)

        self.assertEqual(resp1.get("body").get("name"), "Updated Unit Test Name")
        self.assertEqual(resp2.get("body").get("description"), "Updated Unit Test description")
        self.assertTrue(resp3.get("body").get("disabled"))

    def test_list(self):
        create_new_story = self.stories_api.create(
            team_id=self.team_id,
            name="Unit Test Story Name"
        )
        self.story_id = create_new_story.get("body").get("id")

        page_size = 10
        resp = self.stories_api.list(per_page=page_size)

        self.assertEqual(resp.get("status_code"), 200)
        self.assertLessEqual(len(resp.get("body").get("stories")), page_size)

    def test_delete(self):
        create_new_story = self.stories_api.create(
            team_id=self.team_id,
            name="Unit Test Story Name"
        )

        story_id = create_new_story.get("body").get("id")
        resp = self.stories_api.delete(story_id=story_id)

        self.assertEqual(resp.get("status_code"), 204)

    def test_batch_delete(self):
        story_1 = self.stories_api.create(
            team_id=self.team_id,
            name="Unit Test Story Name 1"
        )

        story_2 = self.stories_api.create(
            team_id=self.team_id,
            name="Unit Test Story Name 2"
        )

        ids = [
            story_1.get("body").get("id"),
            story_2.get("body").get("id")
        ]

        resp = self.stories_api.batch_delete(story_ids=ids)

        self.assertEqual(resp.get("status_code"), 204)

    def test_export(self):
        create_new_story = self.stories_api.create(
            team_id=self.team_id,
            name="Unit Test Story Name"
        )

        self.story_id = create_new_story.get("body").get("id")

        resp = self.stories_api.export(story_id=self.story_id)

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(type(resp.get("body")), dict)
        self.assertEqual(resp.get("body").get("name"), "Unit Test Story Name")

    def test_import(self):
        story_data = {
            "schema_version":                                26,
            "standard_lib_version":                          70,
            "action_runtime_version":                        20,
            "name":                                          "Some Name",
            "description":                                   None,
            "guid":                                          "0a21b58a06fb2c05fa10e7552a2b2007",
            "slug":                                          "some_name",
            "agents":                                        [],
            "diagram_notes":                                 [],
            "links":                                         [],
            "diagram_layout":                                "{}",
            "send_to_story_enabled":                         False,
            "entry_agent_guid":                              None,
            "exit_agent_guids":                              [],
            "api_entry_action_guids":                        [],
            "api_exit_action_guids":                         [],
            "keep_events_for":                               86400,
            "reporting_status":                              True,
            "send_to_story_access":                          None,
            "story_library_metadata":                        {},
            "parent_only_send_to_story":                     False,
            "monitor_failures":                              False,
            "send_to_stories":                               [],
            "recipients":                                    [],
            "synchronous_webhooks_enabled":                  False,
            "send_to_story_access_source":                   0,
            "send_to_story_skill_use_requires_confirmation": True,
            "pages":                                         [],
            "tags":                                          [],
            "time_saved_unit":                               "minutes",
            "time_saved_value":                              0,
            "origin_story_identifier":                       "cloud:49d3ae03e2031ffb0058416a2ec95c06:0a21b58a06fb2c05fa10e7552a2b2007",
            "integration_product":                           None,
            "integration_vendor":                            None,
            "llm_product_instructions":                      "",
            "exported_at":                                   "2025-01-26T00:15:07Z",
            "icon":                                          ":hourglass:",
            "integrations":                                  []
        }

        resp = self.stories_api.import_(
            new_name = "Unit Testing Story Name",
            data     = story_data,
            team_id  = self.team_id
        )

        self.story_id = resp.get("body").get("id")

        self.assertEqual(resp.get("status_code"), 200)
        self.assertEqual(resp.get("body").get("name"), "Unit Testing Story Name")
        self.assertEqual(resp.get("body").get("team_id"), self.team_id)
