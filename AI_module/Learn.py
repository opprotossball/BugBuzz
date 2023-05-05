import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Flatten, Input
from keras.optimizers import Adam
from rl.agents import DQNAgent
from rl.memory import SequentialMemory
from rl.policy import BoltzmannQPolicy, MaxBoltzmannQPolicy

from AI_module.ActionCodeDict import action_list
from AI_module.GameEnv import GameEnv


def build_model(states_shape, n_actions):
    model = Sequential()
    n_states = states_shape[0]
    model.add(Flatten(input_shape=(1, n_states)))
    model.add(Dense(190, activation='relu'))
    model.add(Dense(190, activation='relu'))
    model.add(Dense(n_actions, activation='linear'))
    return model


def build_agent(model, actions):
    policy = MaxBoltzmannQPolicy()
    memory = SequentialMemory(limit=50000, window_length=1)
    dqn = DQNAgent(model=model, memory=memory, policy=policy,
                  nb_actions=actions, nb_steps_warmup=1000, target_model_update=1e-2)
    return dqn


def train_agent(file_path, nb_steps, learning_rate):
    env = GameEnv()
    model = build_model(env.observation_space.shape, len(action_list))
    model.summary()
    dqn = build_agent(model, len(action_list))
    dqn.compile(Adam(lr=learning_rate), metrics=['mae'])
    dqn.fit(env, nb_steps=nb_steps, visualize=False, verbose=1)
    dqn.save_weights(file_path, overwrite=True)


def test_agent(file_path, nb_episodes):
    env = GameEnv()
    model = build_model(env.observation_space.shape, len(action_list))
    dqn = build_agent(model, len(action_list))
    dqn.compile(Adam(lr=0.05), metrics=['mae'])
    dqn.load_weights(file_path)
    _ = dqn.test(env, nb_episodes=nb_episodes, visualize=True)


if __name__ == "__main__":
    test_agent('Models/dqn3_weights.h5f', 3)
    #train_agent('Models/dqn3_weights.h5f', 50000, learning_rate=0.05)

