from greedygame.console import ConsoleGreedyIO


class ConsoleGreedyRunner(object):
    def __init__(self, game):
        self.game = game
        self.io = ConsoleGreedyIO()

    def menu(self):
        menu_options = [
            {
                "description": "Add Player",
                "action": self.game.player_add,
                "arguments": ["name"],
            },
            {
                "description": "Remove Player",
                "action": self.game.player_remove,
                "arguments": ["name"],
            },
            {
                "description": "Start Game",
                "action": self.game.main,
                "arguments": ["greedy_io"],
            },
            {
                "description": "Toggle Ruleset",
                "action": self.game.toggle_ruleset,
                "arguments": [],
            },
            {"description": "Exit", "action": exit, "arguments": []},
        ]

        supplied_args = {"greedy_io": self.io}

        def invalid():
            self.io.text("Error: Entered value is invalid.")

        self.io.text("Greedy Dice Menu\n")

        for i, option in enumerate(menu_options):
            print("    {}. {}".format(i + 1, option["description"]))

        self.io.text("")

        selected = None
        try:
            selected = int(self.io.input("Select option: ")) - 1
        except ValueError as e:
            invalid()
            return False

        if selected < len(menu_options) and selected >= 0:
            args = []

            for arg_name in menu_options[selected]["arguments"]:
                arg = supplied_args.get(arg_name, None)
                if arg is None:
                    self.io.input("Enter {}: ".format(arg_name))
                args.append(arg)

            menu_options[selected]["action"](*args)
        else:
            invalid()
            return False

        print("")
        return True

    def play(self):
        try:
            while True:
                self.menu()
        except KeyboardInterrupt as e:
            exit()
