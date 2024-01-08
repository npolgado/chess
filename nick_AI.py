import numpy as np
from __init__ import *
from game_state import GameState
import threading
import random
import time

class AI :
    def __init__(self, DEBUG: bool=True):
        self.debug = DEBUG
        self.g = GameState()
        self.last_move = None
        
    # Recieve updated move from the other player ai
    def recieve(self, move):
        if move is not None:
            self.g.update(move)
            self.last_move = move 
            # if self.debug:
            #     print("RECIEVE")
            #     print_board(self.g.board)
            #     print("-----------------------------------")
            #     print(f"NICK RECIEVED MOVE: {move}")

    def get_random_move(self, valid_moves):
        # if self.debug:
        #     print("ai board")
        #     print_board(self.g.board)
        #     print("-----------------------------------")

        keys = list(valid_moves.keys())

        # get all possible moves evaluations
        evals = {}

        # print_board(self.g.board)
        curr_board = np.copy(self.g.board)

        for i in keys:
            for j in valid_moves[i]:
                pos_from = i
                pos_to = j
                
                notation = translate_move_t2s(*pos_from, *pos_to)

                b, _ = make_move(curr_board, notation)
                b_eval = evaluate_board(b)
                evals[notation] = b_eval

        # find the best move
        # if black, get lowest evaluation
        if self.g.player_turn:
            max_value = np.min(list(evals.values()))
            best = [key for key, value in evals.items() if value == max_value]

        # if white, get the highest eval
        else:
            min_value = np.max(list(evals.values()))
            best = [key for key, value in evals.items() if value == min_value]

        # extract to string
        if len(best) > 1:
            best = random.choice(best)
        else:
            best = best[0]

        self.g.update(best)
        return best

        # pick randomly
        from_pos = random.choice(keys)
        
        count = 0
        while len(valid_moves[from_pos]) == 0 and count < len(keys):
            from_pos = random.choice(list(valid_moves.keys()))
        
        to_pos = random.choice(valid_moves[from_pos]) 
        
        return translate_move_t2s(from_pos[0], from_pos[1], to_pos[0], to_pos[1])