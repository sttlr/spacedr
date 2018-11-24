#!/usr/bin/env python3

import os
import logging
from typing import List, Callable, Optional, Any
from functools import wraps
from datetime import datetime

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy import PickleType, Float
from sqlalchemy.ext.mutable import MutableList, MutableDict

from .errors import DeckNotFoundError, CardNotFoundError

logger = logging.getLogger(__name__)


def get_db_path() -> str:
    '''Get a path to the database.'''
    return os.path.join(os.path.join(os.getcwd(), 'spacedr'), 'spacedr.sqlite')


engine = create_engine('sqlite:///%s' % os.path.abspath(get_db_path()))
session_maker = sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()


def get_session(commit: bool=True, close: bool=True,
                use_obj_session: bool=False) -> Callable:
    '''Get a sqlalchemy ``session`` object applying parameters via decorator.

       :param commit: commit after making a change.
       :param close: finally close the session.
       :param use_obj_session: use object's session to make a change.
    '''

    def decorator(func) -> Callable:

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if use_obj_session:
                session = inspect(args[0]).session
            else:
                session = session_maker()

            try:
                func.__globals__['session'] = session
                result = func(*args, **kwargs)
                if commit:
                    session.commit()
                return result
            except Exception as e:
                session.rollback()
                logger.exception(e)
                raise
            finally:
                if close:
                    session.close()

        return wrapper
    return decorator


class Card(Base):
    '''A class used to create a card.'''

    __tablename__ = 'card'

    id: int = Column('id', Integer, primary_key=True, autoincrement=True)
    deck_id: int = Column('deck_id', Integer, ForeignKey('deck.id'),
                          nullable=False)
    question: str = Column('question', String, nullable=False)
    examples: List[str] = Column('examples', MutableList.as_mutable(PickleType),
                                 nullable=True)
    answers: List[str] = Column('answers', MutableList.as_mutable(PickleType),
                                nullable=False)
    level: int = Column('level', Integer, nullable=False, default=0)
    due_date: datetime = Column('due_date', DateTime, nullable=True,
                                default=None)
    reviews_count: int = Column('reviews_count', Integer, nullable=False,
                                default=0)
    last_correct: bool = Column('last_correct', Boolean, nullable=True,
                                default=None)
    practiced: bool = Column('practiced', Boolean, nullable=False,
                             default=False)
    other: dict = Column('other', MutableDict.as_mutable(PickleType),
                         nullable=True, default=None)


class Deck(Base):
    '''A class used to create a deck.'''

    __tablename__ = 'deck'

    id: int = Column('id', Integer, primary_key=True)
    name: str = Column('name', String, nullable=False)
    cards: List[Card] = relationship(Card, cascade='all', backref='deck')
    description: Optional[str] = Column('description', String)


def db_init() -> None:
    '''Initialise the database.'''
    os.makedirs(os.path.dirname(get_db_path()), exist_ok=True)
    Base.metadata.create_all(engine)
    logger.debug('The database was successfully initialised')


@get_session(close=False)
def get_deck_by_id(id: int) -> Deck:
    '''Get deck by id.

    :raises errors.DeckNotFoundError: No deck with given id.
    '''
    deck = session.query(Deck).filter(Deck.id == id).one_or_none()
    if not deck:
        raise DeckNotFoundError(f'There is no deck with id: {id}')
    logger.debug(f'Found a deck with id: {deck.id}')
    return deck


@get_session(close=False)
def get_card_by_id(id: int) -> Card:
    '''Get card by id.

    :raises errors.CardNotFoundError: No card with given id.
    '''
    card = session.query(Card).filter(Card.id == id).one_or_none()
    if not card:
        raise CardNotFoundError(f'There is no card with id: {id}')
    logger.debug(f'Found a card with id: {card.id}')
    return card
