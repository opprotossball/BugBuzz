import threading
import time

from AI_module.Evaluator.GameEvaluator import Evaluator


class Trainer:
    def __init__(self, evaluator, threads_count=1, simulation_per_thread=1024, save_interval=5000, log_interval=1000):
        self.Ev = evaluator
        self.threads = []
        self.save_interval = save_interval
        for index in range(threads_count):
            thread = TrainingThread(index, self.Ev, simulation_per_thread, log_interval)
            self.threads.append(thread)

    def run(self):
        for thread in self.threads:
            thread.start()

        for thread in self.threads:
            thread.join()

    def save(self):
        pass

    def set_target_nn_file(self, nn_file):
        pass

    def set_target_gm_file(self, gm_file):
        pass

    def set_target_ts_file(self, ts_file):
        pass

    def final_feed_back(self):
        pass


class TrainingThread:
    def __init__(self, id, evaluator, number_of_simulation, log_interval):
        self.id = id
        self.evaluator = evaluator
        self.thread = threading.Thread()

        self.number_of_simulation = number_of_simulation
        self.simulation_counter = 0
        self.tst_count = 0
        self.eval_count = 0

        self.start_time = 0
        self.last_log = 0

    def start(self):
        self.start_time = time.time()
        self.last_log = self.start_time
        self.thread.start()

    def join(self):
        self.thread.join()

    def get_terminal_states(self):
        pass

    def save_self(self):
        pass

    def log(self):
        now = time.time()
        if self.number_of_simulation < 0:
            sim_left = "Inf"
        else:
            sim_left = self.number_of_simulation - self.simulation_counter
        print("|Thread id: {id:3} |"
              "Time running: {time_from_start:7.2f} [s]|"
              "Time from last log: {time_from_last_log:7.2f} [s]|"
              "Number of simulation performed: {sim_count:10} |"
              "Number of simulation left: {sim_left:10} |"
              "Number of terminal states reached: {tst_count:6} |"
              "Position evaluated: {eval_count:10} |"
              "".format(id=self.id,
                        time_from_start=(now - self.start_time),
                        time_from_last_log=(now - self.last_log),
                        sim_count=self.simulation_counter,
                        sim_left=sim_left,
                        tst_count=self.tst_count,
                        eval_count=self.eval_count))
        self.last_log = now

