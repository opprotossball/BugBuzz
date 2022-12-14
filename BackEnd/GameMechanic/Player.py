import math
from abc import ABC, abstractmethod
from enum import Enum

from BackEnd.GameObjects.Robal import RobalEnum
from BackEnd.GameObjects.Trader import Trader
from Util.PlayerEnum import PlayerEnum


class PlayerState(Enum):
    INACTIVE = 0
    COMBAT = 1
    MOVE = 2
    HATCH = 3


class Player(ABC):

    def __init__(self, gm, side):
        self.gm = gm
        self.side = side
        self.resources = 0
        self.kills = 0
        self.attacked_bugs = []
        self.bugList = []
        self.state = PlayerState.INACTIVE
        self.bugs_available = {
            RobalEnum.K: 3,
            RobalEnum.M: 3,
            RobalEnum.P: 2,
            RobalEnum.Z: 2
        }

    def end_phase(self):
        self.gm.next_phase()

    def perform_move(self, army, direction, update_armies=False):
        self.gm.set_moves(army)
        if army.numberOfMoves < 1:
            return False
        self.gm.perform_move(army, direction)
        if update_armies:
            armies = self.gm.get_armies(self.side)
            for a in armies:
                self.gm.set_moves(a)
        return True

    def perform_hatch(self, bug_type, tile, update_armies=False):
        if self.side == PlayerEnum.B:
            if not tile.is_white_hatchery:
                return False
        elif self.side == PlayerEnum.C:
            if not tile.is_black_hatchery:
                return False

        if tile.bug is not None:
            return False

        trader = Trader()
        bug, price = trader.buy_bug(bug_type, self)
        if bug is None:
            return False

        self.resources -= price
        self.bugs_available[bug.short_name] -= 1
        self.bugList.append(bug)
        bug.move_bug_to(tile)
        if update_armies:
            self.gm.get_armies(self.side)
        return True

    def perform_attack(self, opponent_army):
        self.kills = 0
        if opponent_army.was_attacked:
            return False, 0, None
        attack_power, attacked_bugs = self.gm.get_attack_power_and_bugs_attacked(opponent_army)
        toughness = self.gm.get_toughness_array(opponent_army)
        damage = 0
        rolls = self.gm.roll_dice(attack_power)
        for result in rolls:
            if result not in toughness:
                damage += 1
        kills = math.floor(damage / 2)
        attacked = attack_power > 0
        if attacked:
            opponent_army.was_attacked = True
            self.attacked_bugs = attacked_bugs
            self.kills = kills
        return attacked, kills, rolls

    def kill_bug(self, bug):
        if self.kills > 0 and bug in self.attacked_bugs:
            if self.side == PlayerEnum.B:
                other_player = self.gm.BlackPlayer
            else:
                other_player = self.gm.WhitePlayer
            other_player.bugList.remove(bug)
            other_player.bugs_available[bug.short_name] += 1
            bug.army.bugList.remove(bug)
            self.attacked_bugs.remove(bug)
            bug.field.reset_bug()
            self.kills -= 1
            return True
        return False

    @abstractmethod
    def set_state(self, state):
        pass
