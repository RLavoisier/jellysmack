import json
import os
import re
from datetime import datetime

import requests
import sqlalchemy
from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    UniqueConstraint,
    DateTime,
    Text,
    func,
)

#####################################################
# Initialization script for Jellysmack technical test
#####################################################
db_dir = os.path.join(os.path.dirname(__file__), "jellysmack.sqlite")
DB_PATH = os.path.abspath(db_dir)
# BBD Init
print("Creating database....")
db = sqlalchemy.create_engine(f"sqlite:///{DB_PATH}")
imdb_api_path = (
    "https://imdb-api.com/en/API/SeasonEpisodes/k_g9tdafoz/tt2861424/{season}"
)

try:
    meta = MetaData()

    episodes = Table(
        "episodes",
        meta,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("name", String(200)),
        Column("air_date", Date()),
        Column("episode", String(10)),
        Column("plot", String(500)),
        Column("image", String(500)),
    )

    characters = Table(
        "characters",
        meta,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("name", String(200)),
        Column("status", String(50)),
        Column("species", String(50)),
        Column("type", String(100)),
        Column("gender", String(50)),
    )

    characters_appearance = Table(
        "characters_appearance",
        meta,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("character_id", Integer, ForeignKey("characters.id")),
        Column("episode_id", Integer, ForeignKey("episodes.id")),
        Column("gender", String(50)),
        UniqueConstraint("character_id", "episode_id", name="chara_episode"),
    )

    comments = Table(
        "comments",
        meta,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("character_id", Integer, ForeignKey("characters.id")),
        Column("episode_id", Integer, ForeignKey("episodes.id")),
        Column("author", String(100)),
        Column("posted_on", DateTime(timezone=True), server_default=func.now()),
        Column("comment", Text()),
    )

    meta.drop_all(db)
    meta.create_all(db)
    print("Database created")
except Exception as e:
    print(f"Unable to create database: {e}")
    print(f"aborting")
    exit()

# Importing data
print("Importing data")
print("Importing characters")
with open("rick_morty-characters_v1.json", "r") as f:
    characters_json = json.loads(f.read())

conn = db.connect()
characters_to_insert = []
appeance_to_insert = []
for character in characters_json:
    appearance = character.pop("episode", [])
    characters_to_insert.append(character)
    for episode in appearance:
        appeance_to_insert.append(
            {"episode_id": episode, "character_id": character["id"]}
        )

conn.execute(characters.insert(), characters_to_insert)
conn.execute(characters_appearance.insert(), appeance_to_insert)

print("Importing episodes")
with open("rick_morty-episodes_v1.json", "r") as f:
    episodes_json = json.loads(f.read())

episodes_to_insert = []
for episode in episodes_json:
    episode.pop("characters", [None])
    episode["air_date"] = datetime.strptime(episode["air_date"], "%B %d, %Y").date()
    print(f"Fetching imdb datas for episode {episode['episode']}")
    season_nb, episode_nb = (int(v) for v in re.findall(r"\d+", episode["episode"]))

    imdb_response = requests.get(imdb_api_path.format(season=season_nb))
    try:
        imdb_response.raise_for_status()
        imdb_response = imdb_response.json()
        episode_imdb = next(
            iter(
                episode
                for episode in imdb_response["episodes"]
                if episode["episodeNumber"] == str(episode_nb)
            )
        )
        episode["plot"] = episode_imdb["plot"]
        episode["image"] = episode_imdb["image"]
    except:
        print(f"Unable to get imdb infos for episode {episode['episode']}")

    episodes_to_insert.append(episode)

conn.execute(episodes.insert(), episodes_to_insert)

print("Wubalubadubdub ! Everything's ready")
