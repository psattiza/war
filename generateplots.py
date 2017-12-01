from concurrent.futures import ProcessPoolExecutor
from war import SimpleMindedPlayer, DummiePlayer, play_game
from collections import defaultdict
from statistics import mean, stdev

def nothing(a):
    return

wf = open("wins.dat", "w")
rf = open("rounds.dat", "w")

for dummies in range(1,100):
    e = ProcessPoolExecutor()
    futures = []
    rounds = []
    wins = defaultdict(int)
    for round in range(100):
        futures.append(e.submit( play_game, [SimpleMindedPlayer()]+ [DummiePlayer() for i in range(100)], logger=nothing))
    for f in futures:
        r, w = f.result()
        wins[type(w).__name__] += 1
        if isinstance(w, SimpleMindedPlayer):
            rounds.append(r)
    print(dummies, wins["SimpleMinedPlayer"] / sum(wins), file=wf)
    print(dummies, mean(rounds), stdev(rounds), file=rf)




