class GreedyPlayer(object):
    def __init__(self, name):
        self.name = name
        self.score = 0

    def add_score(self, value):
        self.score += value

    def reset(self):
        self.score = 0
