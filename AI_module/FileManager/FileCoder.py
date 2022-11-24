import pandas as pd

from AI_module.AI.NN import NN
from AI_module.FileManager.LayerSeriesManagment import from_series


def save_model_to_csv(NN, filename):
    if not NN.is_finalized:
        raise Exception("You can't save non finalised model.")
    df = NN.get_layers_df()
    df.to_csv(filename)


def load_model_from_csv(filename):
    df = pd.read_csv(filename)
    nn = NN()
    for index, row in df.iterrows():
        layer = from_series(row)
        nn.put_layer(layer)
    nn.finalize()
    return nn


def load_game_tree_from_csv(filename):      # TODO
    pass


def save_game_tree_to_csv(gm, filename):    # TODO
    pass


def load_terminal_stat_from_csv(filename):  # TODO
    pass


def save_terminal_state_to_csv(ts, filename):   # TODO
    pass
