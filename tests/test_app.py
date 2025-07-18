# tests/test_app.py

from app import app
from app.models.timelinepost import TimelinePost
from peewee import SqliteDatabase
import unittest
import os

os.environ['TESTING'] = 'true'
TEST_DB = SqliteDatabase(':memory:')
MODELS = [TimelinePost]


class AppTestCase(unittest.TestCase):
    def setUp(self):
        TEST_DB.bind(MODELS, bind_refs=False, bind_backrefs=False)
        TEST_DB.connect()
        TEST_DB.create_tables(MODELS)
        self.client = app.test_client()

    def tearDown(self):
        TEST_DB.drop_tables([TimelinePost])
        TEST_DB.close()

    def test_home(self):
        response = self.client.get('/')
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        # Check title
        assert "<title>Alejandro Villate</title>" in html
        # Check main heading
        assert "<h1>Alejandro Villate</h1>" in html
        # Check for profile section
        assert '<div class="profile">' in html
        # Check for bio text
        assert " I\'m a Computer Science major at the University of Florida" in html
        # Check for profile
        assert '<div class="profile">' in html
        # Check for map
        assert '<div id="map"></div>' in html

    def test_timeline(self):
        # Test the timeline page rendering
        endpoint = "api/timeline_post"
        response = self.client.get(endpoint)
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) >= 0

        # Test posting a new timeline post

        post_data = self.client.post(
            "api/timeline_post",
            data={"name": "Smith", "email": "smith@gmail.com",
                  "content": "This is a test post 2."}
        )
        assert post_data.status_code == 200
        json = post_data.get_json()
        assert json["name"] == "Smith"
        assert json["email"] == "smith@gmail.com"
        assert json["content"] == "This is a test post 2."

        # Test the timeline page rendering

        get_data = self.client.get(endpoint)
        assert get_data.status_code == 200
        json = get_data.get_json()
        assert len(json["timeline_posts"]) == 1
