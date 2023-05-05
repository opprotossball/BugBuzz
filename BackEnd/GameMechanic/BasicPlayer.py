from BackEnd.GameMechanic.Player import Player


class BasicPlayer(Player):

    def __init__(self, gm, side):
        super().__init__(gm, side)

    def set_state(self, state):
        self.state = state
