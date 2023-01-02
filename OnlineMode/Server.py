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

                clients_position = pickle.loads(connection.recv(self.data_chunk))

                if clients_position is None:
                    break

                if not (game_id in self.games):
                    break

                if clients_position.winner_side is not None:
                    self.games[game_id].winner = clients_position.winner_side

                if clients_position.valid and self.games[game_id].ready:
                    self.games[game_id].position = clients_position

                self.games[game_id].position.ready = self.games[game_id].ready
                self.games[game_id].position.winner_side = self.games[game_id].winner
                connection.sendall(pickle.dumps(self.games[game_id].position))

            except:
                break

        print("Lost connection with", connection.getpeername())
        if self.game_count >= 0 and game_id in self.games:
            self.games.pop(game_id)
            print("Closing Game ", game_id)
            self.game_count -= 1
        self.player_count -= 1
        connection.close()

    def run(self):
        self.socket.listen()
        while True:
            connection, address = self.socket.accept()
            print(address, "connected")
            self.player_count += 1
            player_side = PlayerEnum.B   # TODO change to give players random side
            if self.player_count % 2 == 1:
                game = GameState()
                game.position.set_starting_position()
                self.games[self.game_count] = game
                self.game_count += 1
                print("Creating a new game...")
            else:
                self.games[self.game_count - 1].ready = True
                player_side = PlayerEnum.C
                print("Game ", self.game_count - 1, " is ready!")

            start_new_thread(self.threaded_client, (connection, player_side, self.game_count - 1))


if __name__ == "__main__":
    server = Server()
    server.run()
