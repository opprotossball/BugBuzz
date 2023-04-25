import json
import math
import time
from csv import DictReader

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
from BackEnd.GameMechanic.Zobrist import Zobrist
from Util.PlayerEnum import PlayerEnum
import pickle


class Arena(GameMaster):
    def __init__(self, path=None):
        super().__init__()
        self.updt_pos_tbl = False
        self.zobrist = Zobrist()
        self.pos_path = "./Data/PositionTable.txt"
        if path is not None:
            self.pos_path = path

    def duel(self, white_bot, black_bot, max_rounds=None):
        self.new_game(white_bot(self, PlayerEnum.B), black_bot(self, PlayerEnum.C), ui=False, banned_tiles=[(-1, 0)])
        self.win_after_kills = None #[15, 15]
        self.victory_points = None #[30, 30]
        counter = 0
        positions = {}
        while self.winner_side is None:
            self.check_game_over()
            self.get_player(self.get_active_player()).play()
            counter += 1
            if self.updt_pos_tbl and (self.turn == 2 or self.turn == 5):
                pos_hash = self.zobrist.zobrist_hash(self)
                prev_data = positions.get(pos_hash)
                if prev_data is None:
                    positions[pos_hash] = (self.pos_code(), 1, counter)
                else:
                    positions[pos_hash] = (prev_data[0], prev_data[1] + 1, counter)   # TODO przekminic jak z counterem
            if max_rounds is not None and counter > max_rounds:
                return 'D', counter, positions
        if self.winner_side == PlayerEnum.B:
            winner = 'B'
        else:
            winner = 'C'
        return winner, counter, positions

    def series(self, white_bot, black_bot, n, max_rounds=None):
        data = pd.DataFrame(columns=["Winner", "NTurns"])
        pos_data = {}
        for i in range(n):
            winner, nmoves, positions = self.duel(white_bot, black_bot, max_rounds)
            data.loc[len(data.index)] = [winner, nmoves]
            if self.updt_pos_tbl:
                for k, v in positions.items():
                    prev_data = pos_data.get(k)
                    if prev_data is None:
                        pos_data[k] = (v[0], int(winner == 'B'), int(winner == 'C'), int(winner == 'D'))    # TODO przekminic jak z counterem i l. wystapien
                    else:
                        pos_data[k] = (prev_data[0], prev_data[1] + int(winner == 'B'), prev_data[2] + int(winner == 'C'), prev_data[3] + int(winner == 'D'))
        return data, pos_data

    def tournament(self, types_list, n_games, max_rounds, n_threads=8):
        suf = datetime.datetime.now().strftime("%d_%m_%H_%M_%S")
        path = f"./Data/{len(types_list)}BotsTournament{suf}"
        os.mkdir(path)
        pos_res = []
        for white in types_list:
            for black in types_list:
                res = []
                with concurrent.futures.ProcessPoolExecutor() as e:
                    futures = [e.submit(self.series, white, black, math.ceil(n_games / n_threads), max_rounds) for _ in range(n_threads)]
                    for f in concurrent.futures.as_completed(futures):
                        res.append(f.result()[0])
                        if self.updt_pos_tbl:
                            pos_res.append(f.result()[1])
                data = pd.concat(res, ignore_index=True)
                name = white.__name__ + "_" + black.__name__
                data.to_csv(path + "/" + name + ".csv")
                print(name + " series finished")
        self.update_position_table(pos_res)

    def update_position_table(self, new_data):
        if not os.path.exists(self.pos_path):
            data = {}
        else:
            with open(self.pos_path, "rb") as f:
                data = pickle.load(f)

        for d in new_data:
            for k, v in d.items():
                prev_data = data.get(k)
                if prev_data is None:
                    data[k] = (v[0], v[1], v[2], v[3])
                else:
                    data[k] = (v[0], prev_data[1] + v[1], prev_data[2] + v[2], prev_data[3] + v[3])

        with open(self.pos_path, "wb") as f:
            pickle.dump(data, f)

    # def dict_from_pos_file(self):
    #     dict = {}
    #     with open(self.pos_path, "r") as f:
    #         line = f.readline()
    #         while line:
    #             data = line.split(',')
    #             dict[data[0]] = (data[1], data[2], data[3], data[4])
    #             line = f.readline()
    #     return dict


def check():
    with open("./Data/PositionTable.txt", "rb") as f:
        data = pickle.load(f)
        print(len(data))
        # n = 0
        # for k, v in data.items():
        #     if v[1] + v[2] + v[3] > 1:
        #         n += 1
        lst = list(data.items())
        lst.sort(key=lambda x: x[1][1] + x[1][2] + x[1][3])
        print(*lst, sep='\n')
        exit(0)
        print(n)
    #print(data)
    exit()


if __name__ == "__main__":
    check()
    exit(0)
    start = time.time()
    a = Arena(path="./Data/PositionTable.txt")
    a.updt_pos_tbl = True
    a.tournament([BasicAprox], 5000, 600, 8)
    duration = time.time() - start
    print("Time elapsed: ", duration)
    exit()


