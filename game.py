import pygame

NUM_BLOCKS = 30

SQ_SZ = 25


side = SQ_SZ * NUM_BLOCKS
size = (side, side)
screen = pygame.display.set_mode(size)


pygame.init()
pygame.display.set_caption('Chess')



GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)



board = [[5, 2, 3, 9, 6, 3, 2, 5],
         [1]*8, [0]*8, [0]*8, [0]*8, [0]*8, [1]*8,
         [5, 2, 3, 9, 6, 3, 2, 5]]

def draw_board():
    global board

    screen.fill(WHITE)

    pygame.font.init()  # you have to call this at the start,
    # # if you want to use this module.
    # myfont = pygame.font.SysFont('Comic Sans MS', 15)
    # textsurface = myfont.render('SCORE: ' + str(score), False, BLACK)
    # textsurface2 = myfont.render('HI:    ' + str(hiScore), False, BLACK)  # 'HI:    '+ str(hiScore)
    # screen.blit(textsurface, (side - 100, 10))
    # screen.blit(textsurface2, (side - 100, 30))

    a = 8
    for i in range (a):
        for j in range(a):
            len = (side/a)
            # pygame.draw.rect(screen, BLACK, (i * len + len / 4, j * len + len / 4, len-1, len-1))
            # pygame.draw.rect(screen, RED, (i *len +len/4, j * len +len/4, len*(4/5), len*(4/5)))
            myfont = pygame.font.SysFont('Comic Sans MS', 15)
            textsurface = myfont.render(str(board[j][i]), False, BLACK)
            screen.blit(textsurface, (i *len +len/4, j *len +len/4))

    pygame.display.update()

    pygame.time.wait(5000)

draw_board()

while True:
    pass