
import chess
import numpy

# This is the way we evaluate the board, If the addition of all piecs on the board with these values is negative black is winning, vise versa
piece_values = {'P': 10, 'N': 35, 'B': 35, 'R': 52.5, 'Q': 100, 'K': 1000, 'p': -10, 'n': -35, 'b': -35, 'r': -52.5, 'q': -100, 'k': -1000}
searched = 0

# Found this great stackoverflow question with position evaluations for each piece along with the piece_values, which I editted
# a bit according to https://en.wikipedia.org/wiki/Chess_piece_relative_value
# here is the stackoverflow question: https://stackoverflow.com/questions/59039152/python-chess-minimax-algorithm-how-to-play-with-black-pieces-bot-has-white

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

# this function was also obtained from the same stackoverflow question
def calculatePos(board, piece_values=piece_values, position_values = position_values):

    pieces = board.piece_map()
    eval = 0

    for i in pieces:
        # eval += piece_values[str(i)]
        file = chess.square_file(i)
        rank = chess.square_rank(i)

        piece_type = str(pieces[i])
        positionArray = position_values[piece_type.upper()]

        if piece_type.isupper():
            flippedPositionArray = numpy.flip(positionArray, axis=0)
            eval += piece_values[piece_type] + flippedPositionArray[rank, file]

        else:
            eval += piece_values[piece_type] - positionArray[rank, file]


    return eval

# simple minimax algorithm with alpha beta pruning. The useAlphaBeta is mainly there for testing purposes.
def getMove(board, depth, initialDepth, player, useAlphaBeta, alpha, beta):
    global searched
    searched += 1
    # base case, if depth = or the node is a terminal node aka game is over
    if depth == 0 or board.is_game_over():
        if player:
            if board.is_checkmate():
                if board.is_stalemate():
                    return 0
                return -numpy.Infinity
            return int(calculatePos(board))
        else:
            if board.is_checkmate():
                if board.is_stalemate():
                    return 0
                return numpy.Infinity
            return int(-calculatePos(board))

    # white
    best_move = None
    if player:
        max = -numpy.Infinity
        best_value_move = -numpy.Infinity
        move_list = list(board.generate_legal_moves())
        for move in move_list:

            # Create a separate board
            temp = chess.Board(board.fen())
            temp.push_san(str(move))

            # get the current value of board
            curr_eval = getMove(temp, depth-1, initialDepth, False, useAlphaBeta, alpha, beta)
            max = numpy.maximum(max, curr_eval)

            if useAlphaBeta:

                alpha = numpy.maximum(alpha, max)

                if alpha >= beta:
                    break

            if max > best_value_move:
                best_value_move = max
                best_move = (str(move))

        if depth < initialDepth:
            return max
    else:
        minimum = numpy.Infinity
        best_value_move = numpy.Infinity
        move_list = list(board.legal_moves)
        for move in move_list:
            # Create a separate board
            temp = chess.Board(board.fen())
            temp.push_san(str(move))

            # get the current value of board
            curr_eval = getMove(temp, depth-1, initialDepth, True, useAlphaBeta, alpha, beta)
            minimum = numpy.minimum(minimum, curr_eval)

            if useAlphaBeta:

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
    return best_move
