from random import randint


class GreedyDie(object):
    def __init__(self, copy=None):
        if copy:
            self.value = copy.value
            self.locked = copy.locked
            self.selected = copy.selected
        else:
            self.value = 1
            self.locked = False
            self.selected = False

    def roll(self):
        if self.selected:
            self.locked = True
            self.selected = False

        if not self.locked:
            self.value = randint(1, 6)

    def select(self):
        self.selected = True

    def reset(self):
        self.locked = False
        self.selected = False
