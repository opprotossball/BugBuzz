from BackEnd.GameMechanic.Zobrist import Zobrist
from BackEnd.GameObjects.Robal import Konik, RobalEnum
from Client import Client
from Util.PlayerEnum import PlayerEnum

if __name__ == "__main__":
    client = Client()
    client.configure("", 5555)  # put server's ip here
    client.run_game()
