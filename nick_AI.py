import numpy as np
from __init__ import *
from game_state import GameState
import threading
import random
import time

class AI :
    def __init__(self):
        self.g = GameState()
        
        self.target_move = None
        self.last_move = None
        
    # Recieve updated move from the other player ai
    def recieve(self, move):
        self.g.update(move)

    def get_random_move(self, valid_moves):
        keys = list(valid_moves.keys())
        from_pos = random.choice(keys)
        
        count = 0
        while len(valid_moves[from_pos]) == 0 and count < len(keys):
            from_pos = random.choice(list(valid_moves.keys()))
        
        to_pos = random.choice(valid_moves[from_pos]) 
        
        return translate_move_t2s(from_pos[0], from_pos[1], to_pos[0], to_pos[1])