from random import Random
from itertools import count

class Player:
    amount_of_me = 0
    def __init__(self, name=None):
        if not name:
            self.__class__.amount_of_me += 1
            self.name = "{}{}".format(
                self.__class__.__name__,
                self.__class__.amount_of_me)
        else:
            self.name = name
        self.hand = list(range(2,14))
        self.wins = []

class DummiePlayer(Player):
    def __init__(self, *args, rngchoose=None, rngtie=None, **kwargs):
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
            if self.wins:
                print("Here is your wins pile (you cannot play now):")
                print(" " * 3, ', '.join(map(str, self.wins)))
                print()
            print("Here is your hand:")
            print(" " * 3, ', '.join(map(str, self.hand)))
            print()
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
        h = self.hand[:]
        idxs = []
        print()
        print("There was a tie between you and {} other player{}.".format(
                len(players), "s" if players != 1 else ""
            )
        )
        for prompt in ("Choose the first card to discard: ",
                       "Choose the second card to discard: ",
                       "Choose the third card to discard: ",
                       "Choose your play: "):
            print()
            print("Here is your hand:")
            print(" " * 3, ', '.join(
                ("\x1B[34m{}\x1B[0m" if th is not None else "\x1B[33m{}\x1B[0m").format(rh)
                for th, rh in zip(h, self.hand))
            )
            print()
            while True:
                try:
                    choice = int(input(prompt))
                    idx = h.index(choice)
                    break
                except ValueError:
                    print("That's not a valid choice, dummie!")
            h[idx] = None
            idxs.append(idx)
        return idxs[:-1], idxs[-1]

class InvalidMoveError(Exception):
    pass

def play_game(players, logger=print):
    carry_pot = []
    for rnd in count(0):
        players_in_round = [p for p in players if p.hand]
        logger("Start of Round {}. Remaining players: {}.".format(
            rnd, ', '.join(p.name for p in players_in_round)
        ))
        if len(players_in_round) < 2:
            logger("Less than two players remain. End of game.")
            break

        # Ask each player for their card of choice
        choices = []
        for p in players_in_round:
            idx = p.chooseone()
            if idx not in range(len(p.hand)):
                raise InvalidMoveError
            logger("{} selects the {} at index {}.".format(
                p.name, p.hand[idx], idx
            ))
            choices.append((p, idx))

        # Next, remove the cards from each hand and build the pot
        # Max card will be m
        pot = []
        m = 0
        for p, idx in choices:
            card = p.hand.pop(idx)
            if card > m:
                m = card
            pot.append((p, card))
            carry_pot.append(card)

        winners = [p for p, card in pot if card == m]
        logger("Winners for this round are {}.".format(
            ', '.join(w.name for w in winners)
        ))
        while len(winners) > 1:
            logger("It's a tie!")
            choices = []

            for p in winners:
                if len(p.hand) < 4:
                    logger(
                        "{} does not have enough cards to compete in this tie-breaker... "
                        "they will have to discard their whole hand.".format(p.name)
                    )
                    choices.append((p, list(range(len(p.hand))), None))
                    continue
                discard_idxs, choice_idx = p.choosetie([w for w in winners if w != p])
                if (any(idx not in range(len(p.hand))
                        for idx in discard_idxs + [choice_idx])
                    or len(set(discard_idxs + [choice_idx])) != 4):
                    raise InvalidMoveError
                logger("{} discards indexes {} and selects the {} at index {}.".format(
                    p.name, discard_idxs, p.hand[choice_idx], choice_idx
                ))
                choices.append((p, discard_idxs, choice_idx))

            pot = []
            m = 0
            for p, discard_idxs, choice_idx in choices:
                idxs = discard_idxs if choice_idx is None else discard_idxs + [choice_idx]
                for idx in sorted(idxs, reverse=True):
                    card = p.hand.pop(idx)
                    if idx == choice_idx:
                        if card > m:
                            m = card
                        pot.append((p, card))
                    carry_pot.append(card)
            winners = [p for p, card in pot if card == m]
            logger("Winners for the tie-breaker are {}.".format(
                ', '.join(w.name for w in winners)
            ))

        if len(winners) == 1:
            logger("{} wins: {}.".format(
                winners[0].name,
                ', '.join(map(str, carry_pot))
            ))
            winners[0].wins += carry_pot
            carry_pot = []
        else:
            logger("Nobody wins! The GM mocks your inability to break ties!")
            logger("Carrying to the next round's pot: {}".format(', '.join(map(str, carry_pot))))
        for p in players_in_round:
            if len(p.hand) == 0:
                logger("{} is out of cards in their hand...".format(p.name))
                if len(p.wins) == 0:
                    logger("{} is out of cards in their wins pile. That sucks!".format(p.name))
                else:
                    logger("{} gathers their wins pile with {} cards.".format(p.name, len(p.wins)))
                    p.hand = p.wins
                    p.wins = []
    if len(players_in_round) == 1:
        p = players_in_round[0]
        logger("Congrats to {}, the winner of the game!".format(p.name))
        return rnd, p
    logger("Looks like you screwed this one up... everyone is out and nobody won!")
    return rnd, None

