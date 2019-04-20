# -*- coding: utf-8 -*-
from collections import defaultdict
from random import randrange

import settings


class Card(object):
    def __init__(self, red, blue):
        self.red = red
        self.blue = blue
        self.sum = red + blue

    @classmethod
    def generate(cls):
        """Generate a random card according to the class constraints."""
        red = randrange(settings.RED_MAX + 1)
        blue = randrange(settings.RED_MAX - red, settings.SUM_MAX - red + 1)
        return cls(red, blue)

    def value(self, active_red=True):
        return self.red if active_red else self.blue

    def dominates(self, card2, active_red=True):
        """Sometimes a card is strictly better than another,
        independently of the rest of the position.
        This method x.dominates(y) detects some cases where x is better than y.
        """
        v_self = self.value(active_red=active_red)
        v_2 = card2.value(active_red=active_red)
        if v_self < v_2:
            return False
        if self.sum < card2.sum:
            return False

        return (self.red, self.blue) != (card2.red, card2.blue)

    @property
    def partial_repr(self):
        return '({}, {})'.format(self.red, self.blue)

    def __repr__(self):
        return 'Card{}'.format(self.partial_repr)


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
            nb_cards = settings.NB_CARDS

        return cls.from_cards(Card.generate() for _ in range(nb_cards))

    def add_card(self, card):
        """Give an ID to a card and add it to the collection."""
        auto_id = self._auto_id
        self.idcards[auto_id] = IdCard(auto_id, card)
        self._auto_id += 1

    @staticmethod
    def sorted_line(line, active_red=True):
        """Sort a row of cards in-place and return it."""
        line.sort(
            key=lambda idcard: idcard.card.value(active_red=active_red),
            reverse=True,
        )
        return line

    def sorted(self, active_red=True):
        """Provide a 2D sorted representation of the cards,
        first by total value, then by value for active player.
        """
        collection = defaultdict(list)
        for idcard in self.idcards.values():
            collection[idcard.card.sum].append(idcard)

        result = list(collection.items())
        result.sort(reverse=True)

        return [self.sorted_line(line) for _, line in result]
