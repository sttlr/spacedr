#!/usr/bin/env python3

import logging
from typing import List, Any
from datetime import datetime, timedelta

from .db import Card, Deck, get_session

logger = logging.getLogger(__name__)

THRESHOLDS = [
    timedelta(seconds=40),
    timedelta(hours=3),
    timedelta(hours=8),
    timedelta(days=1),
    timedelta(days=3),
    timedelta(days=7),
    timedelta(days=30)
]


@get_session(use_obj_session=True, commit=False, close=False)
def update_card(card: Card, answer: Any) -> None:
    '''Update card data.

    Usage::

        >>> spacedr.update_card(card, answer='43')
    '''
    card.reviews_count += 1

    if answer in card.answers:
        card.correct_count += 1
        level = card.level + 1
        card.last_correct = True
    else:
        level = card.level - 1
        if level < 0:  # If first wrong
            level = 0
        card.last_correct = False

    card.level = level

    if level == 7 or (card.reviews_count == 1 and card.level == 1):
        card.practiced = True
        card.due_date = None

    if answer not in card.answers:  # If wrong, review now
        level = 0

    card.due_date = datetime.now() + THRESHOLDS[level]

    session.commit()
    logger.info(f'Updated card with id: {card.id} to level: {card.level}, '
                f'due_date: {card.due_date}')


@get_session()
def get_cards_to_study(deck: Deck, num: int) -> List[Card]:
    '''Get cards that haven't been studied, limit quantity by ``num``.'''
    return list(session.query(Card)
                .filter(Card.deck_id == deck.id)
                .filter(Card.reviews_count == 0)
                .order_by(Card.id.asc())
                .limit(num))


@get_session()
def get_cards_to_review(deck: Deck) -> List[Card]:
    '''Get cards that can be reviewed.'''
    return list(session.query(Card)
                .filter(Card.deck_id == deck.id)
                .filter(Card.practiced == False)
                .filter(Card.reviews_count >= 1)
                .filter(Card.due_date <= datetime.now())
                .order_by(Card.due_date.asc()))
