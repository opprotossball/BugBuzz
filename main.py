from BackEnd.GameMechanic.GameMaster import GameMaster
from BackEnd.GameMechanic.InterfejsGracza import InterfejsGracza

if __name__ == "__main__":
    gm = GameMaster()
    gm.setGUI()
    gm.newGame(InterfejsGracza(gm, "B", lambda: gm.updateWindow()), InterfejsGracza(gm, "C", lambda: gm.updateWindow()))
    while True:
        gm.updateWindow()
