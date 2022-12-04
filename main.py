from BackEnd.GameMechanic.GameMaster import GameMaster
from BackEnd.GameMechanic.HumanPlayer import HumanPlayer
from BackEnd.GameMechanic.NNPlayer import NNPlayer

if __name__ == "__main__":
    gm = GameMaster()
    gm.setGUI()
    gm.new_game(HumanPlayer(gm, "B"), HumanPlayer(gm, "C"))
