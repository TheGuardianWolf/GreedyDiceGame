from . import GreedyPlayer
from . import GreedyDice
from collections import Counter


class GreedyGame(object):
    def __init__(self):
        self.player_active = 0
        self.players = []
        self.dice = [GreedyDice() for x in range(6)]

    def player_add(self, name):
        self.players.append(GreedyPlayer(name))

    def player_remove(self, name):
        search = [i for i, p in enumerate(self.players) if p.name == name]

        for i in search:
            self.players.pop(i)

    def player_next(self):
        self.player_active = (self.player_active + 1) % len(self.player_active)

    def toggle_ruleset(self):
        pass

    def display_dice(self, outputFn):
        pass

    def display_choice(self, inputFn, outputFn):
        pass

    def roll(self):
        if self.selection_valid() or True:
            for dice in self.dice:
                dice.roll()

    def select(self, dice_number):
        self.dice[dice_number].toggle_lock()

    def selection_valid(self):
        selections = Counter()
        

    def stop(self):
        pass

    def main(self, inputFn, outputFn):
        while True:
            self.roll()
            self.display_dice()
            self.display_choice()
