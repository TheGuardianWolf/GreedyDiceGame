"""
MultibotClient is a Slackbot built to multiplex conversations to supported
chatbots.
"""
from .console_game_runner import ConsoleGameRunner
from .greedy_game import GreedyGame
from .greedy_player import GreedyPlayer
from .greedy_dice import GreedyDice


__version__ = '1.0.0'
__author__ = 'Jerry Fan'
__email__ = 'nano@pixelcollider.net'
__url__ = 'https://github.com/TheGuardianWolf/GreedyDiceGame'

__all__ = (
    'ConsoleGameRunner',
    'GreedyGame',
    'GreedyPlayer',
    'GreedyDice'
)
