from FrontEnd.Interfejs import Interfejs


class InterfejsGracza(Interfejs):
    def getAttack(self, possible_attacks):
        choice = -1
        while 0 > choice or choice >= len(possible_attacks):
            choice = int(input("Możliwe ruchy:" + possible_attacks))
        return possible_attacks[choice]

    def getMove(self, possible_moves):
        choice = -1
        while 0 > choice or choice >= len(possible_moves):
            choice = int(input("Możliwe ruchy:" + possible_moves))
        return possible_moves[choice]

    def getHatch(self, possible_hatch):
        choice = -1
        while 0 > choice or choice >= len(possible_hatch):
            choice = int(input("Możliwe ruchy:" + str(possible_hatch)))

        return possible_hatch[choice]