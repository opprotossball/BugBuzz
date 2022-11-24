from BackEnd.GameMechanic.Player import Player
import copy


class GeneratorPlayer(Player):

    def __init__(self, gm, side):
        super().__init__(gm, side)

    def set_state(self, state):
        pass

    def clone(self):
        new = GeneratorPlayer(self.gm, self.side)
        new.bugs_available = copy.deepcopy(self.bugs_available)
        # new.bugList = copy.deepcopy(self.bugList) # niepotrzebne na razie
        new.resources = self.resources
        return new
