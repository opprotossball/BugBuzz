from FrontEnd.GameMaster import GameMaster
from FrontEnd.InterfejsGracza import InterfejsGracza
from FrontEnd.UI import UI
from FrontEnd.UI_thread import UI_thread

if __name__ == '__main__':
    GM = GameMaster()
    ui = UI(GM.plansza)

    player1 = InterfejsGracza(GM, "B", lambda : ui.updateWindow())
    player2 = InterfejsGracza(GM, "C", lambda : ui.updateWindow())

    screenWidth = 1000
    screenHeight = 800


    GM.setUI(ui)
    GM.newGame(player1, player2)

    while ui.running:
        ui.updateWindow()
        GM.nextMove()

