from AI_module.AproxBot import AproxBot
from AI_module.RewardMap import rewardMap


class Territorial(AproxBot):
    def __init__(self, gm, side):
        super().__init__(gm, side)

    def get_score(self):
        score = 0
        for bug in self.bugList:
            score += self.weights['territory'] * rewardMap.get_reward(bug.field)
        return score
