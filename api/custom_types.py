from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel


class RelatedEpisode(BaseModel):
    id: int
    name: str
    air_date: date
    episode: str
    plot: str
    image: str


class Character(BaseModel):
    id: int
    name: str
    status: str
    species: str
    type: str
    gender: str
    episodes: List[RelatedEpisode]
    comments: List[dict]


class RelatedCharacter(BaseModel):
    id: int
    name: str
    status: str
    species: str
    type: str
    gender: str


class Episode(BaseModel):
    id: int
    name: str
    air_date: date
    episode: str
    plot: str
    image: str
    characters: List[RelatedCharacter]
    comments: List[dict]


class Comment(BaseModel):
    id: int = None
    character_id: Optional[int] = None
    episode_id: Optional[int] = None
    author: str
    posted_on: datetime = None
    comment: str
