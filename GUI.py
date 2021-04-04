import sys, pygame, numpy, os
import chess
import Squares
import chessbrain
import time

def main():
    pygame.init()

    screen = pygame.display.set_mode((848, 848))
    pygame.display.set_caption("Chess")
    #Size of squares
    size = 106

    white  = (255, 255, 255)
    black = (161, 96, 43)

    board = chess.Board()
    board_squares = chess.SquareSet()
    squares = []
    # method for drawing chess board obtained from stack overflow, link lost somewhere in history
    count = 0
    # this fen has no slashes, you must remove slashes for any fen to work, you also must remove the ending material that says "3 - 0" or something
    startingFen = 'rnbkqbnrpppppppp8888PPPPPPPPRNBKQBNR'
    fenCount = len(startingFen)- 1
    for i in range(8):
        for j in range(8):
            if count % 2 == 0:
                # rectangle = pygame.rect.Rect(size*j,size*i,size,size)
                rectangle = pygame.draw.rect(screen, white, (size*j,size*i,size,size))
                if startingFen[fenCount].isdigit() and int(startingFen[fenCount]) > 0:
                    squares.append(Squares.Squares(chr((j + 97)) + str(int(8 - i)), "", rectangle, False))
                    f = str(int(startingFen[fenCount]) - 1)
                    startingFen = startingFen[:fenCount] + f + startingFen[fenCount + 1:]
                    if int(startingFen[fenCount]) == 0:
                        fenCount -= 1
                else:
                    squares.append(Squares.Squares(chr((j + 97)) + str(int(8 - i)), startingFen[fenCount], rectangle, False))
                    pieceImg = squares[len(squares) - 1].image
                    screen.blit(pieceImg, (size*j, size*i))
                    fenCount -= 1
            else:
                rectangle = pygame.draw.rect(screen, white, (size*j,size*i,size,size))
                # rectangle = pygame.rect.Rect(size*j,size*i,size,size)
                if startingFen[fenCount].isdigit() and int(startingFen[fenCount]) > 0:
                    squares.append(Squares.Squares(chr((j + 97)) + str(int(8 - i)), "", rectangle, False))
                    f = str(int(startingFen[fenCount]) - 1)
                    startingFen = startingFen[:fenCount] + f + startingFen[fenCount + 1:]
                    if int(startingFen[fenCount]) == 0:
                        fenCount -= 1
                else:
                    squares.append(Squares.Squares(chr((j + 97)) + str(int(8 - i)), startingFen[fenCount], rectangle, False))
                    pieceImg = squares[len(squares) - 1].image
                    screen.blit(pieceImg, (size*j, size*i))
                    fenCount -= 1
            count +=1
        count-=1

    movedThing = None
    x, y = 0, 0
    while True:
        screen = drawBoard(screen, squares)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i in squares:
                        if i.rectangle.collidepoint(event.pos) and i.image != None:
                            i.dragging = True
                            mouse_x, mouse_y = event.pos
                            offset_x = i.posx - mouse_x
                            offset_y = i.posy - mouse_y
                            x, y = event.pos[0], event.pos[1]


            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                for i in range(len(squares)):
                    if squares[i].dragging:
                        squares[i].dragging = False
                        print(event.pos)
                        for x in range(len(squares)):
                            if squares[x].rectangle.collidepoint(event.pos) and squares[x] != squares[i]:

                                # We use a try except because it will raise ValueError on illegal move or on Game Over
                                try:

                                    print(squares[i].pos + squares[x].pos)

                                    playHumanMove(board, squares, i, x)

                                    playAIMove(board, squares)

                                except (ValueError, TypeError, NameError) as e:
                                    if board.is_game_over() or board.is_stalemate():
                                        print("Game Over!")
                                    else:
                                        print("Invalid Move. \n{0}".format(e))

            elif event.type == pygame.MOUSEMOTION:
                for i in squares:
                    if i.image == None:
                        continue
                    if i.dragging:
                        mouse_x, mouse_y = event.pos
                        x = mouse_x + offset_x
                        y = mouse_y + offset_y
                        screen.blit(i.image, (x, y))

        # place the piece that is currently being moved.
        for i in squares:
            if i.dragging:
                screen.blit(i.image, (x, y))
        # loop through squares and place each piece accordingly each update.
        pygame.display.update()

def checkCastle(board, squares, move):
    try:
        # King side white castle
        if move == 'e1g1':
            found = False
            print('castled')
            for rook in squares:
                if rook.pos == 'h1':
                    for f1 in squares:
                        if f1.pos == 'f1' and rook.piece == 'r':
                            f1.image = rook.image
                            rook.image = None
                            found = True
                if found:
                    break
        # Queen side white castle
        if move == 'e1c1':
            found = False
            print('castled')
            for rook in squares:
                if rook.pos == 'a1' and rook.piece == 'r':
                    for d1 in squares:
                        if d1.pos == 'd1':
                            d1.image = rook.image
                            rook.image = None
                            found = True
                if found:
                    break
        # Queen side black castle
        if move == 'e8c8':
            found = False
            print('castled')
            for rook in squares:
                if rook.pos == 'a8' and rook.piece == 'R':
                    for d1 in squares:
                        if d1.pos == 'd8':
                            d1.image = rook.image
                            rook.image = None
                            found = True
                if found:
                    break
        # King side black castle
        if move == 'e8g8':
            found = False
            print('castled')
            for rook in squares:
                if rook.pos == 'h8' and rook.piece == 'R':
                    for f8 in squares:
                        if f8.pos == 'f8':
                            f8.image = rook.image
                            rook.image = None
                            found = True
                if found:
                    break
    except:
        pass
    return squares

def drawBoard(screen, squares):
    white  = (255, 255, 255)
    black = (161, 96, 43)
    index = 0
    count = 0
    for i in range(8):
        for j in range(8):
            if count % 2 == 0:
                pygame.draw.rect(screen, white, squares[index].rectangle)
                if squares[index].image != None and squares[index].dragging == False:
                    screen.blit(squares[index].image, (squares[index].posx, squares[index].posy))
            else:
                pygame.draw.rect(screen, black, squares[index].rectangle)
                if squares[index].image != None and squares[index].dragging == False:
                    screen.blit(squares[index].image, (squares[index].posx, squares[index].posy))
            index += 1
            count += 1
        count -= 1
    return screen

def playAIMove(board, squares):

    start_time = time.time()
    move = chessbrain.getMove(board, 3, 3, True, True, 'BLACK', -numpy.Infinity, numpy.Infinity)
    print(move, chessbrain.searched, str(time.time() - start_time))
    chessbrain.searched = 0
    # chessbrain.searched = 0

    # Check if castle
    squares = checkCastle(board, squares, str(move))

    board.push(chess.Move.from_uci(str(move)))

    if str(move)[len(move) - 1] == 'q':
        found = False
        for pos in squares:
            for newPos in squares:
                f = str(pos.pos + newPos.pos + 'q')
                if f == str(move):
                    newPos.redoImg('Q')
                    pos.image = None
                    found = True
                    break
            if found:
                break
    else:
        found = False
        for pos in squares:
            for newPos in squares:
                f = str(pos.pos + newPos.pos)
                if f == str(move):
                    newPos.image = pos.image
                    pos.image = None
                    found = True
                    break
            if found:
                break

def playHumanMove(board, squares, i, x):

    squares = checkCastle(board, squares, squares[i].pos + squares[x].pos)

    # Check to make sure is legal move using generate_legal_moves not legal_moves.
    if chess.Move.from_uci(squares[i].pos + squares[x].pos + 'q') in list(board.generate_legal_moves()):

        print("Promotion!")

        # Have to move the piece using from_uci otherwise library does not recongnize as legal
        board.push(chess.Move.from_uci(squares[i].pos + squares[x].pos + 'q'))

        # Reset the image variable to new correct image
        squares[x].redoImg('q')
        squares[i].image = None

    else:
        board.push_san(squares[i].pos + squares[x].pos)
        squares[x].image = squares[i].image
        squares[i].image = None

main()
