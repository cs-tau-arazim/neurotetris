#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# NOTE FOR WINDOWS USERS:
# You can download a "exefied" version of this game at:
# http://kch42.de/progs/tetris_py_exefied.zip
# If a DLL is missing or something like this, write an E-Mail (kevin@kch42.de)
# or leave a comment on this gist.

# Very simple tetris implementation
#
# Control keys:
#       Down - Drop stone faster
# Left/Right - Move stone
#         Up - Rotate Stone clockwise
#     Escape - Quit game
#          P - Pause game
#     Return - Instant drop
#
# Have fun!

# Copyright (c) 2010 "Kevin Chabowski"<kevin@kch42.de>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import pygame, sys, ann
import random

# The configuration
cell_size = 18
cols = 10
rows = 22
maxfps = 30
playes_per_tick = 1

a = -0.510066
b = 0.760666
c = -0.35663
d = -0.184483

colors = [
    (0, 0, 0),
    (255, 85, 85),
    (100, 200, 115),
    (120, 108, 245),
    (255, 140, 50),
    (50, 120, 52),
    (146, 202, 73),
    (150, 161, 218),
    (35, 35, 35)  # Helper color for background grid
]

# Define the shapes of the single parts

tetris_shapes = [
    [[0, 1, 0],
     [1, 1, 1]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6, 6, 6]],

    [[7, 7],
     [7, 7]]
]

#stone_arr = [i % 6 for i in xrange(1000)]


def rotate_clockwise(shape):
    return [[shape[y][x]
             for y in xrange(len(shape))]
            for x in xrange(len(shape[0]) - 1, -1, -1)]


def check_collision(board, shape, offset):
    off_x, off_y = offset
    for cy, row in enumerate(shape):
        for cx, cell in enumerate(row):
            try:
                if cell and board[cy + off_y][cx + off_x]:
                    return True
            except IndexError:
                return True
    return False


def remove_row(board, row):
    del board[row]
    return [[0 for i in xrange(cols)]] + board


def copy_board(board1):
    boardCopy = []
    for i in xrange(len(board1)):
        boardCopy.append([])
        for j in xrange(len(board1[0])):
            boardCopy[i].append(board1[i][j])
    return boardCopy


def join_matrixes(mat1, mat2, mat2_off):
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            mat1[cy + off_y - 1][cx + off_x] += val
    return mat1


def new_board():
    board = [[0 for x in xrange(cols)]
             for y in xrange(rows)]
    board += [[1 for x in xrange(cols)]]
    return board


class TetrisApp(object):
    def __init__(self, player_ai, unitTime, minimal_gui, minimal_ai, seed, game_limit):  # start game with given ann
        if minimal_gui:
            pygame.init()
            pygame.key.set_repeat(250, 25)

        random.seed(53695)


        self.game_limit = game_limit
        self.width = cell_size * (cols + 6)
        self.height = cell_size * rows
        self.rlim = cell_size * cols
        self.player_ai = player_ai  # new
        self.unitTime = unitTime
        self.minimal_gui = minimal_gui

<<<<<<< HEAD
        self.landed = True
=======
        self.count_rotate = 0;
>>>>>>> origin/master
        self.stone_count = 0
        self.shape_index = 0
        self.shape_rotate = 0
        self.evaluate = 0

        self.lines_cleared = 0

        self.bground_grid = [[8 if x % 2 == y % 2 else 0 for x in xrange(cols)] for y in xrange(rows)]

        if minimal_gui:
            self.default_font = pygame.font.Font(
            pygame.font.get_default_font(), 12)
            self.screen = pygame.display.set_mode((self.width, self.height))
            pygame.event.set_blocked(pygame.MOUSEMOTION)  # We do not need
        # mouse movement
        # events, so we
        # block them.

        self.next_stone = random.choice(tetris_shapes)

        # todo new method

        self.init_game()

    def f_holes(self, board):
        holes = 0
        for i in range(3, len(board)): # todo 3?
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    if board[i-1][j] > 0:
                        holes += 1
        return holes

    def f_aggheight(self, board):
        agg_height = 0
        for j in range(len(board[0])):
            i = 0
            while board[i][j] == 0:
                i += 1
            agg_height += 22 - i
        return agg_height

    def f_rows(self, board):
        rows_num = 0
        for row in board[:-1]:
            if 0 not in row:
                rows_num += 1
        return rows_num

    def f_bumpiness(self, board):
        bumpiness = 0
        prev_bump = 0

        for j in range(len(board[0])):
            i = 0
            while board[i][j] == 0:
                i += 1
            if j == 0:
                prev_bump = 22 - i
            else:
                bumpiness += (prev_bump - (22 - i))**2
                prev_bump = 22 - i

        return bumpiness ** 0.5

    def new_stone(self):
        self.shape_rotate = 0
        self.stone_count += 1
        self.stone = self.next_stone[:]

        self.shape_index = tetris_shapes.index(self.stone)

        self.next_stone = random.choice(tetris_shapes)

        self.stone_x = int(cols / 2 - len(self.stone[0]) / 2)
        self.stone_y = 0
        # self.evaluate += 1 TODO reward for stones?

        if check_collision(self.board,
                           self.stone,
                           (self.stone_x, self.stone_y)):
            self.gameover = True

    def init_game(self):
        self.board = new_board()
        self.new_stone()
        self.level = 1

        self.score = 0
        self.lines = 0
        if self.minimal_gui:
            pygame.time.set_timer(pygame.USEREVENT + 1, self.unitTime)

    def disp_msg(self, msg, topleft):
        x, y = topleft
        for line in msg.splitlines():
            self.screen.blit(
                self.default_font.render(
                    line,
                    False,
                    (255, 255, 255),
                    (0, 0, 0)),
                (x, y))
            y += 14

    def center_msg(self, msg):
        for i, line in enumerate(msg.splitlines()):
            msg_image = self.default_font.render(line, False,
                                                 (255, 255, 255), (0, 0, 0))

            msgim_center_x, msgim_center_y = msg_image.get_size()
            msgim_center_x //= 2
            msgim_center_y //= 2

            if self.minimal_gui:
                self.screen.blit(msg_image, (
                    self.width // 2 - msgim_center_x,
                    self.height // 2 - msgim_center_y + i * 22))

    def draw_matrix(self, matrix, offset):
        off_x, off_y = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(
                        self.screen,
                        colors[val],
                        pygame.Rect(
                            (off_x + x) *
                            cell_size,
                            (off_y + y) *
                            cell_size,
                            cell_size,
                            cell_size), 0)

    def add_cl_lines(self, n):
        linescores = [0, 40, 100, 300, 1200,9999,99,9,9,9,9,9,9]
        self.lines += n
        self.score += linescores[n] * self.level
        self.lines_cleared += n
        # todo self.evaluate += linescores[n] * self.level * 5

        if self.lines >= self.level * 6:
            self.level += 1
            newdelay = self.unitTime - self.unitTime/20 * (self.level - 1)
            newdelay = self.unitTime/10 if newdelay < self.unitTime/10 else newdelay
            if self.minimal_gui:
                pygame.time.set_timer(pygame.USEREVENT + 1, newdelay)
            else:
                pygame.time.set_timer(pygame.USEREVENT + 1, 0)

    def move(self, delta_x):
        if not self.gameover and not self.paused:
            new_x = self.stone_x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > cols - len(self.stone[0]):
                new_x = cols - len(self.stone[0])
            if not check_collision(self.board,
                                   self.stone,
                                   (new_x, self.stone_y)):
                self.stone_x = new_x

    def quit(self):
        if self.minimal_gui:
            self.center_msg("Exiting...")
            pygame.display.update()
        sys.exit()

    def drop(self, manual):
        if not self.gameover and not self.paused:
            self.score += 1 if manual else 0
            self.evaluate += 1 if manual else 0

            self.stone_y += 1
            if check_collision(self.board,
                               self.stone,
                               (self.stone_x, self.stone_y)):

                # TODO REMEMBER
                self.landed = True
                self.board = join_matrixes(
                    self.board,
                    self.stone,
                    (self.stone_x, self.stone_y))

                #self.evaluate_move()  # todo evaluate

                self.new_stone()
                cleared_rows = 0
                while True:
                    for i, row in enumerate(self.board[:-1]):
                        if 0 not in row:
                            self.board = remove_row(
                                self.board, i)
                            cleared_rows += 1
                            break
                    else:
                        break
                self.add_cl_lines(cleared_rows)
                return True
        return False

<<<<<<< HEAD
    def evaluate_move(self, board):
        return a*self.f_aggheight(board) + b*self.f_bumpiness(board) + c*self.f_holes(board) + d*self.f_rows(board)
=======
    def evaluate_move(self):
        self.evaluate += b*self.f_rows()
        #self.evaluate += a*self.f_aggheight() + b*self.f_rows() + c*self.f_holes() + d*self.f_bumpiness()
>>>>>>> origin/master

        """
        blocked = 0  # todo check can be too negative

        for i in range(len(self.stone[0])):
            j = self.stone_y + 1
            while j < 22 and self.board[j][i + self.stone_x] == 0:
                blocked += 1
                j += 1

        if blocked == 0:
            self.evaluate += self.stone_y
        else:
            self.evaluate -= blocked * self.stone_y / 10
        """

    def insta_drop(self):
        if not self.gameover and not self.paused:
            while (not self.drop(True)):
                pass

    def rotate_stone(self):
        self.evaluate+=0.01
        self.count_rotate += 1
        if not self.gameover and not self.paused:
            self.shape_rotate = (self.shape_rotate + 1) % 4
            new_stone = rotate_clockwise(self.stone)
            if not check_collision(self.board,
                                   new_stone,
                                   (self.stone_x, self.stone_y)):
                self.stone = new_stone

    def toggle_pause(self):
        self.paused = not self.paused

    def start_game(self):
        if self.gameover:
            self.init_game()
            self.gameover = False

    def run(self):
        key_actions = {
            'ESCAPE': self.quit,
            'LEFT': lambda: self.move(-1),
            'RIGHT': lambda: self.move(+1),
            'DOWN': lambda: self.drop(True),
            'UP': self.rotate_stone,
            'p': self.toggle_pause,
            'SPACE': self.start_game,
            'RETURN': self.insta_drop
        }

        self.gameover = False
        self.paused = False

        if self.minimal_gui:
            dont_burn_my_cpu = pygame.time.Clock()
        limit = 0

        while 1:

            if self.minimal_gui:
                self.screen.fill((0, 0, 0))
            if self.gameover or self.stone_count > self.game_limit:
                if self.minimal_gui:
                    self.center_msg("""Game Over!\nYour score: %d
    Press space to continue""" % self.score)

                #print  self.f_aggheight(), self.f_holes(), self.f_bumpiness()
                #print(self.f_bumpiness())
                self.evaluate_board()
                return self.evaluate + (a*self.f_aggheight() + c*self.f_holes()+ d*self.f_bumpiness())/float(self.stone_count)
                # self.evaluate_board()
<<<<<<< HEAD
                return self.evaluate
=======
>>>>>>> origin/master
            else:
                if self.paused:
                    if self.minimal_gui:
                        self.center_msg("Paused")
                else:
                    if self.minimal_gui:
                        pygame.draw.line(self.screen,
                                         (255, 255, 255),
                                         (self.rlim + 1, 0),
                                         (self.rlim + 1, self.height - 1))
                        self.disp_msg("Next:", (
                            self.rlim + cell_size,
                            2))
                        self.disp_msg("Score: %d\n\nLevel: %d\
    \nLines: %d" % (self.score, self.level, self.lines),
                                      (self.rlim + cell_size, cell_size * 5))
                        self.draw_matrix(self.bground_grid, (0, 0))
                        self.draw_matrix(self.board, (0, 0))
                        self.draw_matrix(self.stone,
                                         (self.stone_x, self.stone_y))
                        self.draw_matrix(self.next_stone,
                                         (cols + 1, 2))

            if self.minimal_gui:
                pygame.display.update()
                pygame.time.wait(self.unitTime)

            # self.get_board_with_piece(copy_board(self.board), self.stone, 0)

            # TODO here is where we will change the game

            if self.landed:
                #boardCopy = [[self.board[i][j] for j in xrange(len(self.board[0]))] for i in xrange(len(self.board))]
                #move = self.player_ai.play(join_matrixes(boardCopy, self.stone, (self.stone_x, self.stone_y)))
                #self.get_all_moves()
                #move = self.player_ai.play(self.board, self.shape_index, self.shape_rotate, self.stone_x, self.stone_y)
                assert len(self.board) == 23
                assert len(self.board[0]) == 10


                # dumb ai todo

                board_moves = self.get_all_moves()
                boards_scores = [self.evaluate_move(board_moves[i][0]) for i in xrange(len(board_moves))]
                boards = [board_moves[i][0] for i in xrange(len(board_moves))]

                #print [board_moves[i][0][10:] for i in xrange(len(board_moves))]

                bestMove = boards_scores.index(max(boards_scores))

                move = board_moves[bestMove][1:]
                print move
                while move[0] > self.stone_x:
                    key_actions["RIGHT"]()
                while move[0] < self.stone_x:
                    key_actions["LEFT"]()

                spins = move[1]
                while spins > 0 :
                    key_actions["UP"]()
                    spins -= 1
                self.landed = False

            ##if not self.minimal_gui:
            self.drop(False)

            """
            while limit < 2:
                move = self.player_ai.play(self.board, self.shape_index, self.shape_rotate, self.stone_x, self.stone_y)
                assert len(self.board) == 23
                assert len(self.board[0]) == 10
                if move != "NOTHING":
                    key_actions[move]()

                limit += 1

            self.drop(False)
            limit = 0

            """

            """
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    self.drop(False)
                    limit = 0

            #for event in pygame.event.get():
                #if event.type == pygame.USEREVENT + 1:
            self.drop(False)
            limit = 0

                elif event.type == pygame.QUIT:
                    self.quit()

                elif event.type == pygame.KEYDOWN:
                    for key in key_actions:
                        if event.key == eval("pygame.K_"
                                                     + key):
                            key_actions[key]()
                """

    def get_all_moves(self):

        all_boards = []
        for i in xrange(10):

            for j in xrange(4):
                self.rotate_stone()
                if i + len(self.stone[0]) < 10:
                    board = self.get_board_with_piece(copy_board(self.board), self.stone, i)
                    all_boards.append((board, i, j))

        return all_boards

    def get_board_with_piece(self, board, piece, x):
        depth = 0
        while not check_collision(board, piece, (x, depth)):
            depth += 1
        return join_matrixes(board, piece, (x,depth))


    def evaluate_board(self):
        for i in range(len(self.board) - 1):
            count = 0
            for bit in self.board[i]:
                if bit > 0:
                    count += 1
            self.evaluate += ((2.0 ** count) * i)/20000


    def get_max_length(self, line):
        current = 0
        m = 0
        for n in line:
            if n == 0:
                if current > m:
                    m = current
                current = 0
            else:
                current += 1
        if current > m:
            m = current
        return m