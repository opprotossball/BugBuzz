from FrontEnd.GameMaster import GameMaster
from FrontEnd.InterfejsGracza import InterfejsGracza
from FrontEnd.UI import UI

if __name__ == '__main__':
    GM = GameMaster()
    player1 = InterfejsGracza(GM, "B")
    player2 = InterfejsGracza(GM, "C")

    screenWidth = 1000
    screenHeight = 800

    ui = UI(screenWidth, screenHeight)

    GM.setUI(ui)
    GM.newGame(player1, player2)

