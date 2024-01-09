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
        self.last_opponent_move = None

    def get_evals(self, valid_moves, board):
        # get_evals
        # given a board and valid moves, return a dict of move: evaluation
        keys = list(valid_moves.keys())
        evals = {}
        curr_board = np.copy(board)

        # make each valid move and evaluate the board
        for i in keys:
            for j in valid_moves[i]:
                pos_from = i
                pos_to = j
                
                notation = translate_move_t2s(*pos_from, *pos_to)

                b, _ = make_move(curr_board, notation)
                b_eval = evaluate_board(b)

                # if not in the dict, add it
                if not evals[notation]: evals[notation] = b_eval
        
        return evals

    def recieve(self, move):
        if move is not None:
            self.g.update(move)
            self.last_opponent_move = move 

    def get_ai_move(self, valid_moves):
        keys = list(valid_moves.keys())
        curr_board = np.copy(self.g.board)

        # 1. Get all possible moves evaluations
        evals = self.get_evals(valid_moves, curr_board)

        # 2. Find the best move
        for evaluation, notation in evals.items():
            print(f"{notation}: {evaluation}")

            # fake update 
            b, _ = make_move(curr_board, notation)
            self.g.player_turn = not self.g.player_turn

            # get valid moves for the other player
            valid_opponent_moves = self.g.get_valid_moves(b)

            # undo gs update
            self.g.player_turn = not self.g.player_turn
            self.g.board = np.copy(curr_board)

        # if black, get lowest evaluation
        if self.g.player_turn:
            max_value = np.min(list(evals.values()))
            best = [key for key, value in evals.items() if value == max_value]

        # if white, get the highest eval
        else:
            min_value = np.max(list(evals.values()))
            best = [key for key, value in evals.items() if value == min_value]


        # 3. Format and return target move

        # extract to string
        if len(best) > 1:
            best = random.choice(best)
        else:
            best = best[0]

        self.g.update(best)
        return best

    def get_random_move(self, valid_moves):

        keys = list(valid_moves.keys())

        # pick randomly
        from_pos = random.choice(keys)
        
        count = 0
        while len(valid_moves[from_pos]) == 0 and count < len(keys):
            from_pos = random.choice(list(valid_moves.keys()))
        
        to_pos = random.choice(valid_moves[from_pos]) 
        
        return translate_move_t2s(from_pos[0], from_pos[1], to_pos[0], to_pos[1])