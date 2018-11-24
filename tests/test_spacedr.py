#!/usr/bin/env python3

from typing import List
import pytest
import spacedr

'''Run tests sequentially. Other way, it fails.'''


@pytest.mark.parametrize('name,description,id', [('test', None, 1),
                                                 ('what', 'nothing', 2)],)
def test_create_deck(name: str, description: str, id: int) -> None:
    spacedr.create_deck(name, description)
    deck = spacedr.get_deck_by_id(id)

    assert deck.name == name
    assert deck.description == description


@pytest.mark.parametrize('name,description,id', [('what', 'nothing', 1),
                                                 ('test', None, 2)])
def test_edit_deck(name: str, description: str, id: int) -> None:
    deck = spacedr.get_deck_by_id(id)
    spacedr.edit_deck(deck, name=name, description=description)

    assert deck.name == name
    assert deck.description == description or 'nothing'


@pytest.mark.parametrize('id', [2])
def test_delete_deck(id: int) -> None:
    deck = spacedr.get_deck_by_id(id)
    spacedr.delete_deck(deck)

    with pytest.raises(spacedr.errors.DeckNotFoundError):
        spacedr.get_deck_by_id(id)


@pytest.mark.parametrize('deck_id,card_id,question,answers,examples,other',
                         [(1, 1, 'meaning of life', [42, '42'], ['42dot'],
                           {'key1': 'val1', 'key2': 'val2'}),
                          (1, 2, 'nothing else than 0', [0], ['0', 0.0, 0],
                           {'key3': ['val3', 'val']}),
                          (1, 3, 'just third', [3], ['only 3', 3], {'4': 5}),
                          (1, 4, 'only thing you need to know', [8], ['what'],
                           {'hello': ['gbye']}),
                          (1, 5, 'five.', [5], [5, 5.5], {'key': {'k': 'v'}})])
def test_create_card(deck_id: int, card_id: int, question: str,
                     answers: List[str], examples: List[str],
                     other: dict) -> None:
    deck = spacedr.get_deck_by_id(deck_id)
    spacedr.create_card(deck, question, answers, examples, other)

    card = spacedr.get_card_by_id(card_id)

    assert card.question == question
    assert card.answers == answers
    assert card.examples == examples
    assert card.other == other


@pytest.mark.parametrize('deck_id,card_id,question,answers,examples,other',
                         [(1, 1, 'nothing else than 0', [0], ['4'], {'n': 5}),
                          (1, 2, 'life meaning', [42, '42'], [2], {'l': 'f'})])
def test_edit_card(deck_id: int, card_id: int, question: str,
                   answers: List[str], examples: List[str],
                   other: dict) -> None:
    card = spacedr.get_card_by_id(card_id)
    spacedr.edit_card(card, deck_id=deck_id, question=question,
                      answers=answers, examples=examples, other=other)

    assert card.deck_id == deck_id
    assert card.question == question
    assert card.answers == answers
    assert card.examples == examples
    assert card.other == other


@pytest.mark.parametrize('id', [3])
def test_delete_card(id: int) -> None:
    card = spacedr.get_card_by_id(id)
    spacedr.delete_card(card)

    with pytest.raises(spacedr.errors.CardNotFoundError):
        spacedr.get_card_by_id(id)


@pytest.mark.parametrize('id,answer', [(1, '11'), (2, 42), (2, '42')])
def test_update_card(id: int, answer: str) -> None:
    card = spacedr.get_card_by_id(id)
    old_data = {'due_date': card.due_date, 'reviews_count': card.reviews_count}

    spacedr.update_card(card, answer)

    assert card.due_date != old_data['due_date']
    assert card.reviews_count == old_data['reviews_count'] + 1


@pytest.mark.parametrize('deck_id,num', [(1, 1), (1, 3)])
def test_get_cards_to_study(deck_id: int, num: int) -> None:
    deck = spacedr.get_deck_by_id(deck_id)
    cards_to_study = spacedr.get_cards_to_study(deck, num)

    assert len(cards_to_study) <= num

    for card in cards_to_study:
        assert card.deck_id == deck.id
        assert card.level == 0
        assert card.due_date == None
        assert card.reviews_count == 0


@pytest.mark.parametrize('deck_id', [1])
def test_get_cards_to_review(deck_id: int) -> None:
    deck = spacedr.get_deck_by_id(deck_id)
    cards_to_review = spacedr.get_cards_to_review(deck)

    for card in cards_to_review:
        assert card.deck_id == deck.id
        assert card.due_date != None
        assert card.reviews_count != 0


@pytest.mark.parametrize('id', [10, 42])
def test_error_deck_not_found(id: int) -> None:
    with pytest.raises(spacedr.errors.DeckNotFoundError):
        spacedr.get_deck_by_id(id)


@pytest.mark.parametrize('id', [15, 66])
def test_error_card_not_found(id: int) -> None:
    with pytest.raises(spacedr.errors.CardNotFoundError):
        spacedr.get_card_by_id(id)


@pytest.mark.parametrize('card_id', [(2)])
def test_error_card_already_exists(card_id: int) -> None:
    card = spacedr.get_card_by_id(card_id)
    deck = spacedr.get_deck_by_id(card.deck_id)

    with pytest.raises(spacedr.errors.CardAlreadyExists):
        try:
            spacedr.create_card(deck, question=card.question,
                                answers=card.answers)
        except spacedr.errors.CardAlreadyExists:
            raise
