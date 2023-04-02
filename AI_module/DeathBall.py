from AI_module.AproxBot import AproxBot
from AI_module.RewardMap import rewardMap


class DeathBall(AproxBot):
    def __init__(self, gm, side):
        super().__init__(gm, side)

    def get_score(self):
        score = 0
        for bug in self.bugList:
            score += self.weights['territory'] * rewardMap.get_reward(bug.field)
        score -= 3 * len(self.gm.get_armies(self.side))
        score += self.weights['attack'] * self.get_avg_attack()
        score += self.weights['toughness'] * self.get_avg_toughness()
        return score
