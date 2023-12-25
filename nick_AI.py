import numpy as np
from __init__ import *
from game_state import GameState
import threading
import random
import time

class AI :
    def __init__(self):
        self.g = GameState()
        
    # Recieve updated move from the other player ai
    def recieve(self, move):
        # self.g.update(move)
        pass  

    def get_random_move(self, valid_moves):
        keys = list(valid_moves.keys())

        # get all possible moves evaluations
        evals = {}

        # print_board(self.g.board)
        curr_board = self.g.board

        for i in keys:
            for j in valid_moves[i]:
                # print(f"\n\nfrom {i} to {j}")
                pos_from = i
                pos_to = j
                
                notation = translate_move_t2s(*pos_from, *pos_to)
                # print(f"{notation}")

                b = make_move(curr_board, notation)
                b_eval = evaluate_board(b)
                evals[notation] = b_eval
                # print(b_eval)
                # print(f"{notation} @ {b_eval}")

        # find the best move
        # if white, get highest evaluation
        if self.g.player_turn:
            # print(f"best as white")
            max_value = np.max(list(evals.values()))
            best = [key for key, value in evals.items() if value == max_value]

        # if black, get the lowest eval
        else:
            # print(f"best as black")
            min_value = np.min(list(evals.values()))
            best = [key for key, value in evals.items() if value == min_value]

        # extract to string
        if len(best) > 1:
            best = random.choice(best)
        else:
            best = best[0]

        print(f"{self.g.player_turn}\t{self.g.turn_num}:\t{best} @ {evals[best]}")
        self.g.update(best)
        return best

        # pick randomly
        from_pos = random.choice(keys)
        
        count = 0
        while len(valid_moves[from_pos]) == 0 and count < len(keys):
            from_pos = random.choice(list(valid_moves.keys()))
        
        to_pos = random.choice(valid_moves[from_pos]) 
        
        return translate_move_t2s(from_pos[0], from_pos[1], to_pos[0], to_pos[1])