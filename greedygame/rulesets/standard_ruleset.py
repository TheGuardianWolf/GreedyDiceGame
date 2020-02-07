from collections import defaultdict
from itertools import chain, groupby
from operator import itemgetter


def dice_counter(dice):
    dice_bins = defaultdict(list)
    for die in dice:
        dice_bins[die.value].append(die)
    return dice_bins


def flatten(li=[]):
    return list(chain.from_iterable(li))


class StandardRuleset(object):
    def __init__(self):
        self.name = "Standard"
        self.dice_rules = {
            # Straights (1, 2, 3, 4, 5, 6)
            "straight": {
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
            # Sets of three or above
            "three-or-more": {
                "matches": lambda dice: flatten(
                    dice_bin
                    for dice_bin in dice_counter(dice).values()
                    if len(dice_bin) >= 3
                ),
                "score": lambda matches: sum(
                    [
                        (value if value != 1 else 10) * 100 * 2 ** max(len(dice_bin) - 3, 0)
                        for value, dice_bin in dice_counter(matches).items()
                    ]
                ),
            },
            # Three or more pairs
            "three-pairs-or-more": {
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
                "score": lambda matches: 1000 * 2 ** max(int(len(matches) / 2) - 3, 0),
            },
            # Single ones
            "one": {
                "matches": lambda dice: [die for die in dice if die.value == 1],
                "score": lambda matches: len(matches) * 100,
            },
            # Single fives
            "five": {
                "matches": lambda dice: [die for die in dice if die.value == 5],
                "score": lambda matches: len(matches) * 50,
            }
        }

    def check_match(self, dice):
        matched_dice = set()
        available_dice = dice
        matches = {}
        for name, rule in self.dice_rules.items():
            match = rule["matches"](available_dice)
            matched_dice.update(set(match))
            available_dice = [die for die in available_dice if die not in matched_dice]
            matches[name] = match
        return matches

    def calculate_score(self, matches):
        matches_score = dict([(name, self.dice_rules[name]["score"](match)) for name, match in matches.items()])
        score = sum(matches_score.values())
        return score
