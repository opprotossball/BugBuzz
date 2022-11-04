from BackEnd.GameMechanic.Player import Player


class HumanPlayer(Player):

    def __init__(self, gm, side):
        super().__init__(gm, side)

    def set_state(self, state):
        self.state = state
        self.gm.ui.setMode(state, self.side)  #ui przez gm-a wywołuje metody z Plater.py z odpowiedniej fazy

        #ewentalnie można tu po prostu wkleić ui bo ta klasa praktycznie nic nie robi