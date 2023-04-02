from AI_module.AproxBotDefaultWeights import default_weights
from AI_module.RewardMap import rewardMap
from BackEnd.GameMechanic.PositionGenerator import PositionGenerator
from BackEnd.GameObjects.Trader import Trader
from AI_module.AproxBot import AproxBot


class Swarmer(AproxBot):
    def __init__(self, gm, side):
        super().__init__(gm, side)
        self.generator = PositionGenerator()
        self.trader = Trader()
        self.weights = default_weights

    def get_score(self):
        score = 0
        for bug in self.bugList:
            score += self.weights['territory'] * rewardMap.get_reward(bug.field)
        score += 5 * len(self.gm.get_armies(self.side))
        score += self.weights['attack'] * self.get_avg_attack()
        score += self.weights['toughness'] * self.get_avg_toughness()
        return score
