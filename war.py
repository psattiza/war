import heapq
from random import Random
from itertools import count
from copy import deepcopy

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

    def chooseone(self, players):
        return self.rngchoose.randrange(len(self.hand))

    def choosetie(self, players):
        selection = self.rngtie.sample(range(len(self.hand)), 4)
        return selection[:-1], selection[-1]

class SimpleMindedPlayer(Player):
    def chooseone(self, players):
        self.hand.sort()
        max_of_all = max(max(p.hand) for p in players)
        max_of_me = self.hand[-1]
        if max_of_me > max_of_all:
            for i, card in enumerate(self.hand):
                if card > max_of_all:
                    return i
        if max_of_me == max_of_all and len(self.hand) >= 5:
            return len(self.hand) - 1
        return 0

    def choosetie(self, players):
        if not any(p.hand for p in players):
            # we win this one no matter what happens
            return [0, 1, 2], 3
        upper_hand = self.hand[3:]
        max_of_all = max(max(p.hand) for p in players if p.hand)
        max_of_me = self.hand[-1]
        if max_of_me > max_of_all:
            for i, card in enumerate(upper_hand):
                if card > max_of_all:
                    break
            return [0, 1, 2], 3 + i
        if max_of_me == max_of_all and len(upper_hand) >= 5:
            try:
                lookahead_max = max(
                    heapq.nlargest(2, p.hand)[1]
                    for p in players if len(p.hand) > 1)
            except ValueError:
                return [0, 1, 2], len(self.hand) - 1
            my_next_best = heapq.nlargest(2, upper_hand)[1]
            if my_next_best >= lookahead_max:
                return [0, 1, 2], len(self.hand) - 1
        return [0, 1, 2], 3

class GeneralPurposeAdversary(Player):
    def chooseone(self, players):
        self.hand.sort()
        max_of_all = 0
        max_players = []
        for p in players:
            if not p.hand:
                continue
            card = p.hand[p.chooseone([pp for pp in players if pp != p] + [self])]
            if card > max_of_all:
                max_of_all = card
                max_players = [p]
            elif card == max_of_all:
                max_players.append(p)
        max_of_me = self.hand[-1]
        if max_of_me > max_of_all:
            for i, card in enumerate(self.hand):
                if card > max_of_all:
                    return i
        if max_of_me == max_of_all and len(self.hand) >= 5:
            max_players = deepcopy(max_players)
            me = deepcopy(self)
            for p in max_players:
                p.hand.remove(max_of_all)
                if not p.hand:
                    max_players.remove(p)
            me.hand.remove(max_of_all)
            my_discards, my_choice = me.choosetie(max_players)
            max_choice = 0
            for p in max_players:
                if len(p.hand) < 4:
                    continue
                discard_idxs, choice_idx = p.choosetie([pp for pp in max_players if pp != p] + [me])
                if p.hand[choice_idx] > me.hand[my_choice]:
                    return 0
            return len(self.hand) - 1
        return 0

    def choosetie(self, players):
        if not any(p.hand for p in players):
            # we win this one no matter what happens
            return [0, 1, 2], 3
        me = deepcopy(self)
        me.hand = me.hand[3:]
        return [0, 1, 2], me.chooseone(players) + 3

class HumanPlayer(Player):

    def chooseone(self, players):
        self.hand.sort()
        print("==> {} <==".format(self.name))
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
                return idx
            except ValueError:
                print("That's not a valid choice, dummie!")

    def choosetie(self, players):
        print("==> {} <==".format(self.name))
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

def play_game(players, logger=print, kill_at_uniq=False):
    carry_pot = []
    for rnd in count(0):
        players_in_round = [p for p in players if p.hand]
        logger("Start of Round {}. Remaining players: {}.".format(
            rnd, ', '.join(p.name for p in players_in_round)
        ))
        if kill_at_uniq:
            for p in players_in_round:
                if type(p) != type(players_in_round[-1]):
                    break
            else:
                if not players_in_round:
                    return rnd, None
                return rnd, players_in_round[0]
        if len(players_in_round) < 2:
            logger("Less than two players remain. End of game.")
            break

        # Ask each player for their card of choice
        choices = []
        for p in players_in_round:
            idx = p.chooseone([op for op in players_in_round if op != p])
            if idx not in range(len(p.hand)):
                raise InvalidMoveError
            choices.append((p, idx))

        # Next, remove the cards from each hand and build the pot
        # Max card will be m
        pot = []
        m = 0
        for p, idx in choices:
            card = p.hand.pop(idx)
            logger("{} selects the {} at index {}.".format(p.name, card, idx))
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
                    choices.append((p, list(range(len(p.hand))), None))
                    continue
                discard_idxs, choice_idx = p.choosetie([w for w in winners if w != p])
                if (any(idx not in range(len(p.hand))
                        for idx in discard_idxs + [choice_idx])
                    or len(set(discard_idxs + [choice_idx])) != 4):
                    raise InvalidMoveError
                choices.append((p, discard_idxs, choice_idx))

            pot = []
            m = 0
            for p, discard_idxs, choice_idx in choices:
                if choice_idx is None:
                    logger(
                        "{} does not have enough cards to compete in this tie-breaker... "
                        "they will have to discard their whole hand.".format(p.name)
                    )
                    idxs = discard_idxs
                else:
                    logger("{} discards indexes {} and selects the {} at index {}.".format(
                        p.name, discard_idxs, p.hand[choice_idx], choice_idx
                    ))
                    idxs = discard_idxs + [choice_idx]
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

