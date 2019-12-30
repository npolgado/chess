from dataclasses import dataclass
import copy
import pygame
from random import randrange


# TODO: change explosions to not be randomly created, but instead created by a lookup table and a d8

a = 8
b = 6
SQ_SZ = 100

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 162, 0)
RED = (252, 36, 3)
GREEN = (0, 224, 120)
PINK = (240, 20, 247)
color1 = (176, 46, 89)
color2 = (36, 214, 87)
color3 = (217, 192, 54)
color4 = (50, 188, 230)
color5 = (230, 96, 0)
color5 = (232, 49, 220)

wid = a*SQ_SZ
hgt = b*SQ_SZ

size = (wid, hgt)

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Flashpoint Setup')
screen.fill(WHITE)

@dataclass
class Tile:
    r: bool
    d: bool
    counters: (int, int) = (0, 0)
    rDoor: bool = False
    dDoor: bool = False

t = Tile(False, False)

fire = []

board = [[copy.deepcopy(t) for i in range(8)] for j in range(6)]

# WALLS
board[0][2].r = True
board[0][4].r = True

board[1][2].r = True
board[1][4].r = True    #
for i in range(2, 8):
    board[1][i].d = True

board[2][1].r = True
board[2][5].r = True

board[3][1].r = True
board[3][5].r = True    #
for i in range(8):
    board[3][i].d = True

board[4][4].r = True
board[4][6].r = True

board[5][4].r = True
board[5][6].r = True

# DOORS
board[0][2].rDoor = True
board[1][4].rDoor = True
board[1][7].dDoor = True
board[2][1].rDoor = True
board[3][5].rDoor = True
board[3][3].dDoor = True
board[5][4].rDoor = True
board[5][6].rDoor = True


def print_board ():
    for row in board:
        for el in row:
            s = ""
            if el.d:
                if el.dDoor:
                    s+= "+"
                else:
                    s += "_"
            else:
                s += " "
            if el.r:
                if el.rDoor:
                    s += "l"
                else:
                    s += "|"
            else:
                s += "."
            print(s, end="")
        print()

def draw_board():
    global screen
    pygame.font.init()

    buffer = 4

    # squares
    for i in range(8):
        for j in range(6):
            pygame.draw.rect(screen, color4, (i * SQ_SZ + buffer/2, j * SQ_SZ + buffer/2, SQ_SZ-buffer, SQ_SZ-buffer))

    # walls
    for i in range(8):
        for j in range(6):
            til = board[j][i]
            if til.r or i == 7:
                rec = ((i+1)*SQ_SZ- buffer, j*SQ_SZ-buffer, 10, SQ_SZ)
                pygame.draw.rect(screen, BLACK, rec)
                for ctr in range(til.counters[0]):
                    pygame.draw.rect(screen, ORANGE, ((i+1) * SQ_SZ - buffer*2, j * SQ_SZ + (ctr+1)*SQ_SZ/3, 20, 10))

            if til.d or j == 5:
                rec = (i * SQ_SZ - buffer, (j+1)*SQ_SZ-buffer, SQ_SZ, 10)
                pygame.draw.rect(screen, BLACK, rec)
                for ctr in range(til.counters[1]):
                    pygame.draw.rect(screen, ORANGE, (i*SQ_SZ + (ctr+1)*SQ_SZ/3, (j+1) * SQ_SZ - buffer*2, 10, 20))

    l = 18
    for i in range(len(fire)):
        f = fire[i]
        pygame.draw.circle(screen, ORANGE, (int(f[0]*SQ_SZ + SQ_SZ/2), int(f[1]*SQ_SZ + SQ_SZ/2)), l)
        if i in exp_inds:
            pygame.draw.circle(screen, RED, (int(f[0] * SQ_SZ + SQ_SZ / 2), int(f[1] * SQ_SZ + SQ_SZ / 2)), int(l/3))

    for i in range(len(people)):
        p = people[i]
        pygame.draw.circle(screen, GREEN, (int(p[0]*SQ_SZ + SQ_SZ/2), int(p[1]*SQ_SZ + SQ_SZ/2)), l)

    for i in range(len(haz)):
        h = haz[i]
        pygame.draw.circle(screen, PINK, (int(h[0] * SQ_SZ + SQ_SZ / 2), int(h[1] * SQ_SZ + SQ_SZ / 2)), l)

    pygame.display.update()


if __name__ == '__main__':


    people = []
    haz = []

    # FIRES/ EXPLOSIONS
    exp_inds = []
    cnt = 0
    for i in range(3):
        dice_roll = (randrange(8), randrange(6))
        while dice_roll in fire:
            dice_roll = (randrange(8), randrange(6))
        # dice_roll = (0, 0)
        fire.append(dice_roll)
        exp_inds.append(cnt)
        cnt+=1

        # spread fire in 4 directions
        exp_cent = board[dice_roll[1]][dice_roll[0]]
        # right
        if exp_cent.r or dice_roll[0] == 7:
            exp_cent.counters = (exp_cent.counters[0] + 1, exp_cent.counters[1])
        else:
            fire.append((dice_roll[0]+1, dice_roll[1]))
            cnt += 1

        # down
        if exp_cent.d or dice_roll[1] == 7:
            exp_cent.counters = (exp_cent.counters[0], exp_cent.counters[1] + 1)
        else:
            it_cent = exp_cent
            fire.append((dice_roll[0], dice_roll[1]+1))
            cnt += 1

        # left
        exp_left = board[dice_roll[1]][dice_roll[0]-1]
        if exp_left.r:
            exp_left.counters = (exp_left.counters[0] + 1, exp_left.counters[1])
        else:
            fire.append((dice_roll[0]-1, dice_roll[1]))
            cnt += 1

        # up
        exp_up = board[dice_roll[1]-1][dice_roll[0]]
        # print("up-cent= (", dice_roll[1]-1, dice_roll[0], ")   ", exp_up)
        if exp_up.d:
            exp_up.counters = (exp_up.counters[0], exp_up.counters[1]+1)
        else:
            fire.append((dice_roll[0], dice_roll[1]-1))
            cnt += 1

        draw_board()
        pygame.time.wait(200)

    # PEOPLE
    for i in range(3):
        dice_roll_2 = (randrange(8), randrange(6))
        while dice_roll_2 in fire or dice_roll_2 in people:
            dice_roll_2 = (randrange(8), randrange(6))

        people.append(dice_roll_2)

        draw_board()
        pygame.time.wait(200)

    # HAZARDOUS
    for i in range(3):
        dice_roll_3 = (randrange(8), randrange(6))
        while dice_roll_3 in fire or dice_roll_3 in people or dice_roll_3 in haz:
            dice_roll_3 = (randrange(8), randrange(6))

        haz.append(dice_roll_3)

        draw_board()
        pygame.time.wait(200)

    # print_board()
    draw_board()

    pygame.time.wait(100000)
