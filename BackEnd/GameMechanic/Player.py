from abc import ABC, abstractmethod
from enum import Enum

from BackEnd.GameObjects.Trader import Trader


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
        self.bugList = []
        self.state = PlayerState.INACTIVE
        self.bugs_available = {
            'M': 3,
            'K': 3,
            'P': 2,
            'Z': 2
        }

    def end_phase(self):
        self.gm.next_phase()

    def perform_move(self, army, direction):
        army.setMoves()
        if army.numberOfMoves < 1:
            return False
        army.performMove(direction)
        self.gm.getArmies(self.side)
        return True

    def perform_hatch(self, bug_type, tile):
        if self.side == "B":
            if not tile.is_white_hatchery:
                return False
        elif self.side == "C":
            if not tile.is_black_hatchery:
                return False

        if tile.bug is not None:
            return False

        trader = Trader()
        bug, price = trader.buyBug(bug_type, self)
        if bug is None:
            return False

        self.resources -= price
        self.bugs_available[bug.short_name] -= 1
        self.bugList.append(bug)
        bug.moveBugTo(tile)
        self.gm.getArmies(self.side)
        return True

    def perform_attack(self, opponent_army):
        pass

    @abstractmethod
    def set_state(self, state):
        pass


