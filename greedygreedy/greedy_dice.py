from random import randint


class GreedyDice(object):
    def __init__(self):
        self.value = 1
        self.locked = False

    def roll(self):
        if not self.locked:
            self.value = randint(1, 6)

    def toggle_lock(self):
        self.locked = True

    def reset(self):
        self.value = 1
