from AI_module.AproxBot import AproxBot
from AI_module.RewardMap import rewardMap
from BackEnd.GameObjects.Robal import RobalEnum


class Aggressor(AproxBot):
    def __init__(self, gm, side):
        super().__init__(gm, side)

    def get_melees(self):
        melees = 0
        for bug in self.bugList:
            neighs = self.gm.board.get_field_neighs(bug.field)
            for neighbour in neighs:
                if self.gm.has_opponents_neighbour(bug.side, neighbour):
                    melees += 1
        return melees

    def get_score(self):
        score = 0
        for bug in self.bugList:
            score += self.weights['territory'] * rewardMap.get_reward(bug.field)
        score += 2 * self.get_melees()
        score += self.weights['attack'] * self.get_avg_attack()
        return score

    def hatch(self, prefered=None):
        super().hatch(prefered=[RobalEnum.Z, RobalEnum.P, RobalEnum.M, RobalEnum.K])
        