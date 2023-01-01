from BackEnd.GameObjects.Plansza import Plansza
from Util import Information
from Util.PlayerEnum import PlayerEnum


class GameState:

    def __init__(self, board=None, turn=None, winner=None, active=None):
        self.winner_side = winner
        self.turn = turn
        self.board = board
        self.active_player = active
        self.ready = True
        self.change_active = False

    def set_starting_position(self):
        self.board = Plansza(Information.board_size)
        self.turn = 0
        self.active_player = PlayerEnum.B

    def is_active(self, player_side):
        if not self.ready:
            return False
        return self.active_player == player_side

    def set_active(self, player_side):
        self.active_player = player_side

    def set_change_active(self, change):
        self.change_active = change
