import player
import random

pieces = ["I","J","L","O","S","T","Z"]

nextPiece = True

#TODO remove
board = [[0 for j in xrange(12)] for i in xrange(20)]


def newPiece():
    piece = pieces[random.randint(0,6)]
    if piece == "I":
        board[0][4] = 1
        board[0][5] = 1
        board[0][6] = 1
        board[0][7] = 1
    if piece == "J":
        board[0][4] = 1
        board[0][5] = 1
        board[0][6] = 1
        board[1][4] = 1
    # TODO continue

def update():
    if nextPiece:
        newPiece()

    move = player.play(board)
    if move == "L":
        moveLeft():



def getBoard():

    move = player.play(board)
