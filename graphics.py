import time
import datetime
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


class Graphics:
    def __init__(self, board=None, game=None, display_index=0) -> None:
        # setup pygame for a chess board of 8x8 squares, and a display of 800x800 pixels
        pygame.init()
        self.board_size = 8
        self.square_size = 100
        self.border_size = 100
        self.display_size = self.board_size * self.square_size + (2*self.border_size)

        self.framerate = 30

        self.clicked = False
        self.click_pos = (0,0)

        self.display = pygame.display.set_mode(
            size=(self.display_size, self.display_size),
            flags=pygame.RESIZABLE|pygame.SCALED,
            display=display_index
        )

        self.game_timer = pygame.font.SysFont('Arial', 30)
        self.start_time = time.monotonic()
        self.game_time = 0

        self.board = board
        self.game = game
        self.piece_images = {}

        self.running = True

        self.load_images()
        self.init_board()
        self.draw(self.board, self.game)

    def load_images(self):
        # TODO: load images for pieces
        pass

    def init_board(self):
        # TODO: initialize board

        # Fill the background BLACK
        self.display.fill((0, 0, 0))
        
        # draw board grid (TODO: add row column labels)
        self.draw_grid()
        
        # get formatted string of self.game_time as XX:XX:XX of minutes and seconds and miliseconds elapsed
        time_str = time.strftime("%H:%M:%S", time.gmtime(self.game_time))

        # initialize game timer drawing
        self.display.blit(self.game_timer.render(time_str, True, WHITE), (self.border_size, self.border_size/2))

    def draw_time(self, update=True):
        # TODO: draw time: update self.game_timer
        # get current game time
        curr_time = time.monotonic()
        new_time = float(curr_time - self.start_time)
        time_str = time.strftime("%H:%M:%S", time.gmtime(new_time))
        
        if update:
            # remove old time from display
            self.display.fill(BLACK, (self.border_size, self.border_size/2, self.border_size*2, self.border_size/2))
            # draw new time
            self.display.blit(self.game_timer.render(time_str, True, WHITE), (self.border_size, self.border_size/2))

    def draw(self, board, game):
        # handle pygame events like quitting or aftergame controls
        self.handle_game_events()

        # TODO: drawing???
        self.draw_time()

        # update screen
        pygame.display.flip()

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
                
                rect = pygame.Rect(x, y, self.square_size, self.square_size)
                self.display.fill(color, rect)
                pygame.draw.rect(self.display, color, rect, 1)

                counter += 1

            counter += 1

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

                # TODO: Right click (cancel if clicked on square)
                if event.button == 3:
                    self.clicked = False
                    # unhighlight
                    # break # TODO: ?

                # TODO: Left Click (select square OR move piece if your turn)
                else:
                    self.clicked = True
                    self.clicked_square = self.get_square_from_mouse_pos(self.click_pos)

                    # case: second click (move piece)
                    if self.clicked:
                        pass
                    # case: first click (select piece)
                    else: 
                        pass

            # Quit
            elif event.type == QUIT:
                self.running = False

    def get_square_from_mouse_pos(self, mouse_pos: tuple) -> tuple: # TODO: this
        pass

if __name__ == '__main__':
    from new_game import init_empty_board
    from game_state import GameState

    b = init_empty_board()
    gs = GameState()
    g = Graphics()
    
    g.draw(b, None)
    # TODO: make move
    # g.draw(b, None)
    
    while g.running:
        g.draw(b, None)
    pygame.quit()