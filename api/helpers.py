from typing import Dict

from sqlalchemy.orm import class_mapper, DeclarativeMeta

from .custom_types import Character, Episode
from .models import Comments, Characters, Episodes


def serialize_episode(episode: Episodes) -> Episode:
    """This method serialize an BDD episode object"""
    if not episode:
        return {}
    characters = episode.characters
    comments = episode.comments
    episode = serialize_bdd_object(episode)
    episode["characters"] = [
        serialize_bdd_object(character.character) for character in characters
    ]
    episode["comments"] = [serialize_comment(comment) for comment in comments]
    return episode


def serialize_character(character: Characters) -> Character:
    """This method serialize an BDD episode object"""
    if not character:
        return {}
    episodes = character.episodes
    comments = character.comments
    character = serialize_bdd_object(character)
    character["episodes"] = [
        serialize_bdd_object(episode.episode) for episode in episodes
    ]
    character["comments"] = [serialize_comment(comment) for comment in comments]
    return character


def serialize_comment(comment: Comments):
    """This method serialize a comment"""
    comment_dict = {
        "id": comment.id,
        "character_id": comment.character_id,
        "episode_id": comment.episode_id,
        "author": comment.author,
        "posted_on": comment.posted_on,
        "comment": comment.comment,
    }
    if comment.episode:
        comment_dict["episode"] = comment.episode.episode
    if comment.character:
        comment_dict["character"] = comment.character.name
    return comment_dict


def serialize_bdd_object(o: DeclarativeMeta) -> Dict:
    """This methd return a SQLAlchemy bdd object as json"""
    columns = [c.key for c in class_mapper(o.__class__).columns]
    # then we return their values in a dict
    return dict((c, getattr(o, c)) for c in columns)
