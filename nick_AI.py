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
            # start threaded process
            threading.Thread(
                target=self.process_move,
                args=(move,)
            ).start()
            
            self.thinking = True

    def get_target_move(self, valid_moves):
        tmp = self.target_move
        self.target_move = None
        return tmp
    
    def process_move(self, move):
        with self.lock:

            # CASE: WAITING FOR OTHER PLAYER1
            if move == None and self.g.turn != 1: 
                self.thinking = False
                return
            
            # CASE: PLAYER HAS MOVED
            if move != None:
                self.g.update(move)
                self.last_move = move

            # update valid moves to only include current players moves
            valid_moves = self.g.get_valid_moves()
            player_valid_moves = {}

            print("VALID MOVES")
            print(valid_moves)
            print("\n\n")

            for i in valid_moves:
                piece = self.g.board[i[0]][i[1]]
                        
                # ignore pieces without valid moves
                if valid_moves[i] == []:
                    continue
                
                # if black ignore lowercase keys
                if self.g.bool_turn and piece.islower():
                    continue
                
                # if white, ignore upper case keys, 
                elif not self.g.bool_turn and piece.isupper():
                    continue
                
                player_valid_moves[i] = valid_moves[i]

            print("VALID MOVES")
            print(player_valid_moves)
            print("\n\n")

            # Find a random move where the keys are the from_pos, and the values are the to_pos
            from_pos = random.choice(list(player_valid_moves.keys()))
            to_pos = random.choice(player_valid_moves[from_pos]) 

            # Construct Target Move          
            target_move = translate_move_t2s(from_pos[0], from_pos[1], to_pos[0], to_pos[1])
            print(f"AI move: {from_pos} -> {to_pos}")
            print(f"AI move: {target_move}")

            # Update game board state from target move
            self.g.update(target_move)

            # Set target move to be returned
            self.target_move = target_move

            # Signal process is done
            self.thinking = False

    def encode(self):
        pass

    def decode(self):
        pass

    def softmax(self, x):
        exp_x = np.exp(x - np.max(x))  # Subtracting np.max(x) for numerical stability
        return exp_x / exp_x.sum(axis=0)

    def forward(self):
        pass

    def attention(self, q, k, v):
        # "Scaled Dot-Product Attention"
        # multi-head attention given a query, key, and value
        # We compute the dot products of the query with all keys,
        # divide each by √dk, and apply a softmax function 
        # to obtain the weights on the values.

        pass