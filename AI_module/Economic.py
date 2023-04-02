from AI_module.AproxBot import AproxBot
from AI_module.RewardMap import rewardMap
from BackEnd.GameMechanic.Player import PlayerState
from BackEnd.GameObjects.Robal import RobalEnum


class Economic(AproxBot):

    def __init__(self, gm, side):
        super().__init__(gm, side)

    def play(self):
        if self.state == PlayerState.INACTIVE:
            return
        elif self.state == PlayerState.COMBAT:
            self.attack_and_kill_randomly()
        elif self.state == PlayerState.MOVE:
            self.perform_moves()
        elif self.state == PlayerState.HATCH:
            self.hatch(prefered=[RobalEnum.K, RobalEnum.Z, RobalEnum.P, RobalEnum.M])
        self.end_phase()

    def get_score(self):
        score = 0
        for bug in self.bugList:
            score += self.weights['territory'] * rewardMap.get_reward(bug.field)
        score += 6 * self.gm.get_resources_for_side(self.side)
        score += self.weights['attack'] * self.get_avg_attack()
        score += self.weights['toughness'] * self.get_avg_toughness()
        return score
