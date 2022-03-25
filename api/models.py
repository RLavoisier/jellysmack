from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    MetaData,
    Date,
    func,
    DateTime,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy
from sqlalchemy.orm import relationship

from . import settings

Base = declarative_base()
db = sqlalchemy.create_engine(f"sqlite:///{settings.DB_PATH}")

metadata = MetaData()


class Episodes(Base):

    __tablename__ = "episodes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200))
    air_date = Column(Date())
    episode = Column(String(10))
    plot = Column(String(500))
    image = Column(String(500))


class Characters(Base):

    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200))
    status = Column(String(50))
    species = Column(String(50))
    type = Column(String(100))
    gender = Column(String(50))


class CharactersAppearance(Base):

    __tablename__ = "characters_appearance"

    id = Column(Integer, primary_key=True, autoincrement=True)
    character_id = Column(Integer, ForeignKey("characters.id"))
    episode_id = Column(Integer, ForeignKey("episodes.id"))
    character = relationship("Characters", backref="episodes")
    episode = relationship("Episodes", backref="characters")


class Comments(Base):

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    character_id = Column(Integer, ForeignKey("characters.id"))
    episode_id = Column(Integer, ForeignKey("episodes.id"))
    author = Column(String(100))
    posted_on = Column(DateTime(timezone=True), server_default=func.now())
    comment = Column(Text())
    character = relationship("Characters", backref="comments")
    episode = relationship("Episodes", backref="comments")


Base.metadata.create_all(db)
