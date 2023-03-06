import pandas as pd
import concurrent.futures
import time
import datetime

from AI_module.RandomBot import RandomBot
from BackEnd.GameMechanic.GameMaster import GameMaster
from Util.PlayerEnum import PlayerEnum


class Arena(GameMaster):
    def __init__(self):
        super().__init__()

    def duel(self):
        self.new_game(RandomBot(self, PlayerEnum.B), RandomBot(self, PlayerEnum.C), ui=False)
        counter = 0
        while self.winner_side is None:
            self.get_player(self.get_active_player()).play()
            counter += 1
        if self.winner_side == PlayerEnum.B:
            winner = 'B'
        else:
            winner = 'C'
        return winner, counter

    def tournament(self, n):
        data = pd.DataFrame(columns=["Winner", "NTurns"])
        for i in range(n):
            winner, nmoves = self.duel()
            data.loc[len(data.index)] = [winner, nmoves]
        return data


def concurrent_tournament(n):
    arena = Arena()
    return arena.tournament(n)


if __name__ == "__main__":
    results = []
    start = time.time
    with concurrent.futures.ProcessPoolExecutor() as e:
        fs = [e.submit(concurrent_tournament, 1250) for _ in range(8)]
        for f in concurrent.futures.as_completed(fs):
            results.append(f.result())
    data = pd.concat(results, ignore_index=True)
    suf = datetime.datetime.now().strftime("%m_%d_%H_%M_%S")
    data.to_csv(f'Data/randomBotTournament{suf}.csv')
