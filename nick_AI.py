import numpy as np
from __init__ import *
from game_state import GameState

class AI :
    def __init__(self):
        self.g = GameState(init_empty_board())
        self.target_move = None
        self.opponent_move = None
        
    # has to be non-blocking, return none and thread the processing of the move
    def recieve(self, move: str) -> None:
        self.target_move = None

    def get_target_move(self):
        return self.target_move
    
    def process_move(self, move: str) -> None:
        # 1. update board given move
        self.board = make_move(self.board, move)
        
        # 2. update opponent_move
        self.opponent_move = move

        # 3. get valid moves
        self.g.get_valid_moves(self.board, self.opponent_move)
        
        pass