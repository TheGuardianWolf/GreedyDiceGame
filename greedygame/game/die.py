from random import randint


class Die(object):
    def __init__(self):
        self.value = 1
        self.locked = False
        self.selected = False

    def copy(self, die):
        new_die = Die()
        new_die.value = self.value
        new_die.locked = self.locked
        new_die.selected = self.selected

    def roll(self):
        if self.selected:
            self.locked = True
            self.selected = False

        if not self.locked:
            self.value = randint(1, 6)

    def select(self):
        if not self.locked:
            self.selected = True
            return True
        return False

    def lock(self):
        self.selected = False
        self.locked = True

    def reset(self):
        self.locked = False
        self.selected = False
