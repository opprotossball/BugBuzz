import pickle
import socket
import pygame
from BackEnd.GameMechanic.GameMaster import GameMaster
from BackEnd.GameMechanic.HumanPlayer import HumanPlayer
from BackEnd.GameMechanic.OnlinePlayer import OnlinePlayer
from BackEnd.GameMechanic.Player import PlayerState
from BackEnd.GameObjects.Plansza import Plansza
from FrontEnd.GameScene import GameScene
from FrontEnd.MenuScene import MenuScene
from FrontEnd.VictoryScene import VictoryScene
from OnlineMode.GameState import GameState
from Util import Information
from Util.PlayerEnum import PlayerEnum


class Client(GameMaster):

    def __init__(self):
        super().__init__()
        self.set_display()
        self.server_ip = None
        self.port = None
        self.server_address = None
        self.socket = None
        self.data_chunk = None
        self.online_player_side = None
        self.online_opponent_side = None
        self.clock = pygame.time.Clock()
        pygame.init()

    def configure(self, server_ip, port, data_chunk=4096*16):
        self.server_ip = server_ip
        self.port = port
        self.data_chunk = data_chunk

    def run_game(self):
        self.display.set_scene(MenuScene(self))
        while True:
            if self.playing_online:
                if self.socket is None:  # initialize game
                    self.play_online()
                    if self.online_player_side == PlayerEnum.B:
                        self.new_game(HumanPlayer(self, PlayerEnum.B), OnlinePlayer(self, PlayerEnum.C))
                    else:
                        self.new_game(OnlinePlayer(self, PlayerEnum.B), HumanPlayer(self, PlayerEnum.C))

                is_active = self.get_active_player() == self.online_player_side

            self.update_window()

            if self.display.scene == GameScene and self.game_is_over():
                self.board = Plansza(Information.board_size)
                self.display.set_scene(VictoryScene(self, self.winner_side))
                self.playing_online = False

            elif self.playing_online and self.socket is not None:
                game = GameState(self.board, self.turn, self.winner_side)
                #game.set_active(self.get_active_player())
                game.valid = is_active

                received_game = self.exchange_data(game)

                if self.get_player(self.online_player_side).state == PlayerState.INACTIVE:
                    self.board = received_game.board
                    self.set_bugs_for_both_players()
                    self.set_phase(received_game.turn)

            self.clock.tick(60)

    def connect_to_game(self):
        self.server_address = (self.server_ip, self.port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect(self.server_address)
            self.online_player_side = pickle.loads(self.socket.recv(self.data_chunk))
        except:
            print("Connection failed")

    def exchange_data(self, data):
        try:
            self.socket.sendall(pickle.dumps(data))
            return pickle.loads(self.socket.recv(self.data_chunk))
        except socket.error as e:
            print(e)

    def play_online(self):
        self.connect_to_game()
        if self.online_player_side == PlayerEnum.B:
            self.online_opponent_side = PlayerEnum.C
        else:
            self.online_opponent_side = PlayerEnum.B
        print("My side is: " + str(self.online_player_side))


if __name__ == "__main__":
    client = Client()
    client.configure("10.0.20.100", 5555)
    client.run_game()
