

class _Kernal:
    def __init__(self, size, layers):
        self.size = size
        self.layers = layers

        self.weights = [[0] * layers] * size ** 2

    def eval(self, board, coordinate_root):
        sum = 0
        field = root_field
        pivot_field = root_field
        for x in range(self.size):
            pivot_field = pivot_field.ES
            for y in range(self.size):
                eval_field = self.eval_field(field)
                for idx, val in enumerate(eval_field):
                    sum += self.weights[x*self.size + y][idx] * val
                field = field.W
            field = pivot_field

        return sum


    def eval_field(self, field):
        return [0]
