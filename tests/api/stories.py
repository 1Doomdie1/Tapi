import unittest
from os          import getenv
from api.teams   import TeamsAPI
from api.stories import StoriesAPI
from dotenv      import load_dotenv


class test_StoriesAPI(unittest.TestCase):

    def setUp(self):
        load_dotenv()
        self.stories_api = StoriesAPI(getenv("DOMAIN"), getenv("API_KEY"))
        self.team_id = TeamsAPI(getenv("DOMAIN"), getenv("API_KEY")).list().get("body").get("teams")[0].get("id")
        self.story_id = None

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
        resp1 = self.stories_api.update(story_id = self.story_id, name = "Updated Unit Test Name")
        resp2 = self.stories_api.update(story_id = self.story_id, description = "Updated Unit Test description")
        resp3 = self.stories_api.update(story_id = self.story_id, disabled = True)

        assert resp1.get("status_code") == 200
        assert resp2.get("status_code") == 200
        assert resp3.get("status_code") == 200

        assert resp1.get("body").get("name")        == "Updated Unit Test Name"
        assert resp2.get("body").get("description") == "Updated Unit Test description"
        assert resp3.get("body").get("disabled")    == True
