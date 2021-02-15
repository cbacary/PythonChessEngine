import sys, pygame
import Squares

def main():
    pygame.init()

    screen = pygame.display.set_mode((848, 848))
    pygame.display.set_caption("Chess")
    #Size of squares
    size = 106

    white  = (255, 255, 255)
    black = (161, 96, 43)

    squares = []
    # method for drawing chess board obtained from stack overflow, link lost somewhere in history
    count = 0
    # this fen has no slashes, you must remove slashes for any fen to work, most fen's  probably won't work tho.
    startingFen = 'rnbqkbnrpppppppp8888PPPPPPPPRNBQKBNR'
    fenCount = len(startingFen) - 1
    for i in range(8):
        for j in range(8):
            if count % 2 == 0:
                print(startingFen[fenCount], fenCount)
                pygame.draw.rect(screen, white,[size*j,size*i,size,size])
                if startingFen[fenCount].isdigit() and int(startingFen[fenCount]) > 0:
                    squares.append(Squares.Squares(str(i + 97) + str(int(j + 1)), ""))
                    f = str(int(startingFen[fenCount]) - 1)
                    startingFen = startingFen[:fenCount] + f + startingFen[fenCount + 1:]
                    if int(startingFen[fenCount]) == 0:
                        fenCount -= 1
                else:
                    squares.append(Squares.Squares(str(i + 97) + str(int(j + 1)), startingFen[fenCount]))
                    pieceImg = squares[len(squares) - 1].image
                    screen.blit(pieceImg, (size*j, size*i))
                    fenCount -= 1
            else:
                print(startingFen[fenCount], fenCount)
                pygame.draw.rect(screen, black, [size*j,size*i,size,size])
                if startingFen[fenCount].isdigit() and int(startingFen[fenCount]) > 0:
                    squares.append(Squares.Squares(str(i + 97) + str(int(j + 1)), ""))
                    f = str(int(startingFen[fenCount]) - 1)
                    startingFen = startingFen[:fenCount] + f + startingFen[fenCount + 1:]
                    if int(startingFen[fenCount]) == 0:
                        fenCount -= 1
                else:
                    squares.append(Squares.Squares(str(i + 97) + str(int(j + 1)), startingFen[fenCount]))
                    pieceImg = squares[len(squares) - 1].image
                    screen.blit(pieceImg, (size*j, size*i))
                    fenCount -= 1
            count +=1
        count-=1


    while True:
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

main()
