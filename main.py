from greedygame.console import ConsoleGreedyRunner
from greedygame.game import GreedyGame

if __name__ == "__main__":
    game = GreedyGame()
    game_runner = ConsoleGreedyRunner(game)
    game_runner.play()
