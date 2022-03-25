import os
from datetime import datetime, date

from _pytest.fixtures import fixture
from sqlalchemy import create_engine

from .. import models
from ..db_manager import DBManager
from ..models import Characters, CharactersAppearance, Episodes, Comments


@fixture(scope="session")
def engine():
    return create_engine("sqlite://")


@fixture
def db_manager(engine):
    return DBManager(engine=engine)


@fixture(scope="session")
def connection(engine):
    return engine.connect()


@fixture(scope="session")
def setup(connection):
    models.Base.metadata.bind = connection
    models.Base.metadata.create_all()
    feed_bdd(connection)
    yield
    models.Base.metadata.drop_all()


def feed_bdd(connection):
    episodes = [
        {
            "id": 1,
            "name": "Pilot",
            "air_date": "December 2, 2013",
            "episode": "S01E01",
            "plot": "plot S01E01",
            "image": "image S01E01",
            "characters": [
                1,
                2,
            ],
        },
        {
            "id": 2,
            "name": "Lawnmower Dog",
            "air_date": "December 9, 2013",
            "episode": "S01E02",
            "plot": "plot S01E02",
            "image": "image S01E02",
            "characters": [
                1,
                2,
            ],
        },
        {
            "id": 3,
            "name": "Anatomy Park",
            "air_date": "December 16, 2013",
            "episode": "S01E03",
            "plot": "plot S01E03",
            "image": "image S01E03",
            "characters": [
                1,
                2,
                3,
                4,
                5,
            ],
        },
    ]
    characters = [
        {
            "id": 1,
            "name": "Rick Sanchez",
            "status": "Alive",
            "species": "Human",
            "type": "",
            "gender": "Male",
            "episode": [
                1,
                2,
                3,
            ],
        },
        {
            "id": 2,
            "name": "Morty Smith",
            "status": "Alive",
            "species": "Human",
            "type": "",
            "gender": "Male",
            "episode": [
                1,
                2,
                3,
            ],
        },
        {
            "id": 3,
            "name": "Summer Smith",
            "status": "Alive",
            "species": "Human",
            "type": "",
            "gender": "Female",
            "episode": [
                2,
            ],
        },
        {
            "id": 4,
            "name": "Beth Smith",
            "status": "Alive",
            "species": "Human",
            "type": "",
            "gender": "Female",
            "episode": [
                2,
            ],
        },
        {
            "id": 5,
            "name": "Jerry Smith",
            "status": "Alive",
            "species": "Human",
            "type": "",
            "gender": "Male",
            "episode": [
                3,
            ],
        },
    ]

    episodes_to_insert = []
    for episode in episodes:
        episode.pop("characters", [None])
        episode["air_date"] = datetime.strptime(episode["air_date"], "%B %d, %Y")
        episodes_to_insert.append(episode)

    connection.execute(Episodes.__table__.insert(), episodes_to_insert)

    characters_to_insert = []
    appeance_to_insert = []
    for character in characters:
        appearance = character.pop("episode", [])
        characters_to_insert.append(character)
        for episode in appearance:
            appeance_to_insert.append(
                {"episode_id": episode, "character_id": character["id"]}
            )

    connection.execute(Characters.__table__.insert(), characters_to_insert)
    connection.execute(CharactersAppearance.__table__.insert(), appeance_to_insert)


@fixture
def expected_episode1_without_relation_dict():
    return {
        "id": 1,
        "name": "Pilot",
        "air_date": date(2013, 12, 2),
        "episode": "S01E01",
        "plot": "plot S01E01",
        "image": "image S01E01",
    }


@fixture
def expected_episode1_dict():
    return {
        "id": 1,
        "name": "Pilot",
        "air_date": date(2013, 12, 2),
        "episode": "S01E01",
        "plot": "plot S01E01",
        "image": "image S01E01",
        "characters": [
            {
                "id": 1,
                "name": "Rick Sanchez",
                "status": "Alive",
                "species": "Human",
                "type": "",
                "gender": "Male",
            },
            {
                "id": 2,
                "name": "Morty Smith",
                "status": "Alive",
                "species": "Human",
                "type": "",
                "gender": "Male",
            },
        ],
        "comments": [],
    }


@fixture
def expected_rick():
    return {
        "id": 1,
        "name": "Rick Sanchez",
        "status": "Alive",
        "species": "Human",
        "type": "",
        "gender": "Male",
        "episodes": [
            {
                "id": 1,
                "name": "Pilot",
                "air_date": date(2013, 12, 2),
                "episode": "S01E01",
                "plot": "plot S01E01",
                "image": "image S01E01",
            },
            {
                "id": 2,
                "name": "Lawnmower Dog",
                "air_date": date(2013, 12, 9),
                "episode": "S01E02",
                "plot": "plot S01E02",
                "image": "image S01E02",
            },
            {
                "id": 3,
                "name": "Anatomy Park",
                "air_date": date(2013, 12, 16),
                "episode": "S01E03",
                "plot": "plot S01E03",
                "image": "image S01E03",
            },
        ],
        "comments": [],
    }


@fixture
def expected_full_episode_list():
    return [
        {
            "id": 1,
            "name": "Pilot",
            "air_date": date(2013, 12, 2),
            "episode": "S01E01",
            "plot": "plot S01E01",
            "image": "image S01E01",
            "characters": [
                {
                    "id": 1,
                    "name": "Rick Sanchez",
                    "status": "Alive",
                    "species": "Human",
                    "type": "",
                    "gender": "Male",
                },
                {
                    "id": 2,
                    "name": "Morty Smith",
                    "status": "Alive",
                    "species": "Human",
                    "type": "",
                    "gender": "Male",
                },
            ],
            "comments": [],
        },
        {
            "id": 2,
            "name": "Lawnmower Dog",
            "air_date": date(2013, 12, 9),
            "episode": "S01E02",
            "plot": "plot S01E02",
            "image": "image S01E02",
            "characters": [
                {
                    "id": 1,
                    "name": "Rick Sanchez",
                    "status": "Alive",
                    "species": "Human",
                    "type": "",
                    "gender": "Male",
                },
                {
                    "id": 2,
                    "name": "Morty Smith",
                    "status": "Alive",
                    "species": "Human",
                    "type": "",
                    "gender": "Male",
                },
                {
                    "id": 3,
                    "name": "Summer Smith",
                    "status": "Alive",
                    "species": "Human",
                    "type": "",
                    "gender": "Female",
                },
                {
                    "id": 4,
                    "name": "Beth Smith",
                    "status": "Alive",
                    "species": "Human",
                    "type": "",
                    "gender": "Female",
                },
            ],
            "comments": [],
        },
        {
            "id": 3,
            "name": "Anatomy Park",
            "air_date": date(2013, 12, 16),
            "episode": "S01E03",
            "plot": "plot S01E03",
            "image": "image S01E03",
            "characters": [
                {
                    "id": 1,
                    "name": "Rick Sanchez",
                    "status": "Alive",
                    "species": "Human",
                    "type": "",
                    "gender": "Male",
                },
                {
                    "id": 2,
                    "name": "Morty Smith",
                    "status": "Alive",
                    "species": "Human",
                    "type": "",
                    "gender": "Male",
                },
                {
                    "id": 5,
                    "name": "Jerry Smith",
                    "status": "Alive",
                    "species": "Human",
                    "type": "",
                    "gender": "Male",
                },
            ],
            "comments": [],
        },
    ]


@fixture
def expected_full_character_list():
    return [
        {
            "id": 1,
            "name": "Rick Sanchez",
            "status": "Alive",
            "species": "Human",
            "type": "",
            "gender": "Male",
            "episodes": [
                {
                    "id": 1,
                    "name": "Pilot",
                    "air_date": date(2013, 12, 2),
                    "episode": "S01E01",
                    "plot": "plot S01E01",
                    "image": "image S01E01",
                },
                {
                    "id": 2,
                    "name": "Lawnmower Dog",
                    "air_date": date(2013, 12, 9),
                    "episode": "S01E02",
                    "plot": "plot S01E02",
                    "image": "image S01E02",
                },
                {
                    "id": 3,
                    "name": "Anatomy Park",
                    "air_date": date(2013, 12, 16),
                    "episode": "S01E03",
                    "plot": "plot S01E03",
                    "image": "image S01E03",
                },
            ],
            "comments": [],
        },
        {
            "id": 2,
            "name": "Morty Smith",
            "status": "Alive",
            "species": "Human",
            "type": "",
            "gender": "Male",
            "episodes": [
                {
                    "id": 1,
                    "name": "Pilot",
                    "air_date": date(2013, 12, 2),
                    "episode": "S01E01",
                    "plot": "plot S01E01",
                    "image": "image S01E01",
                },
                {
                    "id": 2,
                    "name": "Lawnmower Dog",
                    "air_date": date(2013, 12, 9),
                    "episode": "S01E02",
                    "plot": "plot S01E02",
                    "image": "image S01E02",
                },
                {
                    "id": 3,
                    "name": "Anatomy Park",
                    "air_date": date(2013, 12, 16),
                    "episode": "S01E03",
                    "plot": "plot S01E03",
                    "image": "image S01E03",
                },
            ],
            "comments": [],
        },
        {
            "id": 3,
            "name": "Summer Smith",
            "status": "Alive",
            "species": "Human",
            "type": "",
            "gender": "Female",
            "episodes": [
                {
                    "id": 2,
                    "name": "Lawnmower Dog",
                    "air_date": date(2013, 12, 9),
                    "episode": "S01E02",
                    "plot": "plot S01E02",
                    "image": "image S01E02",
                }
            ],
            "comments": [],
        },
        {
            "id": 4,
            "name": "Beth Smith",
            "status": "Alive",
            "species": "Human",
            "type": "",
            "gender": "Female",
            "episodes": [
                {
                    "id": 2,
                    "name": "Lawnmower Dog",
                    "air_date": date(2013, 12, 9),
                    "episode": "S01E02",
                    "plot": "plot S01E02",
                    "image": "image S01E02",
                }
            ],
            "comments": [],
        },
        {
            "id": 5,
            "name": "Jerry Smith",
            "status": "Alive",
            "species": "Human",
            "type": "",
            "gender": "Male",
            "episodes": [
                {
                    "id": 3,
                    "name": "Anatomy Park",
                    "air_date": date(2013, 12, 16),
                    "episode": "S01E03",
                    "plot": "plot S01E03",
                    "image": "image S01E03",
                }
            ],
            "comments": [],
        },
    ]


@fixture
def expected_episode1_from_api():
    return {
        "id": 1,
        "name": "Pilot",
        "air_date": "2013-12-02",
        "episode": "S01E01",
        "plot": "plot S01E01",
        "image": "image S01E01",
        "characters": [],
        "comments": [],
    }


@fixture
def expected_full_episode_list_from_api():
    return {
        "items": [
            {
                "id": 1,
                "name": "Pilot",
                "air_date": "2013-12-02",
                "episode": "S01E01",
                "plot": "plot S01E01",
                "image": "image S01E01",
                "characters": [],
                "comments": [],
            },
            {
                "id": 2,
                "name": "Lawnmower Dog",
                "air_date": "2013-12-09",
                "episode": "S01E02",
                "plot": "plot S01E02",
                "image": "image S01E02",
                "characters": [],
                "comments": [],
            },
            {
                "id": 3,
                "name": "Anatomy Park",
                "air_date": "2013-12-16",
                "episode": "S01E03",
                "plot": "plot S01E03",
                "image": "image S01E03",
                "characters": [],
                "comments": [],
            },
        ],
        "page": 1,
        "size": 50,
        "total": 3,
    }


@fixture
def expected_full_character_list_from_api():
    return {
        "items": [
            {
                "id": 1,
                "name": "Rick Sanchez",
                "status": "Alive",
                "species": "Human",
                "type": "",
                "gender": "Male",
                "episodes": [],
                "comments": [],
            },
            {
                "id": 2,
                "name": "Morty Smith",
                "status": "Alive",
                "species": "Human",
                "type": "",
                "gender": "Male",
                "episodes": [],
                "comments": [],
            },
            {
                "id": 3,
                "name": "Summer Smith",
                "status": "Alive",
                "species": "Human",
                "type": "",
                "gender": "Female",
                "episodes": [],
                "comments": [],
            },
            {
                "id": 4,
                "name": "Beth Smith",
                "status": "Alive",
                "species": "Human",
                "type": "",
                "gender": "Female",
                "episodes": [],
                "comments": [],
            },
            {
                "id": 5,
                "name": "Jerry Smith",
                "status": "Alive",
                "species": "Human",
                "type": "",
                "gender": "Male",
                "episodes": [],
                "comments": [],
            },
        ],
        "page": 1,
        "size": 50,
        "total": 5,
    }


@fixture
def expected_rick_from_api():
    return {
        "id": 1,
        "name": "Rick Sanchez",
        "status": "Alive",
        "species": "Human",
        "type": "",
        "gender": "Male",
        "episodes": [],
        "comments": [],
    }


@fixture
def test_comments():
    return [
        {
            "character_id": 1,
            "episode_id": 1,
            "author": "Rick",
            "comment": "Your opinion means little to me",
        },
        {
            "character_id": 2,
            "author": "The Cromulons",
            "comment": "SHOW ME WHAT YOU GOT",
        },
        {"episode_id": 1, "author": "Morty", "comment": "I love jessica"},
    ]


@fixture
def mock_episodes_from_db():
    episodes = [
        {
            "id": 1,
            "name": "Pilot",
            "air_date": "2013-12-02",
            "episode": "S01E01",
            "plot": "plot S01E01",
            "image": "image S01E01",
        },
        {
            "id": 2,
            "name": "Lawnmower Dog",
            "air_date": "2013-12-09",
            "episode": "S01E02",
            "plot": "plot S01E02",
            "image": "image S01E02",
        },
        {
            "id": 3,
            "name": "Anatomy Park",
            "air_date": "2013-12-16",
            "episode": "S01E03",
            "plot": "plot S01E03",
            "image": "image S01E03",
        },
    ]
    return [Episodes(**episode) for episode in episodes]


@fixture
def mock_episode1_from_db():
    episode = {
        "id": 1,
        "name": "Pilot",
        "air_date": "2013-12-02",
        "episode": "S01E01",
        "plot": "plot S01E01",
        "image": "image S01E01",
    }
    return Episodes(**episode)


@fixture
def mock_characters_from_db():
    characters = [
        {
            "id": 1,
            "name": "Rick Sanchez",
            "status": "Alive",
            "species": "Human",
            "type": "",
            "gender": "Male",
            "episodes": [],
            "comments": [],
        },
        {
            "id": 2,
            "name": "Morty Smith",
            "status": "Alive",
            "species": "Human",
            "type": "",
            "gender": "Male",
            "episodes": [],
            "comments": [],
        },
        {
            "id": 3,
            "name": "Summer Smith",
            "status": "Alive",
            "species": "Human",
            "type": "",
            "gender": "Female",
            "episodes": [],
            "comments": [],
        },
        {
            "id": 4,
            "name": "Beth Smith",
            "status": "Alive",
            "species": "Human",
            "type": "",
            "gender": "Female",
            "episodes": [],
            "comments": [],
        },
        {
            "id": 5,
            "name": "Jerry Smith",
            "status": "Alive",
            "species": "Human",
            "type": "",
            "gender": "Male",
            "episodes": [],
            "comments": [],
        },
    ]
    return [Characters(**character) for character in characters]


@fixture
def mock_rick_from_db():
    character = {
        "id": 1,
        "name": "Rick Sanchez",
        "status": "Alive",
        "species": "Human",
        "type": "",
        "gender": "Male",
    }
    return Characters(**character)


@fixture
def mock_comments_from_db():
    comments = [
        {
            "id": 1,
            "character_id": 1,
            "episode_id": 1,
            "author": "Rick",
            "comment": "Your opinion means little to me",
            "posted_on": datetime(2020, 1, 1),
        },
        {
            "id": 2,
            "character_id": 2,
            "episode_id": None,
            "author": "The Cromulons",
            "comment": "SHOW ME WHAT YOU GOT",
            "posted_on": datetime(2020, 1, 1),
        },
        {
            "id": 2,
            "character_id": None,
            "episode_id": 1,
            "author": "Morty",
            "comment": "I love jessica",
            "posted_on": datetime(2020, 1, 1),
        },
    ]
    return [Comments(**comment) for comment in comments]


@fixture
def expected_comment_csv_from_api():
    return "id,character_id,episode_id,author,posted_on,comment\r\n1,1,1,Rick,2020-01-01 00:00:00,Your opinion means little to me\r\n2,2,,The Cromulons,2020-01-01 00:00:00,SHOW ME WHAT YOU GOT\r\n2,,1,Morty,2020-01-01 00:00:00,I love jessica\r\n"
