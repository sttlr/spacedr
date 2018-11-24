API Documentation
=========================

This page covers all of the ``spacedr`` interfaces.

Main interface
--------------

.. automodule:: spacedr.spacedr
    :members:
    :undoc-members:

Scheduling the cards
--------------------

.. automodule:: spacedr.schedule
    :members: get_cards_to_study, get_cards_to_review, update_card

Operations with database
------------------------

.. automodule:: spacedr.db
    :members: get_deck_by_id, get_card_by_id, Deck, Card, db_init, get_db_path, get_session

Porting a deck
--------------

.. automodule:: spacedr.port
    :members:

Exceptions
----------

.. automodule:: spacedr.errors
    :members:
