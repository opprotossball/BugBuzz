from BackEnd.GameObjects.Plansza import Plansza, get_key_for
from GameEnv import GameEnv
from ActionCodeDict import action_list

if __name__ == "__main__":
    env = GameEnv()
    n_actions = 10000
    nval = 0
    for _ in range(n_actions):
        action = env.action_space.sample()
        print(action_list[action])
        #action = {"type": 11, "tile": (0, 0)}
        obs, reward, done, info = env.step(action)
        nval += reward >= 0
    print(nval)
    print(env.gm.pos_code())
