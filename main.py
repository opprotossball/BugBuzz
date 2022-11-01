from FrontEnd.GameMaster import GameMaster
from FrontEnd.InterfejsGracza import InterfejsGracza

if __name__ == "__main__":
    gm = GameMaster()
    gm.newGame(InterfejsGracza(gm, "B", None), InterfejsGracza(gm, "C", None))
    while True:
        gm.updateWindow()
