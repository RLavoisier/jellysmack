import csv
from io import StringIO

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi_pagination import paginate, add_pagination, Page
from fastapi.middleware.cors import CORSMiddleware

from .custom_types import Episode, Character, Comment
from .db_manager import DBManager
from .helpers import serialize_episode, serialize_character, serialize_comment

app = FastAPI(
    title="Rick and Morty episodes API",
    description="""
    Amazon API that allows you to consult and interact with Rick And Morty episodes
    and transform yourselves as a pickle
    """,
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_manager = DBManager()

NOT_FOUND = "Not found"


@app.get("/episodes", response_model=Page[Episode])
async def list_episodes():
    episodes = db_manager.get_episodes()
    return paginate([serialize_episode(episode) for episode in episodes])


@app.get("/characters", response_model=Page[Character])
async def list_characters():
    characters = db_manager.get_characters()
    return paginate([serialize_character(character) for character in characters])


@app.get("/episodes/{episode_id}", response_model=Episode)
async def get_episode_by_id(episode_id: int):
    episode = db_manager.get_episode_by_id(episode_id)
    if not episode:
        return JSONResponse(status_code=404, content={"message": NOT_FOUND})
    return serialize_episode(episode)


@app.get("/characters/{character_id}", response_model=Character)
async def get_character_by_id(character_id: int):
    character = db_manager.get_character_by_id(character_id)
    if not character:
        return JSONResponse(status_code=404, content={"message": NOT_FOUND})
    return serialize_character(character)


@app.get("/comments", response_model=Page[Comment])
async def get_comments(episode_id: int = None, character_id: int = None):
    comments = db_manager.filter_comments(
        episode_id=episode_id, character_id=character_id
    )
    return paginate(
        jsonable_encoder([serialize_comment(comment) for comment in comments])
    )


@app.post("/comments")
def create_comment(comment: Comment):
    try:
        if not comment.character_id and not comment.episode_id:
            raise ValueError("Nedd at least one of (character_id, episode_id)")
        added_comment = db_manager.create_comment(comment.__dict__)
        return JSONResponse(
            status_code=201, content=jsonable_encoder(serialize_comment(added_comment))
        )
    except ValueError as e:
        return JSONResponse(status_code=400, content={"message": f"Bad Request ({e})"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Error ({e})"})


@app.get("/comments/csv", response_class=PlainTextResponse)
def export_comments():
    """This method exports all the comment as a CSV File"""
    comments = db_manager.get_comments()
    if not comments:
        return JSONResponse(
            status_code=404, content={"message": f"No comments to export"}
        )
    comments_to_write = []
    for comment in comments:
        comment = serialize_comment(comment)
        comment.pop("character", None)
        comment.pop("episode", None)
        comments_to_write.append(comment)
    io_file = StringIO()
    fieldnames = comments_to_write[0].keys()
    writer = csv.DictWriter(io_file, fieldnames=fieldnames)
    writer.writeheader()
    for comment in comments_to_write:
        writer.writerow(comment)
    io_file.seek(0)
    return PlainTextResponse(io_file.read())


@app.get("/stats", response_class=PlainTextResponse)
def get_stats():
    """This method returns different stats on comments as a csv file"""
    stats = []
    episodes = db_manager.get_episodes()
    for episode in episodes:
        comments = episode.comments
        nb_comments = len(comments)
        if nb_comments:
            average_comment_length = round(
                sum([len(comment.comment) for comment in comments]) / nb_comments
            )
        else:
            average_comment_length = 0
        stats.append(
            {
                "episode_id": episode.id,
                "episode_title": episode.name,
                "episode_identifier": episode.episode,
                "nb_comments": nb_comments,
                "comments_average_length": average_comment_length,
            }
        )

    io_file = StringIO()
    fieldnames = stats[0].keys()
    writer = csv.DictWriter(io_file, fieldnames=fieldnames)
    writer.writeheader()
    for comment in stats:
        writer.writerow(comment)
    io_file.seek(0)
    return PlainTextResponse(io_file.read())


add_pagination(app)
