#!/usr/bin/env python3

import logging
from typing import List

from .db import Card, Deck, get_session, get_deck_by_id
from .errors import CardAlreadyExists, DeckNotFoundError

logger = logging.getLogger(__name__)


@get_session(use_obj_session=True, commit=False, close=False)
def create_card(deck: Deck, question: str, answers: List[str],
                examples: List[str]=None, other: dict=None) -> None:
    '''Create a card.

    :raises errors.CardAlreadyExists: There is a card in the same deck with the same name.

    Usage::

        >>> spacedr.create_card(deck,
        ...                     question='What is the meaning of life?',
        ...                     answers=[42, '42'])
    '''
    if session.query(Card).filter(Card.deck_id == deck.id)\
       .filter(Card.question == question).one_or_none():
        raise CardAlreadyExists(f'There is a card in the same deck with the '
                                f'same question: {question}')

    card = Card(deck_id=deck.id, question=question, answers=answers,
                examples=examples, other=other)
    deck.cards.append(card)

    session.add(card)
    session.commit()
    logger.info(f'Created card with id: {card.id}')


@get_session(use_obj_session=True, commit=False, close=False)
def edit_card(card: Card, **kwargs) -> None:
    '''Edit card's deck_id, question and answers.

    :param int deck_id: move the card to a different deck.question.
    :param str question: change the card's question.
    :param list answers: set the new answers to a card.

    :raises errors.DeckNotFoundError: can't find deck with given ``deck_id``

    Usage:

        >>> spacedr.edit_card(card, deck_id=deck_id, question='What is life?',
        ...                   answers=[42])
    '''
    deck_id = kwargs.get('deck_id', None) or card.deck_id
    try:
        get_deck_by_id(deck_id)
    except DeckNotFoundError:
        raise

    question = kwargs.get('question', None) or card.question
    answers = kwargs.get('answers', None) or card.answers
    examples = kwargs.get('examples', None) or card.examples
    other = kwargs.get('other', None) or card.other

    card.deck_id = deck_id
    card.question = question
    card.answers = answers
    card.examples = examples
    card.other = other

    session.commit()
    logger.info(f'Edited card with id: {card.id}. Assigned it to the deck '
                f'with id: {deck_id}, question: {card.question}, answers: '
                f'{card.answers}, examples: {card.examples}, other: '
                f'{card.other}')


@get_session(use_obj_session=True)
def delete_card(card: Card) -> None:
    '''Delete a card.'''
    session.delete(card)
    logger.info(f'Deleted card with id: {card.id}')


@get_session(commit=False)
def create_deck(name: str, description: str=None) -> None:
    '''Create a deck.

    Usage::

        >>> spacedr.create_deck(name='Test Deck', description='Just a test.')
    '''
    deck = Deck(name=name, description=description)
    session.add(deck)
    session.commit()
    logger.info(f'Created deck with id: {deck.id}')


@get_session(use_obj_session=True, commit=False, close=False)
def edit_deck(deck: Deck, **kwargs) -> None:
    '''Edit deck's name, description.

    :param str name: new name to the deck.
    :param str description: assign description to the deck.

    Usage::

        >>> spacedr.edit_deck(deck, name='test2', description='new one')
    '''
    name = kwargs.get('name', None) or deck.name
    description = kwargs.get('description', None) or deck.description

    deck.name = name
    deck.description = description

    session.commit()
    logger.info(f'Edited deck with id: {deck.id}. name: {deck.name}, '
                f'description: {deck.description}')


@get_session(use_obj_session=True)
def delete_deck(deck: Deck) -> None:
    '''Delete a deck.'''
    session.delete(deck)
    logger.info(f'Deleted deck with id: {deck.id}')
