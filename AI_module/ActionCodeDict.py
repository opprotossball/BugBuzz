from BackEnd.GameObjects.Plansza import Plansza
from Util.Information import ActionType
import Util.Information as Information

p = Plansza()
action_list = [(ActionType.PASS, None, None)]  # PASS

for tile_id in range(Information.n_tiles):

    action_list.append((ActionType.KILL, tile_id, None))  # KILL

    for d in Information.Direction:
        if p.is_valid_neigh(p.iterList[tile_id], d):
            action_list.append((ActionType.MOVE, tile_id, d))  # MOVE

for hatch_id in range(3):
    for bug_type in Information.bug_types:
        action_list.append((ActionType.HATCH, hatch_id, bug_type))  # HATCH
