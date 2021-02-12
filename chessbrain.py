import chess
import numpy
from MoveTree import MoveTree

piece_values = {'P': 10, 'N': 30, 'B': 30, 'R': 50, 'Q': 90, 'K': 100, 'p': -10, 'n': -30, 'b': -30, 'r': -50, 'q': -90, 'k': -100}


def main():

    board = chess.Board()

    while not board.is_game_over():
        print(board)
        move = input("Move: ")
        board.push_san(move)
        ai = MoveTree(board)
        ai.fillTree()
        eval, aiMove = minimax(ai, 3, maximizingPlayer=False)
        board.push(aiMove)

def boardEval(board, piece_values=piece_values):
    currEval = 0
    pieces = list(board.piece_map().values())

    for i in pieces:
        currEval += piece_values[str(i)]
        print(currEval)
    return currEval

def minimax(node, depth, maximizingPlayer = True):

    # Base case
    print(type(depth))
    if depth == 0 or node.board.is_game_over():
        if maximizingPlayer:
            return boardEval(node.board), node.board
        else:
            return -1*boardEval(node.board), node.board

    # white
    if maximizingPlayer:
        value = -numpy.Infinity
        bestEval = value
        bestEvalMove = None
        for i in node.child:
            value, f = max(value, minimax(i, depth - 1, maximizingPlayer=True))
            print("as")
            if value > bestEval:
                bestEval = value
                bestEvalMove = f
        return bestEval, bestEvalMove
    # black
    else:
        value = numpy.Infinity
        bestEval = value
        bestEvalMove = None
        for i in node.child:
            value, f = min(value, minimax(i, depth - 1, maximizingPlayer=True))
            print("as")
            if value < bestEval:
                bestEval = value
                bestEvalMove = f
        return bestEval, bestEvalMove

main()
