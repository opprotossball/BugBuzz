import pickle
import socket
from _thread import *

from OnlineMode.GameState import GameState
from Util.PlayerEnum import PlayerEnum


class Server:

    def __init__(self):
        self.ip = "10.0.20.100"
        self.port = 5555
        self.data_chunk = 4096*16  # in bytes
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player_count = 0
        self.game_count = 0
        self.games = {}
        try:
            self.socket.bind((self.ip, self.port))
        except socket.error as e:
            print(e)

    def threaded_client(self, connection, player_side, game_id):
        connection.sendall(pickle.dumps(player_side))
        while True:
            try:
                clients_game = pickle.loads(connection.recv(self.data_chunk))

                if clients_game is None:
                    break
                if not (game_id in self.games):
                    break
                if clients_game.valid:
                    self.games[game_id] = clients_game
                connection.sendall(pickle.dumps(self.games[game_id]))
            except error as e:
                print(e)
                break

        print("Lost connection")
        try:
            del self.games[game_id]
            print("Closing Game", game_id)
        except:
            pass
        self.player_count -= 1
        connection.close()

    def run(self):
        self.socket.listen()
        while True:
            connection, address = self.socket.accept()
            print(address, " connected")
            self.player_count += 1
            player_side = PlayerEnum.B   # TODO change to give players random side
            if self.player_count % 2 == 1:
                game = GameState()
                game.set_starting_position()
                self.games[self.game_count] = game
                self.games[self.game_count].ready = False
                self.game_count += 1
                print("Creating a new game...")
            else:
                self.games[self.game_count - 1].ready = True
                player_side = PlayerEnum.C

            start_new_thread(self.threaded_client, (connection, player_side, self.game_count - 1))


if __name__ == "__main__":
    server = Server()
    server.run()
