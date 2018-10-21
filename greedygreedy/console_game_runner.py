class ConsoleGameRunner(object):
    def __init__(self, game):
        self.game = game

    def inputFn(self, prompt):
        return input(prompt)

    def outputFn(self, value, type=None):
        print(value)

    def menu(self):
        menu_options = [{
                'description': 'Add Player',
                'action': self.game.player_add,
                'arguments': ['name']
            }, {
                'description': 'Remove Player',
                'action': self.game.player_remove,
                'arguments': ['name']
            }, {
                'description': 'Start Game',
                'action': self.game.main,
                'arguments': ['inputFn', 'outputFn']
            }, {
                'description': 'Toggle Ruleset',
                'action': self.game.toggle_ruleset,
                'arguments': []
            }, {
                'description': 'Exit',
                'action': exit,
                'arguments': []
            }
        ]

        supplied_args = {
            'inputFn': self.inputFn,
            'outputFn': self.outputFn
        }

        def invalid():
            self.outputFn('Error: Entered value is invalid.')

        self.outputFn('Greedy Dice Menu\n')

        for i, option in enumerate(menu_options):
            print('    {}. {}'.format(i + 1, option['description']))

        self.outputFn('')

        selected = None
        try:
            selected = int(self.inputFn('Select option: ')) - 1
        except ValueError as e:
            invalid()
            return False

        if selected < len(menu_options) and selected >= 0:
            args = []

            for arg_name in menu_options[selected]['arguments']:
                args.append(supplied_args.get(
                    arg_name,
                    self.inputFn('Enter {}: '.format(arg_name))
                ))

            menu_options[selected]['action'](*args)
        else:
            invalid()
            return False

        print('')
        return True

    def play(self):
        try:
            while True:
                self.menu()
        except KeyboardInterrupt as e:
            exit()
