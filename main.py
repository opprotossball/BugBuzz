from BackEnd.GameMechanic.GameMaster import GameMaster
from BackEnd.GameMechanic.HumanPlayer import HumanPlayer
from Util.PlayerEnum import PlayerEnum

if __name__ == "__main__":
    gm = GameMaster()
    gm.set_new_ui_and_display()
    gm.new_game(HumanPlayer(gm, PlayerEnum.B), HumanPlayer(gm, PlayerEnum.C))
