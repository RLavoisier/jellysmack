from datetime import date

from ..helpers import serialize_episode, serialize_character
from ..models import Comments


def test_get_episode_by_id(setup, db_manager, expected_episode1_dict):
    episode1 = db_manager.get_episode_by_id(1)
    assert serialize_episode(episode1) == expected_episode1_dict


def test_get_episodes(setup, db_manager, expected_full_episode_list):
    episodes = db_manager.get_episodes()
    assert [
        serialize_episode(episode) for episode in episodes
    ] == expected_full_episode_list


def test_filter_episodes(setup, db_manager):
    # Episode by id
    episodes = db_manager.filter_episodes(id=3)
    assert len(episodes) == 1

    # Episode by name
    episodes = db_manager.filter_episodes(episode="S01E01")
    assert len(episodes) == 1

    # Unexisting episode
    episodes = db_manager.filter_episodes(episode="Wubalubadubdub")
    assert not episodes

    # Episode from date
    episodes = db_manager.filter_episodes(date_from=date(2013, 12, 9))
    assert len(episodes) == 2

    # Episode to date
    episodes = db_manager.filter_episodes(date_to=date(2013, 12, 8))
    assert len(episodes) == 1

    # Episode between
    episodes = db_manager.filter_episodes(
        date_from=date(2013, 12, 3), date_to=date(2013, 12, 10)
    )
    assert len(episodes) == 1


def test_get_characters(setup, db_manager, expected_full_character_list):
    characters = [
        serialize_character(character) for character in db_manager.get_characters()
    ]
    assert characters == expected_full_character_list


def test_get_character_by_id(setup, db_manager, expected_rick):
    character = serialize_character(db_manager.get_character_by_id(1))
    assert character == expected_rick


def test_filter_character(setup, db_manager):
    characters = db_manager.filter_characters(gender="Female")
    assert len(characters) == 2

    characters = db_manager.filter_characters(species="Human")
    assert len(characters) == 5


def test_create_comment(setup, db_manager):
    comment = {"character_id": 1, "author": "Rick", "comment": "test comment"}
    created_comment = db_manager.create_comment(comment)
    assert type(created_comment) == Comments
    assert created_comment.id == 1

    comment = {
        "character_id": 1,
        "author": "Rick",
        "comment": "test comment",
        "episode_id": 1,
    }
    created_comment = db_manager.create_comment(comment)
    assert type(created_comment) == Comments
    assert created_comment.id == 2


def test_filter_comments(setup, db_manager, test_comments):
    session = db_manager.get_session()
    session.query(Comments).delete()
    for comment in test_comments:
        db_manager.create_comment(comment)

    comments_for_episode_1 = db_manager.filter_comments(episode_id=1)
    assert len(comments_for_episode_1) == 2

    comments_for_character_1 = db_manager.filter_comments(character_id=1)
    assert len(comments_for_character_1) == 1

    comments_for_character_2 = db_manager.filter_comments(character_id=2)
    assert len(comments_for_character_2) == 1

    comments_for_character_3 = db_manager.filter_comments(character_id=3)
    assert len(comments_for_character_3) == 0
