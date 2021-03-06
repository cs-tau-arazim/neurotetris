import numpy as np

determination_factor = 1.4
board_width = 10
rotations_num = 4

def threshold_function(x):
    if x>0.5:
        return 1
    return 0
    #return 1.0 / (1 + np.exp(-20.0 * (x - 1)))

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
        output = self.weight_matrices[length - 1] * output
        #print output.getT().tolist()[0]
        return output

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
        copy_vec = vector_as_list[:]
        copy_vec.remove(m)
        if (m <= determination_factor*max(copy_vec) or m <= 0) and vector_as_list.index(m) != 1:
            return 0
        for i in xrange(len(vector_as_list)):
            if vector_as_list[i] == m:
                return i

        assert 1 == 0, "Could not find the maximum for some reason..."  # not supposed to get to this line
        pass

    # returns the key that is pressed based on the input
    # index - 3 bit, rotate - 2 bit,  x - 4 bit, y - 5 bit
    def play2(self, board, index, rotate, x, y):
        buttons = ['NOTHING', 'UP', 'RIGHT','LEFT' ]
        input_vector = self.parse_input(board, index, rotate, x, y)
        out_vector = self.get_output(input_vector)
        i = self.get_choice(out_vector)
        return buttons[i]

    def get_rotate_and_x_choice(self,vector,rotate,x):
        vector_as_list = vector.getT().tolist()
        vector_as_list = vector_as_list[0]
        x_cor = vector_as_list[:board_width]
        rotations = vector_as_list[-rotations_num:]
        m_x = max(x_cor)
        m_rotate = max(rotations)
        res_x,res_rot = x_cor.index(m_x), rotations.index(m_rotate)

        copy_x_cor = x_cor[:]
        copy_x_cor.remove(m_x)
        if (m_x <= determination_factor*max(copy_x_cor) or m_x <= 0):
            res_x = x
        """
        copy_rot = rotations[:]
        copy_rot.remove(m_rotate)
        if (m_rotate <= determination_factor*max(copy_rot) or m_rotate <= 0):
            res_rot = rotate
            """

        return (res_x, res_rot)

    def play(self, board, index, rotate, x, y):
        buttons = ['NOTHING', 'UP', 'RIGHT','LEFT' ]
        input_vector = self.parse_input2(board, index)
        out_vector = self.get_output(input_vector)

        x_res,rot_res = self.get_rotate_and_x_choice(out_vector,rotate,x)
        if x > x_res:
            return 'LEFT'
        if x < x_res:
            return 'RIGHT'
        if not rot_res == rotate:
            return 'UP'
        return 'NOTHING'

# converts the board into it's input represetation
    def parse_input2(self, board, index):
        input_vector = []
        for i in xrange(len(board) - 1):         # the last line is irreleveant
            for j in xrange(len(board[i])):
                input_vector.append(self.to_binary_rep(board[i][j]))
        for i in xrange(3):
            input_vector.append(index%2)
            index /= 2
        return np.matrix([input_vector]).getT()


