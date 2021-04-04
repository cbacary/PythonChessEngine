from save_thread_result import ThreadWithResult
import threading
import os
import chess
import numpy
import time
import sys
from functools import cache


# This is the way we evaluate the board, If the addition of all piecs on the board with these values is negative black is winning, vise versa
piece_values = {'P': 10, 'N': 35, 'B': 35, 'R': 52.5, 'Q': 100, 'K': 1000, 'p': -10, 'n': -35, 'b': -35, 'r': -52.5, 'q': -100, 'k': -1000}
searched = 0
timeCalcPos = 0.0
known_piece_map_list = []

# Found this great stackoverflow question with position evaluations for each piece along with the piece_values, which I editted
# a bit according to https://en.wikipedia.org/wiki/Chess_piece_relative_value
# here is the stackoverflow question: https://stackoverflow.com/questions/59039152/python-chess-minimax-algorithm-how-to-play-with-black-pieces-bot-has-white

infinity = 99999999

position_values = {
        'P' : numpy.array([ [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
                        [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
                        [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
                        [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
                        [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
                        [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
                        [0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5],
                        [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0] ]),

        'N' : numpy.array([[-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
                       [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
                       [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
                       [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
                       [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
                       [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
                       [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
                       [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0] ]),

        'B' : numpy.array([[-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
                       [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
                       [-1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
                       [-1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
                       [-1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
                       [-1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
                       [-1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
                       [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0] ]),

        'R' : numpy.array([[ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  0.0],
                       [ 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,  0.5],
                       [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                       [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                       [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                       [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                       [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                       [ 0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0,  0.0]]),

        'Q' : numpy.array([[-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
                       [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
                       [-1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
                       [-0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
                       [-0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
                       [-1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
                       [-1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
                       [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]]),

        'K' : numpy.array([[ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                       [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                       [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                       [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                       [ -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
                       [ -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
                       [  2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0 ],
                       [  2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0 ]])}
flipped_pos_vales = {}



# this function was also obtained from the same stackoverflow question
def calculatePos(board, piece_values=piece_values, position_values = position_values, infinity=infinity):
    global timeCalcPos


    # 1/7th of time it takes to generate a move is this board.piece_map() function
    pieces = board.piece_map()
    eval = 0

    for i in pieces:
        # eval += piece_values[str(i)]
        file = chess.square_file(i)
        rank = chess.square_rank(i)
        
        piece_type = str(pieces[i])

        if piece_type.isupper():
            start_time = time.time()
            tempArr = flipped_pos_vales[piece_type.upper()]
            eval += piece_values[piece_type] + tempArr[rank, file]
            timeCalcPos += (time.time() - start_time)

        else:
            start_time = time.time()
            positionArray = position_values[piece_type.upper()]
            eval += piece_values[piece_type] - positionArray[rank, file]
            timeCalcPos += (time.time() - start_time)

    return eval


## Curently scrapped idea, not really optimised for alpha beta pruning and minimax search. Keeping it in here just in case I ever come back to it.
def GetMoveWithThreading(board, depth, initialDepth, player, useAlphaBeta, color, alpha, beta):
    threads = []
    move_list = list(board.generate_legal_moves())
    for i in move_list:

        # Generate new instance of board
        temp = chess.Board(board.fen())
        temp.push_san(str(i))

        # thread = threading.Thread(target=lambda q, arg1: q.put(getMove(arg1)), args=(que, temp, depth - 1, initialDepth, tempPlayer, useAlphaBeta, color, alpha, beta))

        thread = ThreadWithResult(target=getMove, args=(temp, depth - 1, initialDepth, not player, useAlphaBeta, color, alpha, beta, True, ))
        print("a")
        thread.start()
        threads.append([thread, str(i)])

    for i in range(len(threads)):
        threads[i][0].join()

    best_move = threads[0][1]
    best_move_numerical = threads[0][0].result
    for index, tuple in enumerate(threads):
        if tuple[0].result > best_move_numerical:
            best_move_numerical = tuple[0].result
            best_move = tuple[1]
    return best_move


# simple minimax algorithm with alpha beta pruning. The useAlphaBeta is mainly there for testing purposes.
def getMove(board, depth, initialDepth, player, useAlphaBeta, color, alpha, beta):
    global searched
    global timeCalcPos
    searched += 1

    # base case, if depth = 0 or the node is a terminal node aka game is over
    if depth == 0 or board.is_game_over():
        if color == 'WHITE':
            if board.is_checkmate():
                return -infinity
            if board.is_stalemate():
                return 0
            # start_time = time.time()
            f = calculatePos(board)
            # timeCalcPos += (time.time() - start_time)
            return f
        elif color == 'BLACK':
            if board.is_checkmate():
                return infinity
            if board.is_stalemate():
                return 0
            # start_time = time.time()
            f = -calculatePos(board)
            # timeCalcPos += (time.time() - start_time)
            return f
    # Black
    best_move = None
    if player:
        max = -infinity
        best_value_move = -infinity
        move_list = list(board.generate_legal_moves())
        for move in move_list:
            # Create a separate board
            temp = chess.Board(board.fen())
            temp.push_san(str(move))

            # get the current value of board
            curr_eval = getMove(temp, depth-1, initialDepth, False, useAlphaBeta, color, alpha, beta)
            max = numpy.maximum(max, curr_eval)


            # Alpha-beta pruning pseudo code can be found at https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
            if useAlphaBeta and max != infinity:

                alpha = numpy.maximum(alpha, max)

                if alpha >= beta:
                    break

            if max > best_value_move:
                best_value_move = max
                best_move = (str(move))

        if depth < initialDepth:
            return max
    # White
    else:
        minimum = infinity
        best_value_move = infinity
        move_list = list(board.generate_legal_moves())
        for move in move_list:
            # Create a separate board
            temp = chess.Board(board.fen())
            temp.push_san(str(move))

            # get the current value of board
            curr_eval = getMove(temp, depth-1, initialDepth, True, useAlphaBeta, color, alpha, beta)
            minimum = numpy.minimum(minimum, curr_eval)

            # Alpha-beta pruning pseudo code can be found at https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
            if useAlphaBeta and minimum != -infinity:

                beta = numpy.minimum(beta, minimum)

                if beta <= alpha:
                    break

            # if the new min is less than min_move set min_move to min and set best_min to the current best move
            # because the new value of min is less than min_move it means it is the new best move.
            if minimum < best_value_move:
                best_value_move = minimum
                best_move = str(move)

        if depth < initialDepth:
            return minimum
    # If checkmate is the only move available best_move will never be set so just return the first legal move
    if best_move == None:
        print("forced mate on every search or something went wrong")
        return list(board.generate_legal_moves())[0]
    print(f"Time spent calculating evaluation: {timeCalcPos}")
    return best_move

if __name__ != '__main__':
    for i in position_values:
        flipped_pos_vales[i] = numpy.flip(position_values[i], axis=0)