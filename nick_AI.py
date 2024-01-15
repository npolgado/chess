import numpy as np
from __init__ import *
from game_state import GameState
import threading
import random
import time
import copy

class Tree:
    def __init__(self, board, parent=None, move=None, depth=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.depth = depth
        self.children = []

class AI(threading.Thread):
    def __init__(self, DEBUG=False, lock=None): # ): # 
        super().__init__()
        
        self.send_move = False
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
            with self.lock:               
                if self.stop_thread: 
                    self.stop_thread = False
                    return
                
                if self.recieved_move:
                    self.recieved_move = False
                    
                    self.g.update(self.last_opponent_move)
                    
                    side = "Black" if self.g.player_turn else "White"
                    self.aip(f"{side} AI THREAD recieved move {self.last_opponent_move}")
                    
                    self.last_opponent_move = None

                    pprint(self.g.board)

                    v_m = self.g.get_valid_moves()
                    move = self.calculate_move(v_m)
                    
                    self.g.update(move)

                    self.aip(f"{side} AI THREAD calculated move {move}")
                    
                    self.target_move = move
                    self.send_move = True
            
            time.sleep(0.001)

    def recieve(self, move):
        with self.lock:
            if move is not None:

                self.last_opponent_move = move
                self.recieved_move = True
                
                # self.aip(f"AI Game State Updated\n\tPlayer: {self.g.player_turn} | Turn: {self.g.turn_num}", True)
            
            else: self.aip("Recieved None")

    def get_move(self, valid_moves):
        # pprint(valid_moves)
        with self.lock:
            if self.send_move:
                self.send_move = False
                # self.aip(f"AI Sending Move {self.target_move}", True)
                tmp = self.target_move
                self.target_move = None
                return tmp
            
            elif self.g.turn_num == 1:
                move = self.get_random_move(valid_moves)
                self.g.update(move)
                return move
            
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
        # with self.lock:
        # Save current board state
        side = "Black" if self.g.player_turn else "White"
        curr_board = copy.deepcopy(self.g.board)
        curr_evaluation = evaluate_board(curr_board)

        # self.aip(f"Getting Target Move\n\tTurn {self.g.turn_num} | {side}'s Turn | Eval = {curr_evaluation}")

        # 1. Get all possible moves evaluations
        evals = self.get_evals(valid_moves, curr_board)
        best_moves = {}

        # 2. Find the best move
        #   a. go through possible moves
        for notation, evaluation in evals.items():
            # self.aip(f"\tPossible Move {notation}: {evaluation}")

            branch = copy.deepcopy(self.g)
            branch.update(notation)

            valid_opponent_moves = branch.get_valid_moves()

            # go through opponent moves and get the worst case scenario
            opponent_evals = self.get_evals(valid_opponent_moves, branch.board)
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

            # self.aip(f"{side}\t\tO.Eval = {opponent_evaluation} | Curr.Eval = {curr_evaluation} | INDEX = {i}", True)

        # if black, get lowest evaluation
        if self.g.player_turn: index_value = np.min(list(evals.values()))
        
        # if white, get the highest eval
        else: index_value = np.max(list(evals.values()))
        
        best = [key for key, value in evals.items() if value == index_value]

        # 3. Format and return target move
        if len(best) > 1: best = random.choice(best)
        else: best = best[0]

        return best

    def on_exit(self): 
        self.stop_thread = True
        self.join()

    def get_random_move(self, valid_moves):
        # pprint(valid_moves)
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