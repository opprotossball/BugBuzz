from FrontEnd.Interfejs import Interfejs


class InterfejsGracza(Interfejs):
    def getAttack(self, possible_attacks):
        if self.GM.UI is not None:
            attack = None
            while attack not in possible_attacks:
                self.GM.UI.setMode("Attack", self.side)
                attack = self.GM.UI.getAttack()
        else:
            attack = self.get_input_from_terminal(possible_attacks)
        return attack

    def getMove(self, possible_moves):
        if self.GM.UI is not None:
            move = None
            while move not in possible_moves:
                self.GM.UI.setMode("Move", self.side)
                move = self.GM.UI.getMove()
        else:
            move = self.get_input_from_terminal(possible_moves)
        return move

    def getHatch(self, possible_hatch):
        if self.GM.UI is not None:
            hatch = None
            while hatch not in possible_hatch:
                self.GM.UI.setMode("Hatch", self.side)
                hatch = self.GM.UI.getHatch()
        else:
            hatch = self.get_input_from_terminal(possible_hatch)
        return hatch

    def get_input_from_terminal(self, possible):
        choice = -1
        while 0 > choice or choice >= len(possible):
            chosen = input("\tMożliwe ruchy:" + str(possible) + " ")
            if chosen == '':
                choice = 0
            else:
                choice = int(chosen)
        return possible[choice]