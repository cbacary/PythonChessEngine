import chess
import numpy

piece_values = {'P': 10, 'N': 30, 'B': 30, 'R': 50, 'Q': 90, 'K': 100, 'p': -10, 'n': -30, 'b': -30, 'r': -50, 'q': -90, 'k': -100}

class MoveTree:

    def __init__(self, board, isRoot = False, depth = 3):
        self.depth = depth
        self.child = []
        self.board = board

    def getMove(self, board, player):
        move_list = list(self.board.legal_moves)
        k = 0
        while True:
            if k >= len(move_list) - 1:
                break
            temp = chess.Board(self.board.fen())
            temp.push_san(str(move_list[k]))
            self.child.append(MoveTree(temp, depth=self.depth-1))
            if self.depth <= 0:
                return
            self.child[k].fillTree()
            k += 1

    def PrintTree(self):
        for i in self.child:
            i.PrintTree()
        print(self.board)
