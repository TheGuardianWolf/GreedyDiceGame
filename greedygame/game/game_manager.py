from greedygame.game import Player
from greedygame.game import Die


class GameManager(object):
    def __init__(self, ruleset, number_of_dice=6, threshold_score=10000):
        self.ruleset = ruleset
        self.number_of_dice = number_of_dice
        self.threshold_score = threshold_score
        self.player_active = -1
        self.player_winner = -1
        self.player_first_to_threshold = -1
        self.players = []
        self.dice = [Die() for x in range(self.number_of_dice)]

    def player_add(self, name):
        self.players.append(Player(name))

    def player_remove(self, name):
        for player in self.players:
            if player.name == name:
                self.players.remove(player)

    def next_player(self):
        self.player_active = (self.player_active + 1) % len(self.players)

    def dice_roll(self):
        for dice in self.dice:
            dice.roll()

    def dice_select(self, dice_number):
        return self.dice[dice_number].select()

    def dice_reset(self):
        for die in self.dice:
            die.reset()

    def dice_max_score(self):
        dice = [
            die for die in self.dice if not die.locked
        ]

        matches = self.ruleset.check_match(dice)
        score = self.ruleset.calculate_score(matches)
        return score

    def dice_score(self):
        selected_dice = [
            die for die in self.dice if die.selected
        ]

        matches = self.ruleset.check_match(selected_dice)
        score = self.ruleset.calculate_score(matches)
        return score

    def game_reset(self):
        for player in self.players:
            player.reset()
        self.player_active = -1
        self.player_winner = -1
        self.dice = [Die() for x in range(self.number_of_dice)]

    def highest_player_score(self):
        return max([player.score for player in self.players])

    def is_game_over(self):
        if self.player_winner >= 0 and self.player_winner < len(self.players):
            return True
        return False

    def game_can_start(self):
        return len(self.players) > 0

    def display_choice(self, greedy_io, choices, retry=True):
        greedy_io.actions(choices)

        choice = None
        while choice is None:
            try:
                choice = int(greedy_io.input("Please select an option: ")) - 1
            except ValueError:
                choice = None
            else:
                if choice <= len(choices) and choice > 0:
                    return choice
                else:
                    choice = None
            finally:
                if not retry:
                    return choice

    def display_dice(self, greedy_io):
        greedy_io.dice(self.dice)

    def player_turn(self, greedy_io):
        greedy_io.text("Player {}'s turn".format(self.players[self.player_active].name))
        self.dice_reset()

        next_turn = False
        while not next_turn:
            self.display_dice(greedy_io)
            initial_roll = False
            action_ok = False
            turn_score = 0

            def action_select():
                selection = self.display_choice(
                    greedy_io,
                    ["Dice {}".format(i) for i in range(1, self.number_of_dice + 1)],
                )
                if not self.dice_select(selection):
                    greedy_io.text("Cannot select a locked die!")

            def action_roll():
                global turn_score
                global turn_ok
                global action_ok
                global next_turn

                selected_score = self.dice_score()
                if selected_score > 0 or initial_roll:
                    turn_score += selected_score
                    action_ok = True
                    if all([die.selected or die.locked for die in self.dice]):
                        self.dice_reset()

                    for die in self.dice:
                        if die.selected:
                            die.lock()
                    self.dice_roll()
                    max_score = self.dice_max_score()
                    if max_score == 0:
                        greedy_io.text("No dice of point value were rolled!")
                        self.players[self.player_active].busts += 1
                        action_ok = True
                        turn_ok = True
                        turn_score = 0
                else:
                    greedy_io.text("You must select at least one scoring dice!")

            def action_stop():
                global turn_score
                global action_ok
                global next_turn
                selected_score = self.dice_score()
                if (
                    self.player_first_to_threshold > 0 and self.player_first_to_threshold < len(self.players)) and (
                    selected_score <= self.highest_score()
                ):
                    greedy_io.text("You must keep rolling until you beat the \
                    highest score or bust!")
                elif selected_score > 0:
                    turn_score += selected_score
                    action_ok = True
                    next_turn = True
                else:
                    greedy_io.text("You must select at least one scoring dice!")

            while not action_ok:
                if not initial_roll:
                    choice = self.display_choice(greedy_io, ["Roll"])
                    print(initial_roll)
                    if choice == 0:
                        action_roll()
                        initial_roll = True
                else:
                    choice = self.display_choice(greedy_io, ["Select", "Roll", "Stop"])
                    if choice == 0:
                        action_select()
                    elif choice == 1:
                        action_roll()
                    elif choice == 2:
                        action_stop()

            self.players[self.player_active].score += turn_score

    def take_turn(self, greedy_io):
        while True:
            self.player_turn(greedy_io)

            if self.first_to_threshold < 0:
                if self.players[self.player_active].score >= self.threshold_score:
                    self.player_first_to_threshold = self.player_active
                    greedy_io.text(
                        "Player {} has passed {} points! Remaining players must roll \
                        until they beat this score or bust.".format(
                            self.players[self.player_first_to_threshold].name
                        ),
                        self.threshold_score,
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

            self.next_player()

    def main(self, greedy_io):
        if not self.game_can_start():
            return

        self.game_reset()

        self.take_turn(greedy_io)
