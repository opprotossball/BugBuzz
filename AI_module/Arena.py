import math
import time

import pandas as pd
import concurrent.futures
import datetime
import os

from AI_module.DeathBall import DeathBall
from AI_module.Aggressor import Aggressor
from AI_module.BasicAprox import BasicAprox
from AI_module.Economic import Economic
from AI_module.Pacifist import Pacifist
from AI_module.RandomBot import RandomBot
from AI_module.Swarmer import Swarmer
from AI_module.Territorial import Territorial
from BackEnd.GameMechanic.GameMaster import GameMaster
from Util.PlayerEnum import PlayerEnum


class Arena(GameMaster):
    def __init__(self):
        super().__init__()

    def duel(self, white_bot, black_bot, max_rounds=None):
        self.new_game(white_bot(self, PlayerEnum.B), black_bot(self, PlayerEnum.C), ui=False)
        self.win_after_kills = None #[15, 15]
        self.victory_points = None #[30, 30]
        counter = 0
        while self.winner_side is None:
            self.check_game_over()
            self.get_player(self.get_active_player()).play()
            counter += 1
            if max_rounds is not None and counter > max_rounds:
                return 'D', counter
        if self.winner_side == PlayerEnum.B:
            winner = 'B'
        else:
            winner = 'C'
        return winner, counter

    def series(self, white_bot, black_bot, n, max_rounds=None):
        data = pd.DataFrame(columns=["Winner", "NTurns"])
        for i in range(n):
            winner, nmoves = self.duel(white_bot, black_bot, max_rounds)
            data.loc[len(data.index)] = [winner, nmoves]
        return data

    def tournament(self, types_list, n_games, max_rounds, n_threads=8):
        suf = datetime.datetime.now().strftime("%d_%m_%H_%M_%S")
        path = f"./Data/{len(types_list)}BotsTournament{suf}"
        os.mkdir(path)
        for white in types_list:
            for black in types_list:
                res = []
                with concurrent.futures.ProcessPoolExecutor() as e:
                    futures = [e.submit(self.series, white, black, math.ceil(n_games / n_threads), max_rounds) for _ in range(n_threads)]
                    for f in concurrent.futures.as_completed(futures):
                        res.append(f.result())
                data = pd.concat(res, ignore_index=True)
                name = white.__name__ + "_" + black.__name__
                data.to_csv(path + "/" + name + ".csv")
                print(name + " series finished")


if __name__ == "__main__":
    start = time.time()
    a = Arena()
    a.tournament([BasicAprox, Economic, Aggressor, Pacifist, DeathBall, Territorial], 80, 600, 8)
    duration = time.time() - start
    print("Time elapsed: ", duration)
