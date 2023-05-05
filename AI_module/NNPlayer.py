from BackEnd.GameMechanic.Player import Player
from Util.PlayerEnum import PlayerEnum
from Util.Information import directionOptions, ActionType


class NNPlayer(Player):

    def __init__(self, gm, side):
        super().__init__(gm, side)

    def perform_action(self, action_type, par1, par2):  # returns if move is valid and performs it
        if action_type == ActionType.MOVE:  # MOVE phase
            tile = self.gm.board.iterList[par1]
            bug = tile.bug
            if self.gm.turn == 1 + 3 * (self.side == PlayerEnum.C) and bug is not None and bug.side == self.side:
                return self.perform_move(bug.army, par2, update_armies=True)

        elif action_type == ActionType.KILL:  # COMBAT phase
            tile = self.gm.board.iterList[par1]
            bug = tile.bug
            if self.gm.turn == 0 + 3 * (self.side == PlayerEnum.C) and bug is not None:
                return self.kill_bug(bug)

        elif action_type == ActionType.HATCH:  # HATCH phase
            if self.gm.turn == 2 + 3 * (self.side == PlayerEnum.C):
                return self.perform_hatch(par2, self.gm.board.get_hatchery(self.side)[par1], update_armies=True)

        elif action_type == ActionType.PASS:  # PASS
            self.end_phase()
            return True

    # def perform_action(self, action): # returns if move is valid and performs it
    #     tile = self.gm.board.get_field(action[1], action[2])
    #     if tile is None:
    #         return False
    #     bug = tile.bug
    #
    #     if action[0] < 6:  # MOVE phase
    #         if self.gm.turn == 1 + 3 * (self.side == PlayerEnum.C) and bug is not None and bug.side == self.side:
    #             return self.perform_move(bug.army, directionOptions[action[0]], update_armies=True)
    #
    #     elif action[0] == 6:  # COMBAT phase
    #         if self.gm.turn == 0 + 3 * (self.side == PlayerEnum.C) and bug is not None:
    #             return self.kill_bug(bug)
    #
    #     elif action[0] < 11:
    #         if self.gm.turn == 2 + 3 * (self.side == PlayerEnum.C):  # HATCH phase
    #             return self.perform_hatch(bug_types[action[0] - 7], tile, update_armies=True)
    #
    #     elif action[0] == 11:  # PASS
    #         self.end_phase()
    #         return True

    def set_state(self, state):
        self.state = state
