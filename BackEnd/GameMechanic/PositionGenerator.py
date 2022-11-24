from BackEnd.GameMechanic.GameMechanic import GameMechanic
from BackEnd.GameObjects.Plansza import Plansza
from BackEnd.GameMechanic.GeneratorPlayer import GeneratorPlayer
from Util import Information


def set_bugs_available(board, player):
    for tile in board.iterList:
        bug = tile.bug
        if bug is not None and bug.side == player.side:
            player.bugs_available[bug.short_name] -= 1




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


if __name__ == "__main__":  # TEST - printuje pola hatchery
    pg = PositionGenerator()
    board = Plansza(Information.board_size)
    result = pg.get_hatches(board, 'B')
    for p in result:
        print()
        st = ""
        for h in p[0].whitesHatchery:
            if h.bug is None:
                st += "-"
            else:
                st += h.bug.short_name
        print(st)
        print(p[1], "\n")
