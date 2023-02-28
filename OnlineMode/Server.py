import pickle
import socket
from _thread import *

from OnlineMode.GameState import GameState
from Util.PlayerEnum import PlayerEnum
from datetime import datetime


class Server:

    def __init__(self):
        self.ip = "0.0.0.0"
        self.log_file_path = "server_log.txt"
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
        self.log_file = None
        self.write_to_log_file("SERVER STARTED\n")

    def open_log_file(self):
        self.log_file = open(self.log_file_path, "a")

    def write_to_log_file(self, message):
        self.open_log_file()
        self.log_file.write(datetime.now().strftime("%d/%m/%Y, %H:%M:%S") + " " + message + "\n")
        self.log_file.close()

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

        self.write_to_log_file(" Lost connection with " + str(connection.getpeername()))

        if self.game_count >= 0 and game_id in self.games:
            self.games.pop(game_id)
            self.write_to_log_file("Closing Game " + str(game_id))
            self.game_count -= 1
        self.player_count -= 1
        connection.close()

    def run(self):
        self.socket.listen()
        while True:
            connection, address = self.socket.accept()
            self.write_to_log_file(str(address) + " connected")
            self.player_count += 1
            player_side = PlayerEnum.B   # TODO change to give players random side
            if self.player_count % 2 == 1:
                game = GameState()
                game.position.set_starting_position()
                self.games[self.game_count] = game
                self.game_count += 1
                self.write_to_log_file("Created new game")
            else:
                self.games[self.game_count - 1].ready = True
                player_side = PlayerEnum.C
                self.write_to_log_file("Game " + str(self.game_count - 1) + " is ready")

            start_new_thread(self.threaded_client, (connection, player_side, self.game_count - 1))


if __name__ == "__main__":
    server = Server()
    server.run()
