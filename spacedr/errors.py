class DeckNotFoundError(Exception):
    '''No deck with given id.'''


class CardNotFoundError(Exception):
    '''No card with given id.'''


class CardAlreadyExists(Exception):
    '''There is a card with the same question.'''
