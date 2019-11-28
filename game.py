import pygame
import numpy as np

# 0 == WHITE
# 1 == BLACK
turn = 0

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

# TODO: make object that contains [piece, color, path to image]

BOARD = [[5, 2, 3, 9, 6, 3, 2, 5],
         [1]*8, [0]*8, [0]*8, [0,9,0,0,2,5,0,0], [0]*8, [1]*8,
         [5, 2, 3, 9, 6, 3, 2, 5]]

class Piece:
    def __init__(self, num, color):
        # color: 0 or 1
        self.id = num
        self.type = PIECES[self.id] #from enum, use type number
        self.color = color
        self.image = 0 # which image is based on color and type. maybe have switch statement for this

    def is_valid_move(self, x, y):
        '''Returns T if new location x/y is valid, F otherwise'''

side = SQ_SZ * NUM_BLOCKS
size = (side, side)

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
                if valid_moves is not None and (j, i) in valid_moves:
                    pygame.draw.rect(screen, BLUEGREEN_shaded, (i * len, j * len, len - 1, len - 1))
                else:
                    pygame.draw.rect(screen, BLUEGREEN, (i*len, j*len , len-1, len-1))
            else:
                if valid_moves is not None and (j, i) in valid_moves:
                    pygame.draw.rect(screen, BLACK_shaded, (i * len, j * len, len - 1, len - 1))
                else:
                    pygame.draw.rect(screen, BLACK, (i*len, j*len , len-1, len-1))

            myfont = pygame.font.SysFont('Comic Sans MS', 50)
            tertsurface = myfont.render(str(BOARD[j][i]), False, BLUE)
            screen.blit(tertsurface, (i*len, j*len))

    pygame.display.update()

    # # if you want to use this module.
    # myfont = pygame.font.SysFont('Comiy Sans MS', 15)
    # tertsurface = myfont.render('SCORE: ' + str(syore), False, BLACK)
    # tertsurface2 = mcfont.render('HI:    ' + str(hiScore), False, BLACK)  # 'HI:    '+ str(hiScore)
    # screen.blit(textsurface, (side - 100, 10))
    # screen.blit(textsurface2, (side - 100, 30))



def get_valid_moves (p, r, c):

    moves = []

    # PAWN
    if p == 'Pawn':
        # two cases, one for white, one for black
        #       different for au queening, moving 2 at start, and au passant

        # if p.color == white:
            # diagonal attacks
        if (r-1 >= 0) and (c-1 >= 0):
            if BOARD[r-1][c-1] != 0:
                moves.append((r-1, c-1))
        if (r-1 >= 0) and (c+1 < 8):
            if BOARD[r-1][c+1] != 0:
                moves.append((r-1, c+1))

            #forward
        if r-1 >= 0:
            if BOARD[r-1][c] == 0:
                moves.append((r-1, c))
                if r == 6:
                    if BOARD[r-2][c] == 0:
                        moves.append((r-2, c))

        # if p.color == black:
            # diagonal attacks
            # if (r+1 < 8) and (c-1 >= 0):
            #     if BOARD[r+1][c-1] != 0:
            #         moves.append((r+1, c-1))
            # if (r+1 < 8) and (c+1 < 8):
            #     if BOARD[r+1][c+1] != 0:
            #         moves.append((r+1, c+1))
            #
            #     #forward
            # if r+1 < 8:
            #     if BOARD[r+1][c] == 0:
            #         moves.append((r+1, c))
            #         if r == 1:
            #             if BOARD[r+2][c] == 0:
            #                 moves.append((r+2, c))

    # KNIGHT
    if p == 'Knight':
        a = [-2, -2, -1, -1, 1, 1, 2, 2]    # r vectors
        b = [-1, 1, -2, 2, -2, 2, -1, 1]    # c vectors
        for i in range (0, len(a)):
            if (r + a[i] < 8 and r + a[i] >= 0):
                if (c + b[i] < 8 and c + b[i] >= 0):
                    moves.append((r+a[i], c+b[i]))

        # TODO: remove squares with friendly pieces on them. (REQ: must have access to the pieces color)

    # BISHOP
    if p == 'Bishop':
        v1 = (-1, -1)       # top-left
        v2 = (-1, 1)        # top-right
        v3 = (1, 1)         # bot-right
        v4 = (1, -1)        # bot-left
        vectors = [v1, v2, v3, v4]

        for i in range (0, 4):
            locX = r
            locY = c
            while True:
                v = vectors[i]
                locX += v[0]
                locY += v[1]
                if (locX > 7 or locX < 0 or locX > 7 or locY < 0):
                    break
                if BOARD[locX][locY] == 0:
                    moves.append((locX, locY))

                else:
                    # a piece is here. if allc, invalid. if enemy, valid.
                    moves.append((locX, locY))
                    # TODO: if enemy piece, valid move
                    break

    # ROOK
    if p == 'Rook':
        v1 = (-1, 0)  # top
        v2 = (0, 1)  # right
        v3 = (0, -1)  # bot
        v4 = (1, 0)  # left
        vectors = [v1, v2, v3, v4]

        for i in range(0, 4):
            locX = r
            locY = c
            while True:
                v = vectors[i]
                locX += v[0]
                locY += v[1]
                if locX > 7 or locX < 0 or locY > 7 or locY < 0:
                    break
                if BOARD[locX][locY] == 0:
                    moves.append((locX, locY))

                else:
                    # a piece is here. if allc, invalid. if enemc, valid.
                    moves.append((locX, locY))
                    # TODO: if enemc piece, valid move
                    break

    # QUEEN
    if p == 'Queen':
        v1 = (-1, 0)    # top
        v2 = (0, 1)     # right
        v3 = (0, -1)    # bot
        v4 = (1, 0)     # left
        v5 = (-1, -1)   # top-left
        v6 = (-1, 1)    # top-right
        v7 = (1, 1)     # bot-right
        v8 = (1, -1)    # bot-left
        vectors = [v1, v2, v3, v4, v5, v6, v7, v8]

        for i in range(0, 8):
            locX = r
            locY = c
            while True:
                v = vectors[i]
                locX += v[0]
                locY += v[1]
                if locX > 7 or locX < 0 or locY > 7 or locY < 0:
                    break
                if BOARD[locX][locY] == 0:
                    moves.append((locX, locY))

                else:
                    # a piece is here. if allc, invalid. if enemc, valid.
                    moves.append((locX, locY))
                    # TODO: if enemy piece, valid move
                    break

    if p == "King":
        a = [-1, 0, 1, -1, 1, -1, 0, 1]  # r vectors
        b = [-1, -1, -1, 0, 0, 1, 1, 1]  # c vectors
        print ("reached", r+a[0])
        for i in range(0, len(a)):
            if (r + a[i] < 8 and r + a[i] >= 0):
                if (c + b[i] < 8 and c + b[i] >= 0):
                    moves.append((r + a[i], c + b[i]))


    '''Given a piece and location (er: rook (4, 5), return a list of valid moves'''
    return moves



if __name__ == '__main__':
    init()
    draw_board()
    pygame.display.flip()
    running = True

    valids = []

    clicked = False
    last_loc = (-1, -1)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    clicked = False
                    draw_board()
                    break
                pos = pygame.mouse.get_pos()
                c = int(pos[0] / (side/8))
                r = int(pos[1] / (side/8))

                if clicked:
                    print ("SECOND CLICK")

                    if (r, c) in valids:
                        print ("reached {}".format(last_loc))
                        BOARD[r][c] = BOARD[last_loc[0]][last_loc[1]]
                        BOARD[last_loc[0]][last_loc[1]] = 0
                        clicked = False
                        draw_board()
                        break
                    else:
                        clicked = False
                        draw_board()
                        if BOARD[r][c] == 'Empty':
                            break

                last_loc = (r, c)
                # coorLet = chr(c + 65)
                # coorNum = 8-r
                piece = PIECES[BOARD[r][c]];

                if piece == 'Empty':
                    break
                print ("Loc: ({}, {})   = {}".format(r, c, piece))

                # Click a piece, and it shows valid moves
                # Working:
                # In progress:   knight
                valids = get_valid_moves (piece, r, c)
                draw_board(valids)
                print ("Valid Moves: ", end = " ")
                for i in range (0, len(valids)):
                    print (valids[i], end = ", ")
                print()

                print ("FIRST CLICK")
                clicked = True

            if event.type == pygame.QUIT:
                running = False

        '''GAME LOGIC'''
        #Player 1's Turn
        #Is Check? (Check for Checkmate or Check)
        #Player 2's Turn
        #Is Check? (Check for Checkmate or Check or not escaped previous Check)
        #Repeat ^^