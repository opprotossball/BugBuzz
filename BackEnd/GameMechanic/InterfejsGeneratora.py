from BackEnd.GameMechanic.Interfejs import Interfejs


class InterfejsGeneratora(Interfejs):
    def __init__(self, PG, side, update):
        super().__init__(PG, side, update)

    def getMove(self, possible_moves):
        pass

    def getAttack(self, possible_attacks):
        pass

    def getHatch(self, possible_hatch):
        pass