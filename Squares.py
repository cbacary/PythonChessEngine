import sys, pygame

class Squares:

    def __init__(self, pos, piece, rectangle, dragging):
        self.pos = pos
        self.piece = piece
        self.dragging = dragging
        self.rectangle = rectangle
        self.posx = rectangle.x
        self.posy = rectangle.y

        if piece != "":
            # self.piece = piece.lower() if piece.isupper() else piece.upper()
            self.piece = piece
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

    def redoImg(self, piece):
        self.piece = piece
        if self.piece.islower():
            self.image = pygame.image.load('/home/cbac/Desktop/prgTHINGS/PythonThings/ChessEngine/Pieces/White Pieces/' + self.piece + ".png")
            width, height = self.image.get_size()
            self.image = pygame.transform.scale(self.image, (int(width / 3) , int(height / 3 )))
        else:
            self.image = pygame.image.load('/home/cbac/Desktop/prgTHINGS/PythonThings/ChessEngine/Pieces/Black Pieces/' + self.piece + ".png")
            width, height = self.image.get_size()
            self.image = pygame.transform.scale(self.image, (int(width / 3) , int(height / 3 )))
