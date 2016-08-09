import numpy as np


def threshold_function(x):
    return 1.0 / (1 + np.exp(-20.0 * (x - 1)))


class Ann:
    def __init__(self, matrices):
        self.original_matrices = matrices
        self.weight_matrices = []
        for mat in matrices:
            self.weight_matrices.append(np.matrix(mat))

    # returns the output vector
    def get_output(self, input_vector):
        output = input_vector
        length = len(self.weight_matrices)
        for i in xrange(length - 1):
            output = self.weight_matrices[i] * output
            output = self.check_threshold(output)

        return self.weight_matrices[length - 1] * output

    # returns a binary vector of the nuerons being fired
    def check_threshold(self, v):
        lst = v.getT().tolist()
        lst = lst[0]
        lst = [threshold_function(x) for x in lst]
        return np.matrix([lst]).getT()

    # converts the board into it's input represetation
    def parse_board(self, board):
        input_vector = []
        for i in xrange(len(board) - 1):         # the last line is irreleveant
            for j in xrange(len(board[i])):
                input_vector.append(board[i][j])
        return np.matrix([input_vector]).getT()



    # returns the index of the maximum
    def get_max_index(self,vector):
        vector_as_list = vector.tolist()
        vector_as_list = vector_as_list[0]
        index = 0
        m = max(vector_as_list)
        for i in xrange(len(vector_as_list)):
            if vector_as_list[i] == m:
                return i

        assert 1 == 0, "Could not find the maximum for some reason..."  # not supposed to get to this line
        pass

    # returns the key that is pressed based on the input
    def play(self, board):
        buttons = ['LEFT', 'RIGHT', 'UP', 'NOTHING']
        input_vector = self.parse_board(board)
        out_vector = self.get_output(input_vector)
        return buttons[self.get_max_index(out_vector)]
