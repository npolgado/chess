import numpy as np

class AI :
    def __init__(self, game, col):
        self.game = game    # game object to get information about the game
        self.color = col    # color the ai is playing (0 white, 1 black)

        self.target_move = None

    # has to be non-blocking, return none and thread the processing of the move
    def recieve(self, move: str) -> None:
        self.target_move = None
        pass

    def get_target_move(self) -> tuple:
        return self.target_move