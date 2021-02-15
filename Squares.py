import sys, pygame

class Squares:

    def __init__(self, pos, piece):
        self.pos = pos
        self.piece = piece


        if piece != "":
            self.piece = piece.lower() if piece.isupper() else piece.upper()
            if piece.islower():
                self.image = pygame.image.load('/home/cbac/Desktop/prgTHINGS/PythonThings/ChessEngine/Pieces/White Pieces/' + piece + ".png")
                width, height = self.image.get_size()
                self.image = pygame.transform.scale(self.image, (int(width / 3) , int(height / 3 )))
            else:
                self.image = pygame.image.load('/home/cbac/Desktop/prgTHINGS/PythonThings/ChessEngine/Pieces/Black Pieces/' + piece + ".png")
                width, height = self.image.get_size()
                self.image = pygame.transform.scale(self.image, (int(width / 3) , int(height / 3 )))
        else:
            self.image = None
