class ConsoleGreedyIO(object):
    def __init__(self):
        pass

    def text(self, value):
        print(value)

    def dice(self, dice_values):
        print("Current dice:")
        print("")
        print("[" + "] [".join([str(dice.value) for dice in dice_values]) + "]")
        print("")

    def actions(self, actions):
        print("Actions available:")
        print("")
        for i, action in enumerate(actions):
            print("   {}. {}".format(i + 1, action))
        print("")

    def input(self, prompt=""):
        return input(prompt)
