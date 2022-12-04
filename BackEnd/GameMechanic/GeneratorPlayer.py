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

    # def get_hash_for_move(self):
    #     code = ""
    #     tiles = [[] for _ in range(4)]
    #     for bug in self.bugList:
    #         if bug.short_name == 'K':
    #             i = 0
    #         elif bug.short_name == 'M':
    #             i = 1
    #         elif bug.short_name == 'P':
    #             i = 2
    #         else:
    #             i = 3
    #         tiles[i].append(bug.field.get_key_for())
    #     for type_list in tiles:
    #         type_list.sort()
    #     for type_list in tiles:
    #         for c in type_list:
    #             code += str(c)
    #     return code
