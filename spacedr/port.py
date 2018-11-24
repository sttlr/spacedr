#!/usr/bin/env python3

import logging
import json
from typing import IO, Any

from .db import Deck, Card, get_session

logger = logging.getLogger(__name__)


def export_deck(deck: Deck, fd: IO[Any]) -> None:
    '''Export a deck to a file descriptor.

    Usage::

        >>> with open('mydeck.json', 'w+') as fd:
        ...     spacedr.export_deck(deck, fd)
    '''
    json.dump({'name': deck.name,
               'description': deck.description,
               'cards': [{'question': card.question,
                          'answers': card.answers,
                          } for card in deck.cards]
               }, fd, separators=(',', ':'), check_circular=False)
    logger.info('The deck was successfully exported.')


@get_session()
def import_deck(fd: IO[Any]) -> None:
    '''Import a deck from a file descriptor as the new one.
    The old won't be removed.

    Usage::

        >>> with open('mydeck.json') as fd:
        ...     spacedr.import_deck(fd)
    '''
    try:
        deck_obj = json.load(fd)
    except Exception as e:
        raise e

    deck = Deck(name=deck_obj['name'], description=deck_obj['description'])
    session.commit()

    for card_obj in deck_obj['cards']:
        card = Card(deck_id=deck.id, question=card_obj['question'],
                    answers=card_obj['answers'])
        deck.cards.append(card)

    session.add(deck)
    logger.info('The deck was successfully imported.')
