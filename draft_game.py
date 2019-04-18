from collections import defaultdict
from random import randrange

NB_CARDS = 50


class Card(object):
    RED_MAX = 10
    SUM_MAX = 15

    def __init__(self, red, blue):
        self.red = red
        self.blue = blue

    @property
    def partial_repr(self):
        return '({}, {})'.format(self.red, self.blue)

    def __repr__(self):
        return 'Card{}'.format(self.partial_repr)

    def value(self, active_red=True):
        return self.red if active_red else self.blue

    @property
    def sum(self):
        return self.red + self.blue

    @classmethod
    def generate(cls):
        """Generate a random card according to the class constraints."""
        red = randrange(cls.RED_MAX + 1)
        blue = randrange(cls.RED_MAX - red, cls.SUM_MAX - red + 1)
        return cls(red, blue)


class IdCard(object):
    def __init__(self, uid, card):
        self.id = uid
        self.card = card

    def __repr__(self):
        return 'Card #{} {}'.format(self.id, self.card.partial_repr)

    @property
    def text(self):
        return (
            'ID: %s' % self.id,
            '',
            'Red : %s' % self.card.red,
            'Blue: %s' % self.card.blue,
        )


class CardCollection(object):
    def __init__(self):
        self._auto_id = 1
        self.idcards = {}

    @classmethod
    def from_cards(cls, cards):
        collection = cls()
        for card in cards:
            collection.add_card(card)

        return collection

    @classmethod
    def generate(cls, nb_cards=None):
        if nb_cards is None:
            nb_cards = NB_CARDS

        return cls.from_cards(Card.generate() for _ in xrange(nb_cards))

    def add_card(self, card):
        """Give an ID to a card and add it to the collection."""
        auto_id = self._auto_id
        self.idcards[auto_id] = IdCard(auto_id, card)
        self._auto_id += 1

    @staticmethod
    def sorted_line(line, active_red=True):
        """Sort a row of cards in-place and return it."""
        line.sort(key=lambda idcard: idcard.card.value(active_red=active_red))
        return line

    def sorted(self, active_red=True):
        """Provide a 2D sorted representation of the cards,
        first by total value, then by value for active player.
        """
        collection = defaultdict(list)
        for idcard in self.idcards.itervalues():
            collection[idcard.card.sum].append(idcard)

        result = collection.items()
        result.sort()

        return [self.sorted_line(line) for _, line in result]
