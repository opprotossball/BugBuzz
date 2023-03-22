import math
import pandas as pd
import concurrent.futures
import datetime
import pstats
import cProfile
import io
import os

from AI_module.BasicAprox import BasicAprox
from AI_module.RandomBot import RandomBot
from AI_module.Swarmer import Swarmer
from BackEnd.GameMechanic.GameMaster import GameMaster
from Util.PlayerEnum import PlayerEnum


class Arena(GameMaster):
    def __init__(self):
        super().__init__()

    def duel(self, white_bot, black_bot, max_rounds=None):
        self.new_game(white_bot(self, PlayerEnum.B), black_bot(self, PlayerEnum.C), ui=False)
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

    def series(self, white_bot, black_bot, n, max_rounds=None):
        data = pd.DataFrame(columns=["Winner", "NTurns"])
        for i in range(n):
            winner, nmoves = self.duel(white_bot, black_bot, max_rounds)
            print(f"Duel {i} finished: {winner} has won in {nmoves} turns")
            data.loc[len(data.index)] = [winner, nmoves]
        return data

    def tournament(self, types_list, n_games, max_rounds, n_threads=8):
        suf = datetime.datetime.now().strftime("%m_%d_%H_%M_%S")
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
                name = white.__name__ + "vs" + black.__name__
                data.to_csv(path + "/" + name + ".csv")


if __name__ == "__main__":
    a = Arena()
    a.tournament([RandomBot, BasicAprox, Swarmer], 100, 600, 8)
    pass
    # pr = cProfile.Profile()
    # pr.enable()
    # profile()
    # pr.disable()
    # with open('Data/CProfileResults.csv', 'w') as f:
    #     f.write(prof_to_csv(pr))
    # exit()
#
# def profile():
#     arena = Arena()
#     data = arena.series(5, 600)
#     data.to_csv('performanceTest.csv')
#
#
# def prof_to_csv(prof: cProfile.Profile):
#     out_stream = io.StringIO()
#     pstats.Stats(prof, stream=out_stream).print_stats()
#     result = out_stream.getvalue()
#     # chop off header lines
#     result = 'ncalls' + result.split('ncalls')[-1]
#     lines = [','.join(line.rstrip().split(None, 5)) for line in result.split('\n')]
#     return '\n'.join(lines)

