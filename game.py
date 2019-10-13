import pygame

NUM_BLOCKS = 30

SQ_SZ = 25


side = SQ_SZ * NUM_BLOCKS
size = (side, side)
screen = pygame.display.set_mode(size)


pygame.init()
pygame.display.set_caption('SNEK')



GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)





def draw_board():

    screen.fill(WHITE)

    pygame.font.init()  # you have to call this at the start,
    # # if you want to use this module.
    # myfont = pygame.font.SysFont('Comic Sans MS', 15)
    # textsurface = myfont.render('SCORE: ' + str(score), False, BLACK)
    # textsurface2 = myfont.render('HI:    ' + str(hiScore), False, BLACK)  # 'HI:    '+ str(hiScore)
    # screen.blit(textsurface, (side - 100, 10))
    # screen.blit(textsurface2, (side - 100, 30))

    a= 6
    for i in range (a):
        for j in range(a):
            pygame.draw.rect(screen, RED, (i *(side/a), j + (side/a), SQ_SZ * 2 / 2, SQ_SZ * 2 / 2))

    pygame.display.update()

    pygame.time.wait(5000)






draw_board()