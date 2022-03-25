from fastapi.testclient import TestClient

from ..api import app
from ..db_manager import DBManager

client = TestClient(app)


def test_list_episodes(
    monkeypatch, expected_full_episode_list_from_api, mock_episodes_from_db
):
    def mock_bdd_episodes(*args):
        return mock_episodes_from_db

    monkeypatch.setattr(DBManager, "get_episodes", mock_bdd_episodes)
    res = client.get("/episodes")
    assert res.json() == expected_full_episode_list_from_api


def test_list_characters(
    monkeypatch, expected_full_character_list_from_api, mock_characters_from_db
):
    def mock_get_characters(*args):
        return mock_characters_from_db

    monkeypatch.setattr(DBManager, "get_characters", mock_get_characters)
    res = client.get("/characters")
    assert res.json() == expected_full_character_list_from_api


def test_episode_id(monkeypatch, mock_episode1_from_db, expected_episode1_from_api):
    def mock_get_episode_by_id(*args):
        return mock_episode1_from_db

    monkeypatch.setattr(DBManager, "get_episode_by_id", mock_get_episode_by_id)
    res = client.get("/episodes/1")
    assert res.json() == expected_episode1_from_api


def test_character_id(monkeypatch, mock_rick_from_db, expected_rick_from_api):
    def mock_get_character_by_id(*args):
        return mock_rick_from_db

    monkeypatch.setattr(DBManager, "get_character_by_id", mock_get_character_by_id)
    res = client.get("/characters/1")
    assert res.json() == expected_rick_from_api


def test_export_comment_to_csv(
    monkeypatch, mock_comments_from_db, expected_comment_csv_from_api
):
    def mock_get_comments(*args):
        return mock_comments_from_db

    monkeypatch.setattr(DBManager, "get_comments", mock_get_comments)
    res = client.get("/comments/csv")
    assert res.text == expected_comment_csv_from_api
