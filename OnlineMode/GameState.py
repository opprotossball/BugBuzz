from BackEnd.GameObjects.Plansza import Plansza
from Util import Information
from Util.PlayerEnum import PlayerEnum


class GameState:

    def __init__(self, board=None, turn=None, winner=None, active=None):
        self.winner_side = winner
        self.turn = turn
        self.board = board
        self.ready = True
        self.change_active = False
        self.valid = False

    def set_starting_position(self):
        self.board = Plansza(Information.board_size)
        self.turn = 0

