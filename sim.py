from random import Random

class Player:
    amount_of_me = 0
    def __init__(self, name=None):
        if not Name:
            self.amount_of_me += 1
            self.name = "{}{}".format(
                self.__class__.__name__,
                self.amount_of_me)
        self.hand = list(range(2,14))
        self.wins = []

class DummiePlayer(Player):
    def __init__(self, *args, rngchoose=None, rngthree=None, **kwargs):
        super().__init__(*args, **kwargs)
        if not rngchoose:
            rngchoose = Random()
        if not rngtie:
            rngtie = Random()
        self.rngchoose = rngchoose
        self.rngtie = rngtie

    def chooseone(self):
        return self.rngchoose.randrange(len(self.hand))

    def choosetie(self, players):
        selection = self.rngtie.sample(range(len(self.hand)), 4)
        return selection[:-1], selection[-1]

class HumanPlayer(Player):
    def chooseone(self):
        print("==> {} <==".format(self.name))
        self.hand.sort()
        while True:
            print()
            print("Here is your hand:")
            print(" " * 3, ', '.join(map(str, self.hand)))
            try:
                choice = int(input("Which card do you choose? "))
                idx = self.hand.index(choice)
            except ValueError:
                print("That's not a valid choice, dummie!")
                continue
            return idx

    def choosetie(self, players):
        print("==> {} <==".format(self.name))
        # we know the hand must be sorted already
        while True:
            print()
            print("There was a tie between you and {} other player{}.".format(
                    len(players), "s" if players != 1 else ""
                )
            )
            print("Here is your hand:")
            print(" " * 3, ', '.join(map(str, self.hand)))



