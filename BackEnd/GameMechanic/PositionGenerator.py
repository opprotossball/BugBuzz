import random
import time

from BackEnd.GameMechanic.GameMechanic import GameMechanic
from BackEnd.GameObjects.Plansza import Plansza
from BackEnd.GameMechanic.GeneratorPlayer import GeneratorPlayer
from BackEnd.GameObjects.Robal import Mrowka, Zuk, Konik
from Util import Information
from Util.HashMap import HashMap

factorials = [1, 1]


def set_bugs_available(board, player):
    for tile in board.iterList:
        bug = tile.bug
        if bug is not None and bug.side == player.side:
            player.bugs_available[bug.short_name] -= 1


def calculate_roll_probability(success_count, dice_count, toughness_length):
    success_chance = 1 - toughness_length / 10
    for i in range(len(factorials), dice_count + 1):
        factorials.append(factorials[-1] * i)
    result = factorials[dice_count] / factorials[success_count] / factorials[dice_count - success_count]
    result *= pow(success_chance, success_count) * pow(1 - success_chance, dice_count - success_count)
    return result


class PositionGenerator:
    def __init__(self):
        self.move_time = 0
        self.clone_time = 0
        self.set_bugs_time = 0
        self.hashing_time = 0
    def get_hatches(self, given_board, player_side):
        gm = GameMechanic()
        positions_with_players = []
        gm.set_board(given_board.clone())
        player = GeneratorPlayer(gm, player_side)
        gm.set_player(player)
        player.resources = gm.get_resources_for_side(player_side)
        # player.resources = 69  # TEST
        set_bugs_available(gm.board, player)

        positions_with_players.append((gm.board, player, ""))

        hatchery = gm.getAvailableSpaceForHatch(player_side)
        for tile in hatchery:
            for position in positions_with_players:
                for key, value in player.bugs_available.items():
                    gm.set_board(position[0].clone())
                    player = position[1].clone()
                    gm.set_player(player)
                    coordinates = tile.cor()
                    actual_tile = gm.board.getField(coordinates[0], coordinates[1], coordinates[2])  # don't ask
                    if player.perform_hatch(key, actual_tile):
                        code = "" + player_side + "h" + actual_tile.coordinates_to_string() + key + "/"
                        positions_with_players.append((gm.board, player, position[2] + code))

        positions = []
        for pp in positions_with_players:
            positions.append((pp[0], pp[2]))

        return positions

    def get_moves(self, given_board, player_side):
        gm = GameMechanic()
        positions = []
        gm.set_board(given_board.clone())

        player = GeneratorPlayer(gm, player_side)
        gm.set_player(player)
        gm.set_player_bugs(gm.board, player)
        army_tiles = []
        for a in gm.get_armies(player_side):
            army_tiles.append(a.bugList[0].field.cor())
        positions.append((gm.board, "", army_tiles))

        considered = set()
        considered.add(gm.board.get_hash_2())

        for position in positions:
            for c in position[2]:
                for direction in Information.directionOptions:

                    start = time.time()
                    gm.set_board(position[0].clone())
                    self.clone_time += time.time() - start

                    actual_tile = gm.board.getField(c[0], c[1], c[2])

                    start = time.time()
                    gm.set_army_on_tile(actual_tile)
                    self.set_bugs_time += time.time() - start

                    start = time.time()
                    player.perform_move(actual_tile.bug.army, direction)
                    self.move_time += time.time() - start

                    start = time.time()
                    board_hash = gm.board.get_hash_2()
                    self.hashing_time += time.time() - start

                    if not (board_hash in considered):
                        code = "" + player_side + "m" + actual_tile.coordinates_to_string() + direction + "/"
                        army_tiles = []

                        start = time.time()

                        gm.set_player_bugs(gm.board, player)
                        for a in gm.get_armies(player_side, player):
                            army_tiles.append(a.bugList[0].field.cor())

                        self.set_bugs_time += time.time() - start


                        # army_tiles = [i for i in position[2]]
                        # army_tiles.remove(c)
                        # army_tiles.append(actual_tile.getDictionary()[direction].cor())
                        positions.append((gm.board, position[1] + code, army_tiles))
                        considered.add(board_hash)


        return positions


if __name__ == "__main__":  # TEST - printuje pola hatchery

    pg = PositionGenerator()
    board = Plansza(Information.board_size)
    i = 0
    for t in board.iterList:
        if t.resources and i < 3:
            i += 1
            bug = Zuk("B")
            bug.moveBugTo(t)
    # bug = Zuk("B")
    # bug.moveBugTo(board.iterList[7])
    # bug = Zuk("B")
    # bug.moveBugTo(board.iterList[0])
    # bug = Konik("B")
    # bug.moveBugTo(board.iterList[59])
    # bug = Konik("B")
    # bug.moveBugTo(board.iterList[60])

    # result = pg.get_hatches(board, 'B')
    # for p in result:
    #     print()
    #     st = ""
    #     for h in p[0].whitesHatchery:
    #         if h.bug is None:
    #             st += "-"
    #         else:
    #             st += h.bug.short_name
    #     print(st)
    #     print(p[1], "\n")
    start = time.time()
    result = pg.get_moves(board, 'B')
    print("time: ", str(time.time() - start))
    for p in result:
        break
        print(p)
    print(len(result))

    # hash speed test
    # board = Plansza(Information.board_size)
    # for t in board.iterList:
    #     bug = Mrowka("B")
    #     if random.randint(0, 2) > 0:
    #         bug.moveBugTo(t)
    # start = time.time()
    # for i in range(0, 100000):
    #     board.__hash__()
    # print(time.time() - start)
    # start = time.time()
    # for i in range(0, 100000):
    #     board.get_hash_2()
    # print(time.time() - start)
    print("bug setting: " + str(pg.set_bugs_time) + "s")
    print("cloning: " + str(pg.clone_time) + "s")
    print("moving: " + str(pg.move_time) + "s")
    print("hashing: " + str(pg.hashing_time) + "s")



