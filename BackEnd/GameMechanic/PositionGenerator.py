from BackEnd.GameMechanic.GameMechanic import GameMechanic
from BackEnd.GameMechanic.InterfejsGeneratora import InterfejsGeneratora
from BackEnd.GameObjects.Plansza import Plansza
from Util import Information


class PositionGenerator(GameMechanic):
    def __init__(self):
        super().__init__()
        self.WhitePlayer = InterfejsGeneratora(self, "B", None)
        self.BlackPlayer = InterfejsGeneratora(self, "C", None)
        self.turn_of = "B"

    def getPosititions(self, board):
        return []

    def get_new_board(self):
        self.operating_board = Plansza(Information.board_size)

    def set_board(self, board):
        self.operating_board = board.clone()