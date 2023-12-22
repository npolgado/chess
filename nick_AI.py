import numpy as np
from __init__ import *
from game_state import GameState
import threading
import random
import time

class AI :
    def __init__(self):
        self.g = GameState(init_empty_board())

        self.thinking = False
        
        self.target_move = None
        
        self.last_move = None

        self.threading_process = None
        self.lock = threading.Lock()
        
    # has to be non-blocking, return none and thread the processing of the move
    def recieve(self, move):
        with self.lock:
            if move == None or self.thinking:
                self.target_move = None
                return
            
            # start threaded process
            threading.Thread(
                target=self.process_move,
                args=(move,)
            ).start()
            
            self.thinking = True
            self.target_move = None

    def get_target_move(self, valid_moves):
        return self.target_move
    
    def process_move(self, move: str):
        with self.lock:
            # Update game board state from opponent move
            self.g.update(move)
            self.last_move = move
            self.g.get_valid_moves()
            
            # using self.g.valid_moves, find a random move where the keys are the from_pos, and the values are the to_pos
            from_pos = random.choice(list(self.g.valid_moves.keys()))
            while len(self.g.valid_moves[from_pos]) == 0:
                from_pos = random.choice(list(self.g.valid_moves.keys()))
            
            # Construct Target Move
            to_pos = random.choice(self.g.valid_moves[from_pos])           
            target_move = translate_move_t2s(from_pos[0], from_pos[1], to_pos[0], to_pos[1])
            # print(f"AI move: {from_pos} -> {to_pos}")
            # print(f"AI move: {target_move}")

            # Update game board state from target move
            self.g.update(target_move)

            self.target_move = target_move
            self.thinking = False