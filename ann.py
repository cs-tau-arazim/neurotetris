import numpy as np

determination_factor = 2

def threshold_function2(x):
    return 1.0 / (1 + np.exp(-20.0 * (x - 1)))

def threshold_function(x):
    return x


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
    def parse_input(self, board, index, rotate, x, y):
        input_vector = []
        for i in xrange(len(board) - 1):         # the last line is irreleveant
            for j in xrange(len(board[i])):
                input_vector.append(self.to_binary_rep(board[i][j]))
        for i in xrange(3):
            input_vector.append(index%2)
            index /= 2
        for i in xrange(2):
            input_vector.append(rotate%2)
            rotate /= 2
        for i in xrange(4):
            input_vector.append(x%2)
            x /= 2
        for i in xrange(5):
            input_vector.append(y%2)
            y /= 2
        return np.matrix([input_vector]).getT()

    def to_binary_rep(self, n):
        if n > 0:
            return 1
        return 0


    # returns the index of the maximum
    def get_choice(self,vector):
        vector_as_list = vector.getT().tolist()
        vector_as_list = vector_as_list[0]
        m = max(vector_as_list)
        for i in xrange(len(vector_as_list)):
            if m < determination_factor*vector_as_list[i]:
                return 0
        for i in xrange(len(vector_as_list)):
            if vector_as_list[i] == m:
                return i

        assert 1 == 0, "Could not find the maximum for some reason..."  # not supposed to get to this line
        pass

    # returns the key that is pressed based on the input
    # index - 3 bit, rotate - 2 bit,  x - 4 bit, y - 5 bit
    def play(self, board, index, rotate, x, y):
        buttons = ['NOTHING', 'LEFT', 'RIGHT', 'UP']
        input_vector = self.parse_input(board, index, rotate, x, y)
        out_vector = self.get_output(input_vector)
        #print out_vector.getT()
        i = self.get_choice(out_vector)

        return buttons[i]
