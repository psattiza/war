from concurrent.futures import ProcessPoolExecutor
from war import SimpleMindedPlayer, DummiePlayer, play_game
from collections import defaultdict

from functools import update_wrapper
from math import sqrt

DUMMIES = 100
THIRTYGAMESPERDUMMIE = 301

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

def bulk_executor(calls):
    return [f(*args, **kwargs) for f, args, kwargs in calls]

def bulk_dummie_executor(d):
    return bulk_executor([(play_game, [[SimpleMindedPlayer()]+ [DummiePlayer() for i in range(d)]], dict(logger=nothing, kill_at_uniq=True)) for _ in range(30)])

wf = open("wins.dat", "w")
rf = open("rounds.dat", "w")
e = ProcessPoolExecutor()
futures = []

wins = defaultdict(lambda: defaultdict(int))
rounds = defaultdict(statlogger)

for d in range(1, DUMMIES + 1):
    for _ in range(THIRTYGAMESPERDUMMIE):
        futures.append((
                d,
                e.submit(bulk_dummie_executor, d)
        ))

for d, f in futures:
    results = f.result()
    for r, w in results:
        wins[d][type(w)] += 1
        if isinstance(w, SimpleMindedPlayer):
            rounds[d](r)

for d in range(1, DUMMIES + 1):
    print(d, wins[d][SimpleMindedPlayer] / sum(wins[d].values()), file=wf)
    print(d, rounds[d].mean, rounds[d].stdev, file=rf)
