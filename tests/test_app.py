"""
Tests for API-specific routes
"""

from app import app
from app.models.timelinepost import TimelinePost, mydb
from peewee import SqliteDatabase
import unittest
import os

# Close the global database if it's open
if not mydb.is_closed():
    mydb.close()

TEST_DB = SqliteDatabase(":memory:")
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

    def test_timeline(self):
        # Test the timeline page rendering
        endpoint = "/api/timeline_post"
        response = self.client.get(endpoint)
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        # Test posting a new timeline post

        post_data = self.client.post(
            "api/timeline_post",
            data={
                "name": "Smith",
                "email": "smith@gmail.com",
                "content": "This is a test post 2.",
            },
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
