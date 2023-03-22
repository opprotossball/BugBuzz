from AI_module.AproxBotDefaultWeights import default_weights
from AI_module.RewardMap import rewardMap
from BackEnd.GameMechanic.Player import Player, PlayerState
from BackEnd.GameMechanic.PositionGenerator import PositionGenerator
from BackEnd.GameObjects.Trader import Trader
from AI_module.AproxBot import AproxBot


class Swarmer(AproxBot):
    def __init__(self, gm, side):
        super().__init__(gm, side)
        self.generator = PositionGenerator()
        self.trader = Trader()
        self.weights = default_weights

    def set_state(self, state):
        self.state = state

    def play(self):
        if self.state == PlayerState.INACTIVE:
            return
        elif self.state == PlayerState.COMBAT:
            self.hatch()
        elif self.state == PlayerState.MOVE:
            self.perform_moves()
        elif self.state == PlayerState.HATCH:
            self.attack_and_kill_randomly()
        self.end_phase()

    def get_score(self):
        score = 0
        for bug in self.bugList:
            score += self.weights['territory'] * rewardMap.get_reward(bug.field)
        score += 5 * len(self.gm.get_armies(self.side))
        return score

    def perform_moves(self):
        armies_to_move = self.gm.get_armies(self.side)
        count = 0
        while armies_to_move and count < 30:
            count += 1
            best = self.get_best_move(armies_to_move)
            if best is None:
                return
            self.perform_move(best[1].bug.army, best[2])
            armies_to_move = [army for army in self.gm.get_armies(self.side) if army.numberOfMoves > 0]

