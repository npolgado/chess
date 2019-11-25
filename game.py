import pygame
import numpy as np

NUM_BLOCKS = 30
SQ_SZ = 25

GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

BLUEGREEN = (71,255,207)
BLUEGREEN_shaded = (60, 174, 144)
BLACK = (0, 0, 0)
shd = 32
BLACK_shaded = (shd, shd, shd)


PIECES = {
    0: 'Empty',    1: 'Pawn',
    2: 'Bishop',    3: 'Knight',
    5: 'Rook',    6: 'King',
    9: 'Queen'
}

# TODO: make object that contains [piece, color, position] and maybe [alive/dead, path to image]

BOARD = [[5, 2, 3, 9, 6, 3, 2, 5],
         [1]*8, [0]*8, [0]*8, [0,0,0,0,2,0,0,0], [0]*8, [1]*8,
         [5, 2, 3, 9, 6, 3, 2, 5]]

side = SQ_SZ * NUM_BLOCKS
size = (side, side)

def get_valid_moves (p, x, y):

    moves = []

    # KNIGHT
    if (p == 'Knight'):
        a = [-2, -2, -1, -1, 1, 1, 2, 2]    # x vectors
        b = [-1, 1, -2, 2, -2, 2, -1, 1]    # y vectors
        for i in range (0, len(a)):
            if (x + a[i] < 8 and x + a[i] >= 0):
                if (y + b[i] < 8 and y + b[i] >= 0):
                    moves.append((x+a[i], y+b[i]))

        # TODO: remove squares with friendly pieces on them. (REQ: must have access to the pieces color)

    if (p == "Bishop"):
        a = [j for j in range(-4, 5) if j is not 0]  # x vectors
        b = [j for j in range(-4, 5) if j is not 0]  # y vectors

        for i in range(0, len(a)):
            if (x + a[i] < 8 and x + a[i] >= 0):
                if (y + b[i] < 8 and y + b[i] >= 0):
                    moves.append((x + a[i], y + b[i]))

            # Problem: bishops need (x-4, y-4), (x-3, y-3), and (x-4, y+4), (x-3, y+3). This takes case
            #       second case, so array is only half as long as valids.
            if (x + a[i] < 8 and x + a[i] >= 0):
                if (y - b[i] < 8 and y - b[i] >= 0):
                    moves.append((x + a[i], y - b[i]))

        # TODO: remove squares with friendly pieces on them (AND ANYTHING PASSED THEM FOR BISHOPS, QUEENS,
        #       and ROOKS, special case for pawns). (REQ: must have access to the pieces color)

    '''Given a piece and location (ex: rook (4, 5), return a list of valid moves'''
    return moves
def is_check():
    '''Checks to see if the gamestate is in check/checkmate, and flags'''
    pass

def init():
    global screen
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption('Chess')
    screen.fill(WHITE)

def draw_board(valid_moves = None):
    global BOARD, screen
    pygame.font.init()  # you have to call this at the start,

    a = 8
    for i in range (a):
        for j in range(a):
            len = (side/a)
            if (i+j) % 2 == 0:
                if (valid_moves is not None and (j, i) in valid_moves):
                    pygame.draw.rect(screen, BLUEGREEN_shaded, (i * len, j * len, len - 1, len - 1))
                else:
                    pygame.draw.rect(screen, BLUEGREEN, (i*len, j*len , len-1, len-1))
            else:
                if (valid_moves is not None and (j, i) in valid_moves):
                    pygame.draw.rect(screen, BLACK_shaded, (i * len, j * len, len - 1, len - 1))
                else:
                    pygame.draw.rect(screen, BLACK, (i*len, j*len , len-1, len-1))

            myfont = pygame.font.SysFont('Comic Sans MS', 50)
            textsurface = myfont.render(str(BOARD[j][i]), False, BLUE)
            screen.blit(textsurface, (i*len, j*len))

    pygame.display.update()

    # # if you want to use this module.
    # myfont = pygame.font.SysFont('Comic Sans MS', 15)
    # textsurface = myfont.render('SCORE: ' + str(score), False, BLACK)
    # textsurface2 = myfont.render('HI:    ' + str(hiScore), False, BLACK)  # 'HI:    '+ str(hiScore)
    # screen.blit(textsurface, (side - 100, 10))
    # screen.blit(textsurface2, (side - 100, 30))

if __name__ == '__main__':
    init()
    draw_board()
    pygame.display.flip()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                y = int(pos[0] / (side/8))
                x = int(pos[1] / (side/8))

                # coorLet = chr(y + 65)
                # coorNum = 8-x
                piece = PIECES[BOARD[x][y]];


                print ("Loc: ({}, {})   = {}".format(x, y, piece))


                # Click a piece, and it shows valid moves
                # Working:
                # In progress:   knight
                valids = get_valid_moves (piece, x, y)
                draw_board(valids)
                print ("Valid Moves: ", end = " ")
                for i in range (0, len(valids)):
                    print (valids[i], end = ", ")
                print()

            if event.type == pygame.QUIT:
                running = False

        '''GAME LOGIC'''
        #Player 1's Turn
        #Is Check? (Check for Checkmate or Check)
        #Player 2's Turn
        #Is Check? (Check for Checkmate or Check or not escaped previous Check)
        #Repeat ^^