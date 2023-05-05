from abc import ABC
from typing import Tuple, Optional, Union, List

import gym
import numpy as np
from gym import spaces


from AI_module.NNPlayer import NNPlayer
from BackEnd.GameMechanic.BasicPlayer import BasicPlayer
from BackEnd.GameMechanic.GameMaster import GameMaster
from Util import Information
from Util.Information import board_array_size, ActionType
from Util.Information import board_size
from BackEnd.GameObjects.Robal import RobalEnum, Mrowka
from Util.PlayerEnum import PlayerEnum
from ActionCodeDict import action_list


class GameEnv(gym.Env):
    def __init__(self, render_mode=None):
        self.observation_space = spaces.Box(-25, 25, shape=((board_array_size + 1) * board_array_size, 1), dtype=int)
        self.action_space = spaces.Discrete(len(action_list))
        self.state = {}
        self.gm = GameMaster()
        self.game = None
        self.done = False
        self.reset()
        self.steps_to_do = 1000
        self.steps_done = 0

    def reset(self):
        self.steps_done = 0
        self.done = False
        self.game = self.gm.new_game(NNPlayer(self.gm, PlayerEnum.B), NNPlayer(self.gm, PlayerEnum.C), ui=False)
        return self._observe()

    def render(self, mode="human"):
        pass

    def step(self, action):
        a_type, par1, par2 = action_list[action]
        #print(a_type, par1, par2, sep=" ")
        valid = self.gm.get_active_player().perform_action(a_type, par1, par2)
        if a_type == ActionType.PASS:
            reward = 0
        elif valid:
            reward = 1
        else:
            reward = -1
        done = self.gm.winner_side is not None
        if done:
            reward = 1000
        self.steps_done += 1
        if self.steps_done >= self.steps_to_do:
            done = True
        return self._observe(), reward, done, {}

    def _observe(self):
        # obs = {
        #     "phase": self.gm.turn,
        #     "resources": self.gm.get_active_player().resources,
        #     "board": np.ndarray(shape=(board_array_size, board_array_size), dtype=int)
        # }
        obs = np.zeros(shape=(board_array_size+1, board_array_size), dtype=int)
        for bug in self.gm.WhitePlayer.bugList:
            obs[bug.field.x, bug.field.y] = self.encode_bug(bug)
        for bug in self.gm.BlackPlayer.bugList:
            obs[bug.field.x, bug.field.y] = self.encode_bug(bug)
        obs[-1, 0] = self.gm.turn
        obs[-1, 0] = self.gm.get_active_player().resources
        obs = obs.flatten()
        return obs

    @staticmethod
    def encode_bug(bug):
        bug_code = (int(bug.short_name) + 1) * 5
        bug_code += bug.move
        if bug.side == PlayerEnum.C:
            bug_code *= -1
        return bug_code

    @staticmethod
    def decode_bug(bug_code):
        side = PlayerEnum.B
        if bug_code < 0:
            side = PlayerEnum.C
            bug_code *= -1
        move = bug_code % 5
        bug_type = RobalEnum(bug_code // 5 - 1)
        bug = Information.bug_classes[bug_type](side)
        bug.set_move(move)
        return bug


if __name__ == "__main__":
    e = GameEnv()

    print(e.action_space.sample())
