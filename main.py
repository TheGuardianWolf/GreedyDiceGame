from greedygreedy import ConsoleGameRunner
from greedygreedy import GreedyGame

if __name__ == "__main__":
    game = GreedyGame()
    game_runner = ConsoleGameRunner(game)
    game_runner.play()
