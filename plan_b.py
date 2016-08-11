import numpy as np
import tetris

class Dayumm:
    def __init__(self, list):
        self.vector = np.matrix(list)

    def play(self, board, index, rotate, x, y):
        buttons = ['NOTHING', 'UP', 'RIGHT','LEFT' ]
        input_vector = self.parse_input(board, index, rotate, x, y)
        out_vector = self.get_output(input_vector)
        i = self.get_choice(out_vector)
        return buttons[i]
