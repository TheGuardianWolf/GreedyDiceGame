from greedygame.game import GreedyPlayer
from greedygame.game import GreedyDie
from collections import defaultdict
from itertools import chain, groupby
from operator import itemgetter


class GreedyGame(object):
    def __init__(self):
        def dice_counter(dice):
            dice_bins = defaultdict(list)
            for die in dice:
                dice_bins[die.value].append(die)
            return dice_bins

        def flatten(li=[]):
            return list(chain.from_iterable(li))

        self.die_faces = 6
        self.active_player = 0
        self.active_ruleset = 0
        self.first_to_threshold = None
        self.players = []
        self.dice = [GreedyDie() for x in range(self.die_faces)]
        self.rulesets = [
            {
                "name": "Standard",
                "score_threshold": 10000,
                "dice_rules": [
                    {  # Straights (1, 2, 3, 4, 5, 6)
                        "matches": lambda dice: flatten(
                            group
                            for group in [
                                list(map(itemgetter(1), g))
                                for k, g in groupby(
                                    enumerate(dice), lambda ix: ix[0] - ix[1].value
                                )
                            ]
                            if len(group) >= 6
                        ),
                        "score": lambda matches: sum(
                            900 * 2 ** max(len(group) - 5, 0)
                            for group in [
                                list(map(itemgetter(1), g))
                                for k, g in groupby(
                                    enumerate(matches), lambda ix: ix[0] - ix[1].value
                                )
                            ]
                        ),
                    },
                    {  # Sets of three or above
                        "matches": lambda dice: flatten(
                            dice_bin
                            for dice_bin in dice_counter(dice).values()
                            if len(dice_bin) >= 3
                        ),
                        "score": lambda matches: sum(
                            [
                                (value if value != 1 else 10)
                                * 100
                                * 2 ** max(len(dice_bin) - 3, 0)
                                for value, dice_bin in dice_counter(matches).items()
                            ]
                        ),
                    },
                    {  # Three or more pairs
                        "matches": lambda dice: flatten(
                            *[
                                dice_bins
                                for dice_bins in [
                                    [
                                        dice_bin
                                        for dice_bin in dice_counter(dice).values()
                                        if len(dice_bin) == 2
                                    ]
                                ]
                                if len(dice_bins) >= 3
                            ]
                        ),
                        "score": lambda matches: 1000
                        * 2 ** max(int(len(matches) / 2) - 3, 0),
                    },
                    {  # Single ones
                        "matches": lambda dice: [die for die in dice if die.value == 1],
                        "score": lambda matches: len(matches) * 100,
                    },
                    {  # Single fives
                        "matches": lambda dice: [die for die in dice if die.value == 5],
                        "score": lambda matches: len(matches) * 50,
                    },
                ],
            }
        ]

    def player_add(self, name):
        self.players.append(GreedyPlayer(name))

    def player_remove(self, name):
        search = [i for i, p in enumerate(self.players) if p.name == name]

        for i in search:
            self.players.pop(i)

    def player_next(self):
        self.active_player = (self.active_player + 1) % len(self.players)

    def player_reset(self):
        for player in self.players:
            player.reset()

    def toggle_ruleset(self):
        self.active_ruleset = (self.active_ruleset + 1) % len(self.rulesets)

    def display_dice(self, greedy_io):
        dice_copy = [GreedyDie(copy=die) for die in self.dice]

        greedy_io.dice(dice_copy)

    def display_choice(self, greedy_io, choices, retry=True):
        greedy_io.actions(choices)

        choice = None
        while choice is None:
            try:
                choice = int(greedy_io.input("Please select an option: ")) - 1
            except ValueError as e:
                choice = None
            else:
                if choice <= len(choices) and choice > 0:
                    return choice
                else:
                    choice = None
            finally:
                if not retry:
                    return choice

    def roll(self):
        for dice in self.dice:
            dice.roll()

    def dice_select(self, dice_number):
        self.dice[dice_number].select()

    def dice_validate(self, selected, locked):
        selected_dice = [
            die
            for die in self.dice
            if (
                (die.selected is selected or die.selected is None)
                and (die.locked is locked or die.locked is None)
            )
        ]

        ruleset = self.rulesets[self.active_ruleset]
        score = 0
        for rule in ruleset["dice_rules"]:
            rule_matches = rule["matches"](selected_dice)
            for match in rule_matches:
                selected_dice.remove(match)
            score += rule["score"](rule_matches)
        return score

    def dice_reset(self):
        for die in self.dice:
            die.reset()

    def is_game_over(self):
        if self.first_to_threshold is not None:
            return (self.active_player + 1) % len(
                self.players
            ) == self.first_to_threshold
        return False

    def highest_score(self):
        return max([player.score for player in self.players])

    def game_can_start(self):
        return len(self.players) > 0

    def player_turn(self, greedy_io):
        greedy_io.text("Player {}'s turn".format(self.players[self.active_player].name))
        self.dice_reset()

        next_turn = False
        while not next_turn:
            self.roll()
            self.display_dice(greedy_io)

            possible_score = self.dice_validate(False, False)

            if possible_score == 0:
                greedy_io.text("No dice of point value were rolled!")
                self.players[active_player].busts += 1
                break

            turn_ok = False
            while not turn_ok:
                choice = self.display_choice(greedy_io, ["Select", "Roll", "Stop"])
                if choice == 1:
                    selection = self.display_choice(
                        greedy_io,
                        ["Dice {}".format(i) for i in range(1, self.die_faces + 1)],
                    )
                    self.dice_select(selection)
                elif choice == 2:
                    selected_score = self.dice_validate(True, False)
                    if selected_score > 0:
                        self.players[active_player].score += selected_score
                        turn_ok = True
                        if all([die.selected or die.locked for die in self.dice]):
                            self.dice_reset()
                    else:
                        greedy_io.text("You must select at least one scoring dice!")
                elif choice == 3:
                    selected_score = self.dice_validate(True, False)
                    if (
                        self.first_to_threshold is not None) and (
                        selected_score <= self.highest_score()
                    ):
                        greedy_io.text("You must keep rolling until you beat the \
                        highest score or bust!")
                    elif selected_score > 0:
                        turn_ok = True
                        next_turn = True
                    else:
                        greedy_io.text("You must select at least one scoring dice!")

    def main(self, greedy_io):
        if not self.game_can_start():
            return

        self.player_reset()

        while True:
            self.player_turn(greedy_io)

            if self.first_to_threshold is None:
                if (
                    self.players[self.active_player].score
                    >= self.rulesets[self.active_ruleset]["score_threshold"]
                ):
                    self.first_to_threshold = self.active_player
                    greedy_io.text(
                        "Player {} has passed {} points! Remaining players must roll \
                        until they beat this score or bust.".format(
                            self.players[self.first_to_threshold].name
                        ),
                        self.rulesets[self.active_ruleset]["score_threshold"],
                    )
            else:
                if self.is_game_over():
                    highest_score = self.highest_score()
                    winner = [player for player in self.players if (
                        player.score == highest_score
                    )]
                    greedy_io.text(
                        "Player {} has won with {} points!".format(
                            winner.name, winner.score
                        )
                    )
                    break

            self.player_next()
