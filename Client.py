import pickle
import socket
import pygame

from BackEnd.GameMechanic.GameMaster import GameMaster
from BackEnd.GameMechanic.HumanPlayer import HumanPlayer
from BackEnd.GameMechanic.OnlinePlayer import OnlinePlayer
from BackEnd.GameMechanic.Player import PlayerState
from FrontEnd.DefeatScene import DefeatScene
from FrontEnd.GameScene import GameScene
from FrontEnd.LoadingScene import LoadingScene
from FrontEnd.MenuScene import MenuScene
from FrontEnd.VictoryScene import VictoryScene
from OnlineMode.Position import Position
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
        self.fps = 60
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
                is_active = self.get_active_player() == self.online_player_side

            if not self.playing_online and self.socket is not None:
                self.socket = None

            self.update_window()

            if self.playing_online and self.socket is not None:
                game = Position(self.board, self.turn, self.winner_side)

                if isinstance(self.display.scene, GameScene):  # to show what opponent is selecting
                    game.active_rolls = self.ui.rolls
                    game.active_kills = self.get_player(self.online_player_side).kills
                    game.highlighted_by_active = [tile.cor() for tile in self.display.scene.highlightedTiles]
                    if self.ui.selected_tile is not None:
                        game.active_leader = self.ui.selected_tile.cor()

                game.valid = is_active

                received_game = self.exchange_data(game)

                if not self.playing_online:  # was disconnected
                    continue

                if received_game.ready and isinstance(self.display.scene, LoadingScene):
                    self.display.set_scene(GameScene(self))

                if isinstance(self.display.scene, GameScene):
                    if received_game.winner_side is not None:
                        self.winner_side = received_game.winner_side
                        self.playing_online = False
                    elif self.get_player(self.online_player_side).state == PlayerState.INACTIVE:
                        self.board = received_game.board
                        self.set_bugs_for_both_players()
                        self.set_phase(received_game.turn)

                        self.display.scene.online_opponent_rolls = received_game.active_rolls
                        self.display.scene.online_opponent_kills = received_game.active_kills
                        self.display.scene.highlighted_by_online_opponent = []
                        for tile in received_game.highlighted_by_active:
                            self.display.scene.highlighted_by_online_opponent.append(self.board.get_field(tile[0], tile[1]))
                    self.game_is_over()

            if isinstance(self.display.scene, GameScene) and self.winner_side is not None:
                if self.winner_side == self.online_player_side:
                    self.display.set_scene(VictoryScene(self, self.online_player_side))
                else:
                    self.display.set_scene(DefeatScene(self, self.online_player_side))
                self.playing_online = False

            self.clock.tick(self.fps)

    def connect_to_game(self):
        self.server_address = (self.server_ip, self.port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect(self.server_address)
            self.online_player_side = pickle.loads(self.socket.recv(self.data_chunk))
        except:
            self.playing_online = False
            self.display.set_scene(MenuScene(self))
            print("Connection failed")

    def exchange_data(self, data):
        try:
            self.socket.sendall(pickle.dumps(data))
            return pickle.loads(self.socket.recv(self.data_chunk))
        except:
            self.playing_online = False
            self.display.set_scene(MenuScene(self))
            print("Lost connection")

    def play_online(self):
        self.connect_to_game()
        if self.online_player_side == PlayerEnum.B:
            self.new_game(HumanPlayer(self, PlayerEnum.B), OnlinePlayer(self, PlayerEnum.C))
        else:
            self.new_game(OnlinePlayer(self, PlayerEnum.B), HumanPlayer(self, PlayerEnum.C))
        self.display.set_scene(LoadingScene(self))
        print("My side is: " + str(self.online_player_side))
