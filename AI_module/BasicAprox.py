from AI_module.AproxBot import AproxBot
from AI_module.RewardMap import rewardMap
from BackEnd.GameMechanic.Player import PlayerState
from BackEnd.GameObjects.Robal import RobalEnum


class BasicAprox(AproxBot):
    def __init__(self, gm, side):
        super().__init__(gm, side)

    def get_score(self):
        score = 0
        for bug in self.bugList:
            score += self.weights['territory'] * rewardMap.get_reward(bug.field)
        score += self.weights['attack'] * self.get_avg_attack()
        score += self.weights['toughness'] * self.get_avg_toughness()
        return score

    def n_of_resources(self):
        return self.gm.get_resources_for_side(self.side)
