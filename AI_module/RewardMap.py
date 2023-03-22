from BackEnd.GameObjects.Plansza import Plansza

INF = 99
distance_reward = {
    0: 10,
    1: 5,
    2: 3,
    3: 2,
    4: 1
}


class RewardMap:

    def __init__(self, board):
        self.board = board
        self.size = board.size
        self.reward = [[INF for _ in range(2 * self.size + 1)] for _ in range(2 * self.size + 1)]

        for r in board.resources:
            self.set_reward(r, 0)
            self.dfs(r, 0)

        for row in self.reward:
            row[:] = [distance_reward.get(dist, 0) for dist in row]

    def dfs(self, field, depth):
        depth += 1
        for neigh in self.board.get_field_neighs(field):
            if neigh is None:
                continue
            if self.get_reward(neigh) > depth:
                self.reward[neigh.x + self.size][neigh.y + self.size] = depth
                self.dfs(neigh, depth)

    def get_reward(self, field):
        return self.reward[field.x + self.size][field.y + self.size]

    def set_reward(self, field, value):
        self.reward[field.x + self.size][field.y + self.size] = value


rewardMap = RewardMap(Plansza(4))
