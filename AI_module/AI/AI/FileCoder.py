import pandas as pd
from AI.Layer.LayerSeriesManagment import to_dict, from_series
from AI.nNN import nNN


class FileCoder:
    def save_model_to_csv(self, NN, filename):
        if not NN.is_finalized:
            raise Exception("You can't save non finalised model.")
        df = NN.get_layers_df()
        df.to_csv(filename)

    def load_model_from_csv(self, filename):
        df = pd.read_csv(filename)
        nn = nNN()
        for index, row in df.iterrows():
            layer = from_series(row)
            nn.put_layer(layer)
        nn.finalize()
        return nn
