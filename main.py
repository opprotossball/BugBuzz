from FrontEnd.GameMaster import GameMaster
from FrontEnd.InterfejsGracza import InterfejsGracza

if __name__ == "__main__":
    gm = GameMaster()
    #gm.setDisplay()
    gm.newGame(InterfejsGracza(gm, "B", lambda: gm.updateWindow()), InterfejsGracza(gm, "C", lambda: gm.updateWindow()))
    while True:
        gm.updateWindow()
        gm.nextMove()
