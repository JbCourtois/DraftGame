# -*- coding: utf-8 -*-
import codecs
import sys

from draft_game import CardCollection
from table_draw import CollectionDraw
import settings

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())


class Game(object):
    def __init__(self):
        self.score_red = 0
        self.score_blue = 0
        self.collection = CardCollection.generate()
        self.is_red_turn = True

    @property
    def nb_cards(self):
        return len(self.collection)

    @property
    def is_player_turn(self):
        return not (self.is_red_turn ^ settings.PLAYER_IS_RED)

    def run(self):
        while self.nb_cards > settings.LEFTOVER_CARDS:
            run_turn_method = (
                self.run_player_turn if self.is_player_turn
                else self.run_ai_turn
            )
            run_turn_method()
            self.is_red_turn ^= True

        self.end()

    def end(self):
        """TODO"""
        print('Game over.')
        print()
        exit()

    def flush_ui(self):
        """TODO"""
        pass

    def score_card(self, idcard, active_red=True):
        card = idcard.card
        if active_red:
            self.score_red += card.red
        else:
            self.score_blue += card.blue

    def print_game_status(self):
        print('\n'.join([
            'There are {} cards available.'.format(self.nb_cards),
            '(the game ends when only {} cards remain)'.format(settings.LEFTOVER_CARDS),
        ]))
        print()

        table = CollectionDraw(self.collection, active_red=settings.PLAYER_IS_RED)
        print(table.format())
        print()

        players = (settings.AI_NAME, settings.PLAYER_NAME)
        print('\n'.join([
            'Scores:',
            '\tRed ({}): {}'.format(players[int(settings.PLAYER_IS_RED)], self.score_red),
            '\tBlue ({}): {}'.format(players[1 - int(settings.PLAYER_IS_RED)], self.score_blue),
        ]))
        print()

    def run_player_turn(self):
        card_id = None
        while not card_id:
            self.flush_ui()
            print('Your turn.')
            print()

            self.print_game_status()

            card_id = self.player_pick()

        idcard = self.collection.idcards.pop(card_id)
        self.score_card(idcard, active_red=settings.PLAYER_IS_RED)

    def run_ai_turn(self):
        """TODO"""
        print('AI passes.')
        print()

    def player_pick(self):
        idcard = self.player_ask_pick()
        print()
        if self.player_confirm(idcard):
            print()
            return idcard.id

    def player_ask_pick(self):
        while True:
            try:
                card_id = int(input('Pick a card, typing its ID: '))
            except ValueError:
                print('Please type a valid number!')
                continue

            try:
                return self.collection.idcards[card_id]
            except KeyError:
                print('Card #{} not found. Please type a valid ID!'.format(card_id))
                continue

    def player_confirm(self, idcard):
        """TODO"""
        return True
