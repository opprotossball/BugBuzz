from FrontEnd.Interfejs import Interfejs


class InterfejsGracza(Interfejs):
    def getAttack(self, possible_attacks):
        return self.getInput(possible_attacks)

    def getMove(self, possible_moves):
        return self.getInput(possible_moves)

    def getHatch(self, possible_hatch):
        return self.getInput(possible_hatch)

    def getInput(self, possible):
        choice = -1
        while 0 > choice or choice >= len(possible):
            chosen = input("\tMożliwe ruchy:" + str(possible) + " ")
            if chosen == '':
                choice = 0
            else:
                choice = int(chosen)
        return possible[choice]