
import chess
import numpy

# This is the way we evaluate the board, If the addition of all piecs on the board with these values is negative black is winning, vise versa
piece_values = {'P': 10, 'N': 30, 'B': 30, 'R': 50, 'Q': 90, 'K': 100, 'p': -10, 'n': -30, 'b': -30, 'r': -50, 'q': -90, 'k': -100}
searched = 0


def calculatePos(board, piece_values=piece_values):
    pieces = list(board.piece_map().values())

    eval = 0

    for i in pieces:
        eval += piece_values[str(i)]
    return eval

# simple minimax algorithm, no alpha-beta pruning yet.
def getMove(board, depth, player):
    global searched
    searched += 1
    if depth == 0 or board.is_game_over():
        if player:
            return int(calculatePos(board))
        else:
            return int(-1*calculatePos(board))

    # white
    if player:
        max = -numpy.Infinity
        move_list = list(board.legal_moves)
        for i, move in enumerate(move_list):

            # Create a separate board
            temp = chess.Board(board.fen())
            temp.push_san(str(move))

            # get the current value of board
            try:
                curr_eval, f = getMove(temp, depth-1, False)
            except:
                curr_eval = getMove(temp, depth-1, False)
            max = numpy.maximum(max, curr_eval)
        return max
    else:
        minimum = numpy.Infinity
        best_value_move = numpy.Infinity
        move_list = list(board.legal_moves)
        for i, move in enumerate(move_list):

            # Create a separate board
            temp = chess.Board(board.fen())
            temp.push_san(str(move))

            # get the current value of board
            curr_eval = getMove(temp, depth-1, True)
            minimum = numpy.minimum(minimum, curr_eval)

            # if the new min is less than min_move set min_move to min and set best_min to the current best move
            # because the new value of min is less than min_move it means it is the new best move.
            if minimum < best_value_move:
                best_value_move = minimum
                best_move = move

        return minimum, best_move

# def main():
#
#     board = chess.Board()
#
#     while not board.is_game_over():
#         print(board)
#         while True:
#             try:
#                 move = input("Move: ")
#                 board.push_san(move)
#             except:
#                 continue
#             break
#         val, ai = getMove(board, 3, False)
#         print(searched)
#         board.push(chess.Move.from_uci(str(ai)))


# def boardEval(board, piece_values=piece_values):
#     currEval = 0
#     pieces = list(board.piece_map().values())
#
#     for i in pieces:
#         currEval += piece_values[str(i)]
#         print(currEval)
#     return currEval
#
# def minimax(node, depth, maximizingPlayer = True):
#
#     # Base case
#     print(type(depth))
#     if depth == 0 or node.board.is_game_over():
#         if maximizingPlayer:
#             return boardEval(node.board), node.board
#         else:
#             return -1*boardEval(node.board), node.board
#max
#     # white
#     if maximizingPlayer:
#         value = -numpy.Infinity
#         bestEval = value
#         bestEvalMove = None
#         for i in node.child:
#             value, f = max(value, minimax(i, depth - 1, maximizingPlayer=True))
#             print("as")
#             if value > bestEval:
#                 bestEval = value
#                 bestEvalMove = f
#         return bestEval, bestEvalMove
#     # black
#     else:
#         value = numpy.Infinity
#         bestEval = value
#         bestEvalMove = None
#         for i in node.child:
#             value, f = min(value, minimax(i, depth - 1, maximizingPlayer=True))
#             print("as")
#             if value < bestEval:
#                 bestEval = value
#                 bestEvalMove = f
#         return bestEval, bestEvalMove
