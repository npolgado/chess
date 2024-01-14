import numpy as np
from __init__ import *
from game_state import GameState
import threading
import random
import time
import copy

class AI(threading.Thread):
    def __init__(self, DEBUG=False, lock=None):
        super().__init__()
        
        self.sent_move = False
        self.recieved_move = False

        self.last_opponent_move = None
        self.target_move = None

        # self.thread = threading.Thread(target=self.run)
        if lock:
            self.lock = lock
        else: self.lock = threading.Lock()
        
        self.stop_thread = False
        self.debug = DEBUG
        self.g = GameState()

    def run(self):
        while True:                     
            if self.stop_thread: 
                self.stop_thread = False
                return
            
            if self.recieved_move:
                self.recieved_move = False
                
                self.aip(f"AI THREAD recieved move {self.last_opponent_move}")
                
                v_m = self.g.get_valid_moves()
                # move = self.calculate_move(v_m)
                move = self.get_random_move(v_m)

                self.aip(f"AI THREAD calculated move {move}", True)
                
                self.target_move = move
                self.sent_move = True

    def recieve(self, move):
        if move is not None:            
            self.g.update(move)

            self.last_opponent_move = move
            self.recieved_move = True
            
            self.aip(f"AI Game State Updated\n\tPlayer: {self.g.player_turn} | Turn: {self.g.turn_num}\n", True)
        
        else: self.aip("Recieved None")

    def get_move(self, valid_moves):
        if self.sent_move:
            self.sent_move = False
            tmp = self.target_move
            self.target_move = None
            return tmp
        
        elif self.g.turn_num == 1:
            return self.get_random_move(valid_moves)
        
        else: return None

    def aip(self, message:str, sep=False, end="\n"):
        if self.debug: 
            print(f"[NICK_AI] {message}")
            if sep: 
                print("--------------------------------------------------", end=end)

    def get_evals(self, valid_moves, board):
        # get_evals
        # given a board and valid moves, return a dict of move: evaluation
        keys = list(valid_moves.keys())
        evals = {}
        curr_board = copy.deepcopy(board)

        # make each valid move and evaluate the board
        for i in keys:
            for j in valid_moves[i]:                
                notation = translate_move_t2s(*i, *j)
                b, _ = make_move(curr_board, notation)
                if notation not in evals.keys(): evals[notation] = evaluate_board(b)

        return evals
        
    def calculate_move(self, valid_moves):
        # Save current board state
        side = "Black" if self.g.player_turn else "White"
        curr_board = copy.deepcopy(self.g.board)
        curr_evaluation = evaluate_board(curr_board)
        curr_en_passant = self.g.en_passant

        self.aip(f"Getting Target Move\n\tTurn {self.g.turn_num} | {side}'s Turn | Eval = {curr_evaluation}")

        # 1. Get all possible moves evaluations
        evals = self.get_evals(valid_moves, curr_board)
        best_moves = {}

        # 2. Find the best move
        #   a. go through possible moves
        for notation, evaluation in evals.items():
            self.aip(f"\tPossible Move {notation}: {evaluation}")


            b, _ = make_move(curr_board, notation)

            # fake turn change to get opponent moves
            self.g.player_turn = not self.g.player_turn
            self.g.board = copy.deepcopy(b)
            self.g.en_passant = _
            
            valid_opponent_moves = self.g.get_valid_moves()
            
            self.g.player_turn = not self.g.player_turn
            self.g.board = copy.deepcopy(curr_board)
            self.g.en_passant = curr_en_passant

            # go through opponent moves and get the worst case scenario
            opponent_evals = self.get_evals(valid_opponent_moves, b)
            opponent_evaluation = None
            
            for i in opponent_evals.values():
                
                # get worse case scenario (higest if opponent is black, lowest if opponent is white)
                if self.g.player_turn:
                    if i > curr_evaluation:
                        if opponent_evaluation is None: opponent_evaluation = i
                        elif i > opponent_evaluation: opponent_evaluation = i
                else:
                    if i < curr_evaluation:
                        if opponent_evaluation is None: opponent_evaluation = i
                        elif i < opponent_evaluation: opponent_evaluation = i
                
                # self.aip(f"\t| O.Eval = {opponent_evaluation} | Curr.Eval = {curr_evaluation} | INDEX = {i}")

            if opponent_evaluation is None: 
                best_moves[notation] = evaluation            
            else:
                # if the opponent evaluation is better (depending on player turn) than the current evaluation, add to best moves
                if self.g.player_turn:
                    if opponent_evaluation >= curr_evaluation: best_moves[notation] = evaluation
                    # self.aip(f"Found a good evaluation as white\n")
                else:
                    if opponent_evaluation <= curr_evaluation: best_moves[notation] = evaluation
                    # self.aip(f"Found a good evaluation as black\n")

            self.aip(f"\t\tO.Eval = {opponent_evaluation} | Curr.Eval = {curr_evaluation} | INDEX = {i}", True)

        # if black, get lowest evaluation
        if self.g.player_turn: index_value = np.max(list(evals.values()))
        
        # if white, get the highest eval
        else: index_value = np.min(list(evals.values()))
        
        best = [key for key, value in evals.items() if value == index_value]

        # 3. Format and return target move
        if len(best) > 1: best = random.choice(best)
        else: best = best[0]

        self.g.update(best)
        return best

    def on_exit(self): 
        self.stop_thread = True
        self.join()

    def get_random_move(self, valid_moves):
        pprint(valid_moves)
        side = self.g.player_turn

        keys = list(valid_moves.keys())

        # pick randomly
        from_pos = random.choice(keys)

        count = 0
        while len(valid_moves[from_pos]) == 0 and count < len(keys):
            from_pos = random.choice(list(valid_moves.keys()))
            count += 1
        
        to_pos = random.choice(valid_moves[from_pos]) 
        
        return translate_move_t2s(from_pos[0], from_pos[1], to_pos[0], to_pos[1])