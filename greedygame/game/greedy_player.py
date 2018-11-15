class GreedyPlayer(object):
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.busts = 0

    def reset(self):
        self.score = 0
        self.busts = 0
