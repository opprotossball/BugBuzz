from FrontEnd.Interfejs import Interfejs


class InterfejsGracza(Interfejs):
    def __init__(self, GM, side, updateMethod):
        super().__init__(GM, side, updateMethod)
        self.attack = None
        self.move = None
        self.hatch = None

    def getAttack(self, possible_attacks):
        if self.GM.UI is not None:
            self.attack = None
            while self.attack not in possible_attacks:
                self.GM.UI.setMode("Attack", self.side)
                self.GM.UI.getAttack(lambda attack: self.setAttack(attack))
        else:
            self.attack = self.get_input_from_terminal(possible_attacks)
        return self.attack

    def getMove(self, possible_moves):
        if self.GM.UI is not None:
            self.move = None
            while self.move not in possible_moves:
                self.GM.UI.setMode("Move", self.side)
                self.GM.UI.getMove(lambda move: self.setMove(move))
        else:
            self.move = self.get_input_from_terminal(possible_moves)
        return self.move

    def getHatch(self, possible_hatch):
        if self.GM.UI is not None:
            self.hatch = None
            while self.attack not in possible_hatch:
                self.GM.UI.setMode("Hatch", self.side)
                self.hatch = self.GM.UI.getHatch(lambda hatch: self.setHatch(hatch))
        else:
            self.hatch = self.get_input_from_terminal(possible_hatch)
        return self.hatch

    def setAttack(self, attack):
        self.attack = attack

    def setMove(self, move):
        self.move = move

    def setHatch(self, hatch):
        self.hatch = hatch

    def get_input_from_terminal(self, possible):
        choice = -1
        while 0 > choice or choice >= len(possible):
            chosen = input("\tMożliwe ruchy:" + str(possible) + " ")
            if chosen == '':
                choice = 0
            else:
                choice = int(chosen)
        return possible[choice]