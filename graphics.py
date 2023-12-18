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


class Graphics:
    def __init__(self, board = None, game = None) -> None:
        # setup pygame for a chess board of 8x8 squares, and a display of 800x800 pixels
        pygame.init()
        self.board_size = 8
        self.square_size = 100
        self.display_size = self.board_size * self.square_size
        self.border_size = 100
        self.display = pygame.display.set_mode((self.display_size, self.display_size))
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

    def draw(self, board, gs):
        self.handle_game_events()
        pygame.display.flip()

    def handle_game_events(self):
        # Look at every event in the queue
        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == K_ESCAPE:
                    self.running = False

            # Did the user click the window close button? If so, stop the loop.
            elif event.type == QUIT:
                self.running = False

if __name__ == '__main__':
    g = Graphics()
    while g.running:
        g.draw(None, None)