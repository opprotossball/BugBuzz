import os.path

import pandas as pd

from AI_module.AI.TerminalStatesTracker import TerminalStatesTracker
from AI_module.Evaluator.GameDictionary import GameDictionary
from AI_module.Evaluator.GameEvaluator import Evaluator
from AI_module.FileManager.FileCoder import *
from AI_module.AI.Layer.FullyConnected import FullyConnected
from AI_module.AI.Layer.InputLayer import InputLayer
from AI_module.AI.NN import NN

#   A
from AI_module.Trainer import Trainer

nn_id = ""
ts_id = ""
'''
If for given id there will be now result in dir AI_data/. it will result creating brand new AI_module and will start 
learning process from the beginning (card blanch).I this case, it is compulsory to fill, all parameters in section B.
'''

number_of_simulation_per_thread = 1024
save_interval = 5000
log_interval = 1000
'''
negative number will cause indefinite learning mode. In this case please be sure that you have specified how often you
want to save progress. Log is short information of the progress of given thread.
'''

number_of_threads = 4
'''
This parameter has to be greater then 0
'''

#   B
layer_distribution = [(100, "ReLU"), (100, "ReLU"), (30, "ReLu")]
'''
Format (size_of_layer, activation_function)
Warning! Input layer is hard coded and can't be changed.
Possible activation function:
    -"SoftMax" 
    -"ReLu" 
    -"Neutral" # f(x) = x
'''

if __name__ == "__main__":

    nn_file = "AI_data/AI_model_saved_{id}.csv".format(id=id)
    gm_file = "AI_data/AI_game_tree.csv"
    ts_file = "AI_data/AI_terminal_state_{id}.csv".format(id=id)

    if os.path.exists(nn_file):
        nn = load_model_from_csv(nn_file)
    else:
        nn = NN()
        in_l = InputLayer(315)
        nn.put_layer(in_l)
        for layer_argument in layer_distribution:
            layer = FullyConnected(layer_argument[0], layer_argument[1])
            nn.put_layer(layer)
        out_l = FullyConnected(1, "ReLu")
        nn.put_layer(out_l)
        nn.finalize()

    if os.path.exists(gm_file):
        gm = load_game_tree_from_csv(gm_file)
    else:
        gm = GameDictionary()

    if os.path.exists(ts_file):
        ts = load_terminal_stat_from_csv(ts_file)
    else:
        ts = TerminalStatesTracker(ts_file)

    evaluator = Evaluator(nn)
    trainer = Trainer(Evaluator, number_of_simulation_per_thread, save_interval)
    trainer.set_target_nn_file(nn_file)
    trainer.set_target_gm_file(gm_file)
    trainer.set_target_ts_file(ts_file)

    trainer.run()
