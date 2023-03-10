import pandas as pd
import concurrent.futures
import time
import datetime

from AI_module import AproxBotDefaultWeights
from AI_module.AproxBot import AproxBot
from AI_module.RandomBot import RandomBot
from BackEnd.GameMechanic.GameMaster import GameMaster
from Util.PlayerEnum import PlayerEnum


class Arena(GameMaster):
    def __init__(self):
        super().__init__()

    def duel(self, max_rounds=None):
        self.new_game(AproxBot(self, PlayerEnum.B, AproxBotDefaultWeights.default_weights), RandomBot(self, PlayerEnum.C), ui=False) # TODO bot types as parameters
        counter = 0
        while self.winner_side is None:
            self.get_player(self.get_active_player()).play()
            counter += 1
            if max_rounds is not None and counter > max_rounds:
                return 'D', counter
        if self.winner_side == PlayerEnum.B:
            winner = 'B'
        else:
            winner = 'C'
        return winner, counter

    def tournament(self, n, max_rounds=None):
        data = pd.DataFrame(columns=["Winner", "NTurns"])
        for i in range(n):
            winner, nmoves = self.duel(max_rounds)
            print(f"Duel {i} finished: {winner} has won in {nmoves} turns")
            data.loc[len(data.index)] = [winner, nmoves]
        return data


def concurrent_tournament(n, max_rounds=None):
    arena = Arena()
    return arena.tournament(n, max_rounds)


if __name__ == "__main__":
    results = []
    start = time.time
    with concurrent.futures.ProcessPoolExecutor() as e:
        fs = [e.submit(concurrent_tournament, 5, 600) for _ in range(8)]
        for f in concurrent.futures.as_completed(fs):
            results.append(f.result())
    data = pd.concat(results, ignore_index=True)
    suf = datetime.datetime.now().strftime("%m_%d_%H_%M_%S")
    data.to_csv(f'Data/WhiteAproxBlackRandom{suf}.csv')
    results = []
    start = time.time
