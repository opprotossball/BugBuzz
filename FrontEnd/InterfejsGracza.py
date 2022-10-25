from BackEnd.Trader import Trader
from FrontEnd.Interfejs import Interfejs


class InterfejsGracza(Interfejs):
    def getAttack(self, possible_attacks):
        choice = ""
        while choice not in possible_attacks:
            choice = input("Możliwe ruchy:" + possible_attacks)

    def getMove(self, possible_moves):
        choice = ""
        while choice not in possible_moves:
            choice = input("Możliwe ruchy:" + possible_moves)

    def getHatch(self, possible_hatch):
        choice = ""
        while choice not in possible_hatch:
            choice = input("Możliwe ruchy:" + possible_hatch)