import time
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

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BOARD_LIGHT_COLOR = (255, 206, 158)
BOARD_DARK_COLOR = (209, 139, 71)

HIGHLIGHT_COLOR = (255, 255, 0)

IMAGE_ROOT = 'images/'

class Piece(pygame.sprite.Sprite):
    def __init__(self, color, im, size):
       pygame.sprite.Sprite.__init__(self)
       # TODO: resize image to size

class Square(pygame.sprite.Sprite):
    def __init__(self, color, size):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.Surface([size, size])
       self.image.fill(color)
       self.rect = self.image.get_rect()


# Draws board and pieces
# Displays time, material count

class Graphics:
    def __init__(self) -> None:
        # setup pygame for a chess board of 8x8 squares, and a display of 800x800 pixels
        pygame.init()
        
        self.board_size = 8
        self.square_size = 100
        self.border_size = 100

        self.display_size = self.board_size * self.square_size + (2*self.border_size)

        self.display = pygame.display.set_mode(
            size=(self.display_size, self.display_size),
            flags=pygame.RESIZABLE|pygame.SCALED,
            display=display_index
        )

        self.game_timer = pygame.font.SysFont('Arial', 30)
        self.time = None

        self.board = board
        self.game = game
        self.piece_images = {}

        self.running = True
        self.load_images()
        self.draw_board()
        self.draw(self.board, self.game)

## PYGAME ##

    def handle_game_events(self):
        # Look at every event in the queue
        for event in pygame.event.get():

            # Key Press
            if event.type == KEYDOWN:
                # TODO: add key press events after game to review game

                # Q for Quit, or Esc i guess.. 
                if event.key == K_ESCAPE or event.key == ord('q'):
                    self.running = False

            # # Mouse Click
            # if event.type == pygame.MOUSEBUTTONUP:
            #     # self.click_pos = pygame.mouse.get_pos()
            #     # self.clicked_square = self.get_square_from_mouse_pos(self.click_pos)

            #     # TODO: Right click (cancel if clicked on square)
            #     if event.button == 3:
            #         self.clicked = False
            #         self.clicked_square = None
            #         # unhighlight

            #     # TODO: Left Click (select square OR move piece if your turn)
            #     else:
            #         # case: second click (move piece)
            #         if self.clicked:
            #             # save current click pos and clicked square

            #             # update click state
            #             self.clicked = True
            #             self.click_pos = pygame.mouse.get_pos()
            #             self.clicked_square = self.get_square_from_mouse_pos(self.click_pos)

            #             # unhighlight

            #         # case: first click (select piece)
            #         else:
            #             # save current click pos and clicked square
                        
            #             # update click state
            #             self.clicked = True
            #             self.click_pos = pygame.mouse.get_pos()
            #             self.clicked_square = self.get_square_from_mouse_pos(self.click_pos)

            #             # highlight
            #             # highlight possible moves

            # Quit
            elif event.type == QUIT:
                self.running = False

## DRAWING ##
    def draw_pieces(self):
        # given the board, draw the pieces on the board

        for i in range(self.board_size):
            for j in range(self.board_size):
                piece = self.board[i][j]
                if piece is not None:
                    x = self.border_size + (i * self.square_size)
                    y = self.border_size + (j * self.square_size)
                    p = Piece(piece.color, self.piece_images[piece], self.square_size)
                    self.display.blit(p.image, (x, y))
        
        # if there is no piece in the position (i, j), then draw nothing

    def draw_grid(self):
        # board size is display size - 2*border size
        grid_len = self.display_size - self.border_size
        
        counter = 0 

        # start x at border on lfet side, and increment by total board size
        for x in range(self.border_size, grid_len, self.square_size):
            for y in range(self.border_size, grid_len, self.square_size):

                # if x is even, y is odd, or vice versa, then the square is light
                if counter % 2 == 0:
                    color = BOARD_LIGHT_COLOR
                else:
                    color = BOARD_DARK_COLOR
                
                s = Square(color, self.square_size)
                self.display.blit(s.image, (x, y))

                counter += 1

            counter += 1

    def draw_board(self):
        # Fill the background BLACK
        self.display.fill((0, 0, 0))

        # draw board grid (TODO: add row column labels)
        self.draw_grid()

        # initialize game timer drawing
        self.display.blit(self.game_timer.render(self.time, True, WHITE), (self.border_size, self.border_size/2))

    def draw_turn(self):
        pass

    def draw(self, board, game):
        self.game = game
        self.board = board

        self.time = time.strftime("%H:%M:%S", time.gmtime(self.game.time))
        
        self.handle_game_events() # TODO: player on player

        # TODO: redrawing?? clear here
        self.draw_pieces() # TODO: this
        self.draw_time()
        self.draw_turn() # TODO: this
        pygame.display.flip()

    def draw_time(self, update=True):        
        if update:
            # remove old time from display
            self.display.fill(BLACK, (self.border_size, self.border_size/2, self.border_size*2, self.border_size/2))
            # draw new time
            self.display.blit(self.game_timer.render(self.time, True, WHITE), (self.border_size, self.border_size/2))

## HELPERS ##

    def get_square_from_mouse_pos(self, mouse_pos: tuple) -> tuple: # TODO: this
        pass

    def load_images(self): # TODO: this
        # TODO: load images for pieces
        # TODO: create dictionary of piece images
        pass

if __name__ == '__main__':
    from new_game import init_empty_board
    from game_state import GameState

    b = init_empty_board()
    gs = GameState()
    g = Graphics(display_index=1)
    
    # g.draw(b, gs)
    # TODO: make move
    # g.draw(b, gs)
    
    while g.running:
        g.draw(b, gs)

    pygame.quit()