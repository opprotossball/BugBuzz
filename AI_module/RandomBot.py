import random

from BackEnd.GameMechanic.Player import Player, PlayerState
from BackEnd.GameMechanic.PositionGenerator import PositionGenerator
from BackEnd.GameObjects.Trader import Trader
from Util import Information


class RandomBot(Player):
    def __init__(self, gm, side):
        super().__init__(gm, side)
        self.generator = PositionGenerator()
        self.trader = Trader()

    def set_state(self, state):
        self.state = state

    def play(self):
        if self.state == PlayerState.INACTIVE:
            return
        elif self.state == PlayerState.COMBAT:
            self.attack_each()
        elif self.state == PlayerState.MOVE:
            self.random_moves()
        elif self.state == PlayerState.HATCH:
            self.random_hatch()
        self.end_phase()

    def random_moves(self):
        armies_to_move = self.gm.get_armies(self.side)
        while armies_to_move:
            self.perform_move(random.choice(armies_to_move), random.choice(Information.directionOptions), update_armies=True)
            armies_to_move = [army for army in self.gm.get_armies(self.side) if army.numberOfMoves > 0]

    def attack_each(self):
        for army in self.gm.get_armies(self.get_opponent_side()):
            if self.perform_attack(army) is None:
                return
            while True:
                if not self.attacked_bugs or not self.kill_bug(random.sample(self.attacked_bugs, 1)[0]):
                    break

    def random_hatch(self):
        options = self.trader.get_options(self.resources, self.bugs_available)
        hatchery = self.gm.get_available_space_for_hatch(self.side)
        while options and hatchery:
            self.perform_hatch(random.choice(options), random.choice(hatchery))
            options = self.trader.get_options(self.resources, self.bugs_available)
            hatchery = self.gm.get_available_space_for_hatch(self.side)
