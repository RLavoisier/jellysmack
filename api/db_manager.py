from datetime import date
from typing import List, Dict

import sqlalchemy
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from . import settings
from .models import Episodes, Characters, Comments


class DBManager:
    def __init__(self, engine: Engine = None):
        """This class encapsulate every method to fetch data from the BDD

        param engine: An existing SQLAlchemy Engine object
        """
        self.db = engine or sqlalchemy.create_engine(f"sqlite:///{settings.DB_PATH}")

    def __call__(self, *args, **kwargs):
        try:
            return self.__instance
        except AttributeError:
            self.__instance = DBManager(*args, **kwargs)
            return self.__instance

    def get_session(self):
        """Returns a BDD session"""
        Session = sessionmaker(bind=self.db)
        return Session()

    def get_episodes(self) -> List[Episodes]:
        """This method returns all the episodes from bdd"""
        session = self.get_session()
        return session.query(Episodes).all()

    def get_episode_by_id(self, episode_id: int) -> Episodes:
        """This method return a single episode by id"""
        session = self.get_session()
        return session.query(Episodes).filter(Episodes.id == episode_id).first()

    def filter_episodes(
        self, date_from: date = None, date_to: date = None, **kwargs
    ) -> List[Episodes]:
        """This method returns a list of episodes based on different filters"""
        session = self.get_session()
        k_wargs = {k: v for k, v in kwargs.items() if v}
        episodes = session.query(Episodes).filter_by(**k_wargs)
        if date_from:
            episodes = episodes.filter(Episodes.air_date >= date_from)
        if date_to:
            episodes = episodes.filter(Episodes.air_date <= date_to)

        return episodes.all()

    def get_characters(self) -> List[Characters]:
        """This method returns all the characters from bdd"""
        session = self.get_session()
        return session.query(Characters).all()

    def filter_characters(self, **kwargs) -> List[Characters]:
        """This method returns a list of character based on different filters"""
        session = self.get_session()
        k_wargs = {k: v for k, v in kwargs.items() if v}
        return session.query(Characters).filter_by(**k_wargs).all()

    def get_character_by_id(self, character_id: int) -> Characters:
        """This method returns a character from its id"""
        session = self.get_session()
        return session.query(Characters).filter(Characters.id == character_id).first()

    def get_comments(self) -> List[Comments]:
        """This method returns the list of all comments"""
        session = self.get_session()
        return session.query(Comments).all()

    def filter_comments(self, **kwargs):
        k_wargs = {k: v for k, v in kwargs.items() if v}
        session = self.get_session()
        return session.query(Comments).filter_by(**k_wargs).all()

    def create_comment(self, comment: dict):
        """This method insert a comment in the database"""
        comment.pop("id", None)
        comment.pop("posted_on", None)

        session = self.get_session()
        comment_to_add = Comments(**comment)
        session.add(comment_to_add)
        session.commit()
        session.refresh(comment_to_add)
        return comment_to_add
