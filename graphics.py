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

class Graphics:
    def __init__(self, board = None, game = None, display_index=0) -> None:
        # setup pygame for a chess board of 8x8 squares, and a display of 800x800 pixels
        pygame.init()
        self.board_size = 8
        self.square_size = 100
        self.border_size = 100
        self.display_size = self.board_size * self.square_size + (2*self.border_size)

        self.framerate = 30

        self.display = pygame.display.set_mode(
            size=(self.display_size, self.display_size),
            flags=pygame.RESIZABLE|pygame.SCALED,
            display=display_index
        )
        self.clock = pygame.time.Clock()

        self.board = board
        self.game = game
        self.piece_images = {}

        self.running = True

        self.load_images()
        self.init_board()
        pygame.display.update()

    def load_images(self):
        # TODO: load images for pieces
        pass

    def init_board(self):
        # TODO: initialize board

        # Fill the background BLACK
        self.display.fill((0, 0, 0))
        
        # draw board grid (TODO: add row column labels)
        self.draw_grid()
        
        # initialize game timer drawing
        self.game_timer = pygame.font.SysFont('Arial', 30)
        self.display.blit(self.game_timer.render('00:00', True, WHITE), (self.border_size, self.border_size/2))

    def draw(self, board, gs):
        # handle pygame events like quitting or aftergame controls
        self.handle_game_events()

        # update screen
        pygame.display.flip()

        # Ensure program maintains a rate of 30 frames per second
        self.clock.tick(self.framerate)

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
            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == K_ESCAPE or event.key == ord('q'):
                    self.running = False

            # Did the user click the window close button? If so, stop the loop.
            elif event.type == QUIT:
                self.running = False

if __name__ == '__main__':
    g = Graphics()
    while g.running:
        g.draw(None, None)
    pygame.quit()