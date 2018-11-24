#!/usr/bin/env python3

from .db import Deck, Card, get_card_by_id, get_deck_by_id

from .port import export_deck, import_deck

from .spacedr import create_card, edit_card, delete_card, create_deck
from .spacedr import edit_deck, delete_deck

from .schedule import update_card, get_cards_to_study, get_cards_to_review

from . import errors

from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __author__, __license__, __copyright__

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s:'
                                  '%(funcName)s > %(message)s',
                              datefmt='%d/%m %I:%M:%S')

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)

logger.addHandler(handler)
