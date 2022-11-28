from BackEnd.GameMechanic.GameMechanic import GameMechanic
from BackEnd.GameMechanic.Player import PlayerState
from BackEnd.GameObjects.Plansza import Plansza
from BackEnd.GameObjects.Robal import Konik
from Util import Information


class GameMaster(GameMechanic):
    def __init__(self):
        super().__init__()
        self.turn = -1
        self.ui = None
        self.display = None

        self.winner_side = None

    def new_game(self, player_white, player_black):
        self.set_board(Plansza(Information.board_size))
        self.set_player(player_white)
        self.set_player(player_black)
        self.next_phase()

        while True:
            self.updateWindow()
            if self.game_is_over():
                print("Player " + self.winner_side + " has won!")
                return

    def next_phase(self):
        self.turn += 1
        if self.turn == 6:
            self.turn = 0
        if self.turn == 0:
            self.get_armies("C")
            self.BlackPlayer.set_state(PlayerState.INACTIVE)
            self.WhitePlayer.set_state(PlayerState.COMBAT)
        elif self.turn == 1:
            self.get_armies("C")
            self.resetMove("B")
            self.WhitePlayer.set_state(PlayerState.MOVE)
        elif self.turn == 2:
            self.WhitePlayer.resources = self.get_resources_for_side("B")
            self.WhitePlayer.set_state(PlayerState.HATCH)
        elif self.turn == 3:
            self.get_armies("B")
            self.WhitePlayer.set_state(PlayerState.INACTIVE)
            self.BlackPlayer.set_state(PlayerState.COMBAT)
        elif self.turn == 4:
            self.get_armies("B")
            self.resetMove("C")
            self.BlackPlayer.set_state(PlayerState.MOVE)
        elif self.turn == 5:
            self.BlackPlayer.resources = self.get_resources_for_side("C")
            self.BlackPlayer.set_state(PlayerState.HATCH)

    def game_is_over(self):
        bug = self.board.resources[0].bug
        if bug is not None:
            side = bug.side
        else:
            return False

        for pole in self.board.resources:
            if pole.bug is None or pole.bug.side != side:
                return False

        self.winner_side = side
        return True
