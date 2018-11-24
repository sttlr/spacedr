spacedr
=======

Spaced Repetition API
---------------------

Enhance your learning speed with **Spaced Repetition** technique. It uses increasing intervals of time between card reviews.

But now you have **API**. Create cards, organise them into decks, study and actually review.

*And there is no* ``session`` *object to pass it everywhere.*

Installation
------------

.. code-block:: bash

    $ pip install spacedr

Usage
-----

At first, you need to import the module:

.. code-block:: python

    >>> import spacedr

And initialise the database:

.. code-block:: python

    >>> spacedr.db_init()

Create a deck
"""""""""""""

.. code-block:: python

    >>> spacedr.create_deck(name='Test Deck', description='Just a test.')

Get a deck
""""""""""

You can get a **deck id from a card** *(which you get using* ``get_cards_to_review`` *or* ``get_cards_to_study`` *functions)*:

.. code-block:: python

    >>> deck_id = card.deck_id

And then use this to get the ``deck`` object.

.. code-block:: python

    >>> deck = spacedr.get_deck_by_id(deck_id)

Create a card
"""""""""""""

.. code-block:: python

    >>> spacedr.create_card(deck,
    ...                     question='What is the meaning of life?',
    ...                     answers=[42, '42'])

Update a card
"""""""""""""

You have to update a card each time the user answers.

If answer is right, card's level will be increased, othervise decreased. And the card will be postponed accordingly.

.. code-block:: python

    >>> spacedr.update_card(card, answer='43')

Get cards to study
""""""""""""""""""

You will get a number of cards *(limited by* ``num``*)*, that haven't been practiced, in the given deck.

.. code-block:: python

    >>> spacedr.get_cards_to_study(deck, num=20)
    [...]

Get cards to review
"""""""""""""""""""

You will get a number of cards, that need to be reviewed, in the given deck.

.. code-block:: python

    >>> spacedr.get_cards_to_review(deck)
    [...]

Edit a deck
"""""""""""

You have to pass ``name`` and ``description`` as keyword arguments:

.. code-block:: python

    >>> spacedr.edit_deck(deck, name='test2', description='new one')

Edit a card
"""""""""""

You have to pass ``deck_id`` *(replace to an another deck)*, ``question`` and ``answers`` as keyword arguments:

.. code-block:: python

    >>> spacedr.edit_card(card, deck_id=deck_id, question='What is life?',
    ...                   answers=[42])

Delete a deck
"""""""""""""

The cards assigned to given deck will be deleted too:

.. code-block:: python

    >>> spacedr.delete_deck(deck)

Delete a card
"""""""""""""

.. code-block:: python

    >>> spacedr.delete_card(card)

Export a deck
"""""""""""""

Export the deck from a file descriptor:

.. code-block:: python

    >>> with open('mydeck.json', 'w') as file_d:
    ...     spacedr.export_deck(deck, file_d)


Import a deck
"""""""""""""

Import the deck from a file descriptor:

.. code-block:: python

    >>> with open('mydeck.json') as file_d:
    ...     spacedr.import_deck(deck, file_d)

.. note::

    The deck and the cards will be imported as new ones. The old won't be removed.
