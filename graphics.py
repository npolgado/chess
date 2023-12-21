import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    # K_UP,
    # K_DOWN,
    # K_LEFT,
    # K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from __init__ import *
import numpy as np
import time

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BOARD_LIGHT_COLOR = (255, 206, 158)
BOARD_DARK_COLOR = (209, 139, 71)

HIGHLIGHT_COLOR = (255, 255, 0)

IMAGE_ROOT = 'images/'

FULL_NAMES = {
    'P': 'Pawn',
    'N': 'Knight',
    'B': 'Bishop',
    'R': 'Rook',
    'Q': 'Queen',
    'K': 'King',
    'p': 'Pawn',
    'n': 'Knight',
    'b': 'Bishop',
    'r': 'Rook',
    'q': 'Queen',
    'k': 'King'
}

TEST_BOARD_3 = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', '-', 'p', 'p', 'p', 'p'],
    ['-', '-', '-', '-', '-', '-', '-', '-'], 
    ['-', '-', '-', 'p', '-', '-', '-', '-'],
    ['-', '-', '-', '-', 'P', '-', '-', '-'], 
    ['-', '-', '-', '-', '-', '-', '-', '-'], 
    ['P', 'P', 'P', 'P', '-', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
]

class White(pygame.sprite.Sprite):
    def __init__(self, piece, size):
        pygame.sprite.Sprite.__init__(self)

        # get image filepath
        im = os.path.join(IMAGE_ROOT, 'White', FULL_NAMES[piece] + '.png')

        # Load image from file path im
        self.image = pygame.image.load(im).convert_alpha()
        self.image.set_colorkey(None)

        # Scale image to size
        self.image = pygame.transform.scale(self.image, (size, size))

        # Set image background to transparent
        self.rect = self.image.get_rect()

class Black(pygame.sprite.Sprite):
    def __init__(self, piece, size):
        pygame.sprite.Sprite.__init__(self)

        # get image filepath
        im = os.path.join(IMAGE_ROOT, 'Black', FULL_NAMES[piece] + '.png')

        # Load image from file path im
        self.image = pygame.image.load(im).convert_alpha()
        self.image.set_colorkey(None)

        # Scale image to size
        self.image = pygame.transform.scale(self.image, (size, size))

        # Set image background to transparent
        self.rect = self.image.get_rect()

class Square(pygame.sprite.Sprite):
    def __init__(self, color, size):
       pygame.sprite.Sprite.__init__(self)

       # Create a square image of the given size
       self.image = pygame.Surface([size, size])
       
       # Fill the square with the given color
       self.image.fill(color)
       
       # Set image background to transparent
       self.rect = self.image.get_rect()

# Draws board and pieces
# Displays time, material count
class Graphics:
    def __init__(self, board=None, game_time: tuple=None, display_index=0) -> None:
        # setup pygame for a chess board of 8x8 squares, and a display of 800x800 pixels
        pygame.init()
        
        self.board_size = 8
        self.square_size = 75
        self.border_size = 100
        self.piece_padding = 10
        self.pos_offset = self.piece_padding / 2

        self.display = board
        self.display_size = self.board_size * self.square_size + (2*self.border_size)

        self.clicked = False
        self.click_pos = (0,0)

        # self.board = board
        self.running = True

        self.game_timer_white = pygame.font.SysFont('Arial', 30)
        self.game_timer_black = pygame.font.SysFont('Arial', 30)

        self.game_time_white = "00:00:00" if game_time == None else self.format_elapsed_time(game_time[0])
        self.game_time_black = "00:00:00" if game_time == None else self.format_elapsed_time(game_time[1])

        self.init(display_index)

    def init(self, display_index):
        self.display = pygame.display.set_mode(
            size=(self.display_size, self.display_size),
            flags=pygame.RESIZABLE|pygame.SCALED|pygame.SRCALPHA,
            display=display_index
        )
        pygame.display.set_caption('Chess')
        pygame.display.set_icon(pygame.image.load(os.path.join(IMAGE_ROOT, 'Black', 'King.png')))
        pygame.display.flip()

    def handle_game_events(self):
        # Look at every event in the queue
        for event in pygame.event.get():

            # Key Press
            if event.type == KEYDOWN:
                # TODO: add key press events after game to review game

                # Q for Quit, or Esc i guess.. 
                if event.key == K_ESCAPE or event.key == ord('q'):
                    self.running = False

            # Mouse Click
            if event.type == pygame.MOUSEBUTTONUP:
                self.click_pos = pygame.mouse.get_pos()
                self.clicked_square = self.get_square_from_mouse_pos(self.click_pos)

                # TODO: Right click (cancel if clicked on square)
                if event.button == 3:
                    self.clicked = False
                    self.clicked_square = None
                    # unhighlight

                # TODO: Left Click (select square OR move piece if your turn)
                else:
                    # case: second click (move piece)
                    if self.clicked:
                        # save current click pos and clicked square

                        # update click state
                        self.clicked = True
                        self.click_pos = pygame.mouse.get_pos()
                        self.clicked_square = self.get_square_from_mouse_pos(self.click_pos)

                        # unhighlight

                    # case: first click (select piece)
                    else:
                        # save current click pos and clicked square
                        
                        # update click state
                        self.clicked = True
                        self.click_pos = pygame.mouse.get_pos()
                        self.clicked_square = self.get_square_from_mouse_pos(self.click_pos)

                        # highlight
                        # highlight possible moves

            # Quit
            elif event.type == QUIT:
                self.running = False
                
    def draw(self, board, game_time):
        # update state
        self.game_time_white = "00:00:00" if game_time == None else self.format_elapsed_time(game_time[0])
        self.game_time_black = "00:00:00" if game_time == None else self.format_elapsed_time(game_time[1])
        self.board = np.flip(board, axis=0)
        
        # TODO: player on player
        self.handle_game_events()

        # Clear the entire screen
        self.display.fill(BLACK)

        # Draw white time
        self.display.blit(self.game_timer_white.render(self.game_time_white, True, WHITE), (self.border_size, self.border_size/2))

        # Draw black time
        self.display.blit(self.game_timer_black.render(self.game_time_black, True, WHITE), (self.border_size, self.display_size - self.border_size))

        counter = 0 

        # Draw board
        for i in range(self.board_size):
            for j in range(self.board_size):

                # get square position
                x = self.border_size + (i * self.square_size)
                y = self.border_size + (j * self.square_size)

                # alternate colors
                color = BOARD_LIGHT_COLOR if counter % 2 == 0 else BOARD_DARK_COLOR

                # get piece notation from board_state
                piece = self.board[j][i]

                # draw squares
                s = Square(color, self.square_size)
                self.display.blit(s.image, (x, y))

                # draw piece
                if piece is not None:
                    if piece == '-':
                        pass

                    elif piece.isupper():
                        p = Black(piece, self.square_size-self.piece_padding)
                        self.display.blit(p.image, (x+self.pos_offset, y+self.pos_offset))

                    else:
                        p = White(piece, self.square_size-self.piece_padding)
                        self.display.blit(p.image, (x+self.pos_offset, y+self.pos_offset))                    

                counter += 1

            counter += 1

        # Update display
        if self.running: pygame.display.flip()

    def format_elapsed_time(self, elapsed_time_seconds):
        hours, remainder = divmod(elapsed_time_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = int((elapsed_time_seconds - int(elapsed_time_seconds)) * 1000)
        
        return "{:02d}:{:02d}:{:02d}.{:03d}".format(int(hours), int(minutes), int(seconds), milliseconds)

    def get_square_from_mouse_pos(self, mouse_pos: tuple) -> tuple: # TODO: this
        pass

if __name__ == '__main__':
    from game_state import GameState

    b = init_empty_board()
    gs = GameState()
    g = Graphics(display_index=0)
    
    s = time.monotonic()
    while g.running:
        curr_time = float(time.monotonic()-s)
        g.draw(b, gs.time)
        gs.time = (curr_time,curr_time) #TODO: time is using time.gmtime() so it is not accurate

        if gs.time[0] > 3 and gs.time[1] > 3.02:
            b = TEST_BOARD_3

        if gs.time[0] > 6 and gs.time[1] > 6.02:
            b = [
                ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                ['p', 'p', 'p', 'p', '-', 'p', 'p', 'p'],
                ['-', '-', '-', '-', '-', '-', '-', '-'],
                ['-', '-', '-', '-', '-', '-', '-', '-'],
                ['-', '-', '-', 'p', '-', '-', '-', '-'],
                ['-', '-', '-', '-', '-', '-', '-', '-'],
                ['P', 'P', 'P', '-', 'P', 'P', 'P', 'P'],
                ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
            ]

    pygame.quit()