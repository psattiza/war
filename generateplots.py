from concurrent.futures import ProcessPoolExecutor
from war import SimpleMindedPlayer, DummiePlayer, play_game
from collections import defaultdict

from functools import update_wrapper
from math import sqrt

class Welford:
    def __init__(self, f):
        self.f = f
        update_wrapper(self, f)
        self.mean = 0
        self.v = 0
        self.trials = 0

    def __call__(self, *args, **kwargs):
        r = self.f(*args, **kwargs)
        self.trials += 1
        d = r - self.mean
        self.v += d**2 * (self.trials - 1)/self.trials
        self.mean += d/self.trials
        return r

    @property
    def stdev(self):
        return sqrt(self.v/self.trials) if self.trials else 0

def statlogger():
    @Welford
    def i(x):
        return x
    return i

def nothing(a):
    return a

wf = open("wins.dat", "w")
rf = open("rounds.dat", "w")
e = ProcessPoolExecutor()
futures = []

wins = defaultdict(lambda: defaultdict(int))
rounds = defaultdict(statlogger)

for dummies in range(1, 100 + 1):
    for round in range(1000 + 1):
        futures.append((e.submit( play_game, [SimpleMindedPlayer()]+ [DummiePlayer() for i in range(100)], logger=nothing), dummies))

for f, d in futures:
    r, w = f.result()
    wins[d][type(w)] += 1
    if isinstance(w, SimpleMindedPlayer):
        rounds[d](r)

for dummies in range(1, 100 + 1):
    for round in range(1000 + 1):
        print(dummies, wins[dummies][SimpleMinedPlayer] / sum(wins[dummies].values()), file=wf)
        print(dummies, rounds[dummies].mean, rounds[dummies].stdev, file=rf)



print("Done with", dummies)




