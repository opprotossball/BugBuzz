from BackEnd.GameMechanic.GameMaster import GameMaster
from BackEnd.GameMechanic.HumanPlayer import HumanPlayer
from BackEnd.GameObjects.Armia import Armia
from BackEnd.GameObjects.Plansza import Plansza
from BackEnd.GameObjects.Robal import *
from Util import Information
from Util.PlayerEnum import PlayerEnum


def set_position(position, board, player):
    side = player.side
    for elem in position:
        option = elem[0]
        if option == 'K':
            bug = Konik(side)
        elif option == 'M':
            bug = Mrowka(side)
        elif option == 'P':
            bug = Pajak(side)
        elif option == 'Z':
            bug = Zuk(side)
        else:
            raise Exception("Something is NOT yes")
        bug.army = Armia(board=board)
        player.bugList.append(bug)
        player.bugs_available[bug.short_name] -= 1
        tile = board.get_field(elem[1][0], elem[1][1])
        bug.move_bug_to(tile)


def launch_combat_demo():
    gm = GameMaster()

    board = Plansza(Information.board_size)

    whites_position = [('M', (0, -2)), ('P', (-1, 1)), ('K', (-1, 0)), ('K', (-2, 1)), ('K', (0, 2))]
    white_player = HumanPlayer(gm, PlayerEnum.B)
    set_position(whites_position, board, white_player)

    blacks_position = [('M', (1, 0)), ('P', (0, 1)), ('K', (1, -1)), ('K', (0, -1)), ('Z', (0, 0))]
    black_player = HumanPlayer(gm, PlayerEnum.C)
    set_position(blacks_position, board, black_player)

    gm.set_display()
    gm.set_new_debug_ui()
    gm.new_game(white_player, black_player, board=board, start_at_turn=5)


def launch_move_demo():
    gm = GameMaster()

    board = Plansza(Information.board_size)

    whites_position = [('K', (-3, 1)), ('Z', (-1, -1)), ('P', (3, 1)), ('M', (0, -3))]
    white_player = HumanPlayer(gm, PlayerEnum.B)
    set_position(whites_position, board, white_player)

    blacks_position = [('Z', (1, 0)), ('P', (-1, 3)), ('K', (2, -4))]
    black_player = HumanPlayer(gm, PlayerEnum.C)
    set_position(blacks_position, board, black_player)

    gm.set_display()
    gm.set_new_debug_ui()
    gm.new_game(white_player, black_player, board=board, start_at_turn=0)


def launch_hatch_demo():
    gm = GameMaster()

    board = Plansza(Information.board_size)

    whites_position = [('M', (1, 0)), ('K', (1, -1)), ('P', (2, -2)), ('Z', (2, -3)), ('K', (1, -3))]
    white_player = HumanPlayer(gm, PlayerEnum.B)
    set_position(whites_position, board, white_player)

    black_player = HumanPlayer(gm, PlayerEnum.C)

    gm.set_display()
    gm.set_new_debug_ui()
    gm.new_game(white_player, black_player, board=board, start_at_turn=0)
