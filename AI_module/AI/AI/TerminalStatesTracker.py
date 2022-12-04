import pandas as pd

class TerminalStatesTracker:
    def __init__(self, target_file_name, buffer_size=20):
        self.counter = 0
        self.buffer_size = buffer_size
        self.file_name = target_file_name
        self.df = pd.DataFrame()

    def add_state(self, coded_position, winning_player):
        if self.counter == self.buffer_size:
            self.save_buffer()
        if winning_player == PlayerEnum.B:
            self.df = pd.concat([self.df, pd.DataFrame({"position": [coded_position], "eval": [1]})], ignore_index=True)
        elif winning_player == PlayerEnum.C:
            self.df = pd.concat([self.df, pd.DataFrame({"position": [coded_position], "eval": [0]})], ignore_index=True)

    def close(self):
        self.save_buffer()

    def save_buffer(self):
        self.df.to_csv(self.file_name)
