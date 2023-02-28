from BackEnd.GameMechanic.Player import Player
import copy


class GeneratorPlayer(Player):

    def __init__(self, gm, side):
        super().__init__(gm, side)

    def set_state(self, state):
        pass

    def clone_for_hatch(self):
        new = GeneratorPlayer(self.gm, self.side)
        new.bugs_available = copy.deepcopy(self.bugs_available)
        new.resources = self.resources
        return new

    def clone_for_move(self):
        new = GeneratorPlayer(self.gm, self.side)
        for bug in self.bugList:
            new.bugList.append(bug.clone_with_field())
        return new
