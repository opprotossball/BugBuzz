from BackEnd.GameMechanic.GameMechanic import GameMechanic
from BackEnd.GameObjects.Plansza import Plansza
from BackEnd.GameMechanic.GeneratorPlayer import GeneratorPlayer
from Util import Information
from Util.PlayerEnum import PlayerEnum

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

        hatchery = gm.get_available_space_for_hatch(player_side)
        for tile in hatchery:
            for position in positions_with_players:
                for key, value in player.bugs_available.items():
                    gm.set_board(position[0].clone())
                    player = position[1].clone_for_hatch()
                    gm.set_player(player)
                    coordinates = tile.cor()
                    actual_tile = gm.board.get_field(coordinates[0], coordinates[1], coordinates[2])  # don't ask
                    if player.perform_hatch(key, actual_tile):
                        code = "" + str(player_side) + "h" + actual_tile.coordinates_to_string() + str(key) + "/"
                        positions_with_players.append((gm.board, player, position[2] + code))

        positions = []
        for pp in positions_with_players:
            positions.append((pp[0], pp[2]))

        return positions

    def get_moves(self, given_board, player_side, return_boards=False):
        gm = GameMechanic()
        positions = []  # (player, army_tiles, code)
        board = given_board.clone()
        player = GeneratorPlayer(gm, player_side)
        gm.set_player_bugs(board, player)

        army_tiles = []

        considered = set()

        for a in gm.get_armies(player_side, player):
            army_tiles.append(a.bugList[0].field)

        positions.append((player, army_tiles, ""))
        considered.add(board.get_hash_2())

        old_player = player

        for position in positions:
            for tile in position[1]:
                for direction in Information.directionOptions:
                    player = position[0].clone_for_move()
                    gm.set_player(player)
                    gm.change_position_for_player(old_player, player)
                    old_player = player
                    gm.set_army_on_tile(tile)
                    army = tile.bug.army
                    if player.perform_move(army, direction):
                        position_hash = board.get_hash_2()
                        if not (position_hash in considered):
                            code = "" + str(player_side) + "m" + tile.coordinates_to_string() + direction + "/"
                            army_tiles = []
                            for a in gm.get_armies(player_side, player):
                                army_tiles.append(a.bugList[0].field)
                            positions.append((player, army_tiles, position[2] + code))
                            considered.add(position_hash)

        if return_boards:  # pls dont use it
            p = []
            for position in positions:
                b = Plansza(Information.board_size)
                gm.set_position_for_player(b, position[0], delete_others=False)
                p.append((b, position[2]))
            return p

        return positions


if __name__ == "__main__":  # TEST
    pg = PositionGenerator()
    b = Plansza(Information.board_size)
    positions = pg.get_hatches(b, PlayerEnum.B)
    print(positions)
    # i = 0
    # bug = Zuk(PlayerEnum.C)
    # bug.move_bug_to(b.iterList[60])
    # bug = Zuk(PlayerEnum.B)
    # bug.move_bug_to(b.iterList[54])
    # bug = Konik(PlayerEnum.B)
    # bug.move_bug_to(b.iterList[47])
    # start = time.time()
    # result = pg.get_moves(b, PlayerEnum.B)
    # t = time.time() - start
    # print("unique positions: ", len(result))
    # print("time: ", t, "s")

    exit()



