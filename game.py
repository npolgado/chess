import pygame
import numpy as np

NUM_BLOCKS = 30
SQ_SZ = 25

GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

PIECES = {
    0: 'Empty',    1: 'Pawn',
    2: 'Bishop',    3: 'Knight',
    5: 'Rook',    6: 'King',
    9: 'Queen'
}

BOARD = [[5, 2, 3, 9, 6, 3, 2, 5],
         [1]*8, [0]*8, [0]*8, [0]*8, [0]*8, [1]*8,
         [5, 2, 3, 9, 6, 3, 2, 5]]

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

def draw_board():
    global BOARD, screen
    pygame.font.init()  # you have to call this at the start,

    a = 8
    for i in range (a):
        for j in range(a):
            len = (side/a)
            if (i+j) % 2 == 0:
                pygame.draw.rect(screen, RED, (i*len, j*len , len-1, len-1))
            else:
                pygame.draw.rect(screen, BLACK, (i*len, j*len , len-1, len-1))

            myfont = pygame.font.SysFont('Comic Sans MS', 50)
            textsurface = myfont.render(str(BOARD[j][i]), False, GREEN)
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
                print ("mouse = ", pos)
                print ("   ")
            if event.type == pygame.QUIT:
                running = False

        '''GAME LOGIC'''
        #Player 1's Turn
        #Is Check? (Check for Checkmate or Check)
        #Player 2's Turn
        #Is Check? (Check for Checkmate or Check or not escaped previous Check)
        #Repeat ^^