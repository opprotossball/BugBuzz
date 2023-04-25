import math
import os
import numpy as np
import Util.Information as Info
import random


class Zobrist:

    def __init__(self):
        self.path = "./ZobristNums.txt"
        self.max_coord = 2 * Info.board_size + 1
        self.zobrist_nums = None  # color, type, x, y
        self.max_val = math.pow(2, 64) - 1
        self.phase = None
        random.seed(21372137)
        self.init()

    def init(self):
        if not os.path.exists(self.path):
            self.generate_zobrist_nums()
            return
        with open(self.path, "r") as f:
            nums = f.read().split("\n")
        self.zobrist_nums = np.ndarray(shape=(2, 4, self.max_coord, self.max_coord), dtype=np.ulonglong)
        self.phase = np.zeros(6, dtype=np.ulonglong)
        for n in range(self.phase.size):
            self.phase[n] = int(nums[n])
            n += 1
        for i in range(self.zobrist_nums.shape[0]):
            for j in range(self.zobrist_nums.shape[1]):
                for k in range(self.zobrist_nums.shape[2]):
                    for l in range(self.zobrist_nums.shape[3]):
                        self.zobrist_nums[i, j, k, l] = int(nums[n])
                        n += 1

    def generate_zobrist_nums(self):
        with open(self.path, "w") as f:
            self.phase = np.random.randint(self.max_val, size=6, dtype=np.ulonglong)
            self.zobrist_nums = np.random.randint(self.max_val, size=(2, 4, self.max_coord, self.max_coord), dtype=np.ulonglong)
            to_write = ""
            for v in self.phase:
                to_write = to_write + str(v) + "\n"
            for v in np.nditer(self.zobrist_nums):
                to_write = to_write + str(v) + "\n"
            f.write(to_write)

    def zobrist_hash(self, gm):
        h = self.phase[gm.turn]
        for bug in gm.WhitePlayer.bugList:
            h ^= self.zobrist_nums[0, int(bug.short_name), bug.field.x + 4, bug.field.y + 4]
        for bug in gm.BlackPlayer.bugList:
            h ^= self.zobrist_nums[1, int(bug.short_name), bug.field.x + 4, bug.field.y + 4]
        return h
