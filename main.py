from FrontEnd.GameMaster import GameMaster
from FrontEnd.InterfejsGracza import InterfejsGracza
from FrontEnd.UI import UI

if __name__ == '__main__':
    GM = GameMaster()
    ui = UI(GM.plansza)

    player1 = InterfejsGracza(GM, "B", lambda: GM.updateWindow())
    player2 = InterfejsGracza(GM, "C", lambda: GM.updateWindow())

    screenWidth = 1000
    screenHeight = 800

    GM.setUI(ui)
    GM.newGame(player1, player2)

    while True:
        GM.updateWindow()
        GM.nextMove()
