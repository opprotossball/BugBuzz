from BackEnd.GameMechanic.GameMaster import GameMaster
from BackEnd.GameMechanic.HumanPlayer import HumanPlayer
from FrontEnd.MenuScene import MenuScene
from Util.PlayerEnum import PlayerEnum

if __name__ == "__main__":
    gm = GameMaster()
    gm.set_display()
    gm.display.set_scene(MenuScene(gm))
    gm.new_game(HumanPlayer(gm, PlayerEnum.B), HumanPlayer(gm, PlayerEnum.C))
