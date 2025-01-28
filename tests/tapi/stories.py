import unittest

from os     import getenv
from dotenv import load_dotenv
from tapi   import RunsAPI, StoriesAPI, VersionsAPI, ChangeRequestAPI


class test_StoriesAPI(unittest.TestCase):

    def setUp(self):
        load_dotenv()
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
        assert resp.get("status_code")             == 201
        assert resp.get("body").get("name")        == "Unit Test Story Name"
        assert resp.get("body").get("description") == "Unit Test Story Description"
        assert resp.get("body").get("disabled")    == True

    def test_get(self):
        create_new_story = self.stories_api.create(
            team_id = self.team_id,
            name    = "Unit Test Story Name"
        )

        self.story_id = create_new_story.get("body").get("id")
        get_story = self.stories_api.get(self.story_id)

        assert get_story.get("status_code")      == 200
        assert get_story.get("body").get("name") == "Unit Test Story Name"

    def test_get_when_story_id_doesnt_exist(self):
        get_story = self.stories_api.get(123)
        assert get_story.get("status_code") == 404

    def test_update(self):
        create_new_story = self.stories_api.create(
            team_id = self.team_id,
            name    = "Unit Test Story Name"
        )

        self.story_id = create_new_story.get("body").get("id")
        resp1 = self.stories_api.update(story_id = self.story_id, name        = "Updated Unit Test Name")
        resp2 = self.stories_api.update(story_id = self.story_id, description = "Updated Unit Test description")
        resp3 = self.stories_api.update(story_id = self.story_id, disabled    = True)

        assert resp1.get("status_code") == 200
        assert resp2.get("status_code") == 200
        assert resp3.get("status_code") == 200

        assert resp1.get("body").get("name")        == "Updated Unit Test Name"
        assert resp2.get("body").get("description") == "Updated Unit Test description"
        assert resp3.get("body").get("disabled")    == True

    def test_list(self):
        create_new_story = self.stories_api.create(
            team_id=self.team_id,
            name="Unit Test Story Name"
        )
        self.story_id = create_new_story.get("body").get("id")

        page_size = 10
        resp = self.stories_api.list(per_page=page_size)

        assert resp.get("status_code") == 200
        assert len(resp.get("body").get("stories")) <= page_size

    def test_delete(self):
        create_new_story = self.stories_api.create(
            team_id=self.team_id,
            name="Unit Test Story Name"
        )

        story_id = create_new_story.get("body").get("id")
        resp = self.stories_api.delete(story_id=story_id)

        assert resp.get("status_code") == 204

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

        assert resp.get("status_code") == 204

    def test_export(self):
        create_new_story = self.stories_api.create(
            team_id=self.team_id,
            name="Unit Test Story Name"
        )

        self.story_id = create_new_story.get("body").get("id")

        resp = self.stories_api.export(story_id=self.story_id)

        assert resp.get("status_code")      == 200
        assert type(resp.get("body"))       == dict
        assert resp.get("body").get("name") == "Unit Test Story Name"

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

        assert resp.get("status_code")         == 200
        assert resp.get("body").get("name")    == "Unit Testing Story Name"
        assert resp.get("body").get("team_id") == self.team_id

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

    def test_create(self):
        resp = self.change_request_api.create(
            story_id    = self.story_id,
            title       = "Create Change Request Test Title",
            description = "Created with Tapi :)"
        )

        self.change_request_id = resp.get("body").get("change_request").get("id")

        assert resp.get("status_code")                      == 200
        assert type(resp.get("body").get("id"))             == int
        assert type(resp.get("body").get("change_request")) == dict

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

        assert resp.get("status_code")                              == 200
        assert resp.get("body").get("change_request")               is not None
        assert resp.get("body").get("id")                           is not None
        assert resp.get("body").get("change_request").get("status") == "APPROVED"

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

        assert resp.get("status_code")                == 200
        assert resp.get("body").get("change_request") is None
        assert resp.get("body").get("id")             is not None
        assert type(resp.get("body").get("id"))       == int

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

        assert resp.get("status_code")      == 200
        assert resp.get("body").get("name") == "Testing"
        assert resp.get("body").get("id")   == self.story_id

    def test_view(self):
        resp = self.change_request_api.view(
            story_id = self.story_id
        )

        assert resp.get("status_code") == 200
        if resp.get("body").get("change_request"):
            assert resp.get("body").get("change_request").get("id")               is not None
            assert type(resp.get("body").get("change_request").get("story_diff")) == list

class test_RunsAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.story_id       = int(getenv("RUNS_API_STORY_ID"))
        self.runs_api       = RunsAPI(getenv("DOMAIN"), getenv("API_KEY"))
        self.story_run_guid = getenv("RUNS_API_STORY_RUN_GUID")

    def test_events(self):
        resp = self.runs_api.events(
            story_id       = self.story_id,
            story_run_guid = self.story_run_guid
        )

        assert resp.get("status_code") == 200
        assert type(resp.get("body").get("story_run_events")) == list

    def test_list(self):
        resp = self.runs_api.list(
            story_id=self.story_id
        )

        assert resp.get("status_code") == 200
        assert type(resp.get("body").get("story_runs")) == list

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

    def test_create(self):
        resp = self.versions_api.create(
            story_id = self.story_id,
            name     = "Create Version Unit Test"
        )

        self.version_id = resp.get("body").get("story_version").get("id")

        assert resp.get("status_code")                           == 200
        assert resp.get("body").get("story_version").get("name") == "Create Version Unit Test"

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

        assert resp.get("status_code")                                        == 200
        assert resp.get("body").get("story_version").get("name")              == "Get Version Unit Test"
        assert resp.get("body").get("story_version").get("export_file")       is not None
        assert type(resp.get("body").get("story_version").get("export_file")) == dict

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

        assert resp.get("status_code")                           == 200
        assert resp.get("body").get("story_version").get("name") == "New Version Unit Test Name"

    def test_list(self):
        create_version = self.versions_api.create(
            story_id = self.story_id,
            name     = "List Version Unit Test"
        )

        self.version_id = create_version.get("body").get("story_version").get("id")

        resp = self.versions_api.list(
            story_id=self.story_id
        )

        assert resp.get("status_code")                      == 200
        assert type(resp.get("body").get("story_versions")) == list
        assert len(resp.get("body").get("story_versions"))  >= 1

    def test_delete(self):
        create_version = self.versions_api.create(
            story_id = self.story_id,
            name     = "Deleete Version Unit Test"
        )

        version_id = create_version.get("body").get("story_version").get("id")

        resp = self.versions_api.delete(
            story_id   = self.story_id,
            version_id = version_id
        )

        assert resp.get("status_code") == 200
