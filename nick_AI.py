import numpy as np
from __init__ import *
from game_state import GameState
import threading
import random
import time
import copy

''' 
Ai has a background task always running

Need to make a class that abstracts the search space given a board state

'''

class Node:
    def __init__(self, gs: GameState, move=None, parent=None, children=None):
        self.gs = copy.deepcopy(gs)
        self.board = self.gs.board
        
        self.move = move
        
        self.parent = parent
        self.children = children
        self.depth = self.get_depth()

    def get_depth(self, depth=0):
        # Recursive function to get the depth of the node
        if self.parent is None: return depth
        else:                   return self.parent.get_depth(depth+1)

    def get_parent(self):   return self.parent
    def get_board(self):    return self.board
    def get_move(self):     return self.move
    def get_gs(self):       return self.gs

    def get_children(self):
        if self.children is None:
            self.children = []
            valid_moves = self.gs.get_valid_moves()
            
            for i in valid_moves.keys():
                for j in valid_moves[i]:

                    notation = translate_move_t2s(*i, *j)
                    new_gs = copy.deepcopy(self.gs)
                    new_gs.update(notation)

                    self.children.append(Node(new_gs, notation, self))
        
        return self.children

class AI(threading.Thread):
    def __init__(self, DEBUG=False, lock=None): # ): # 
        super().__init__()
        
        self.send_move = False
        self.recieved_move = False

        self.last_opponent_move = None
        self.target_move = None

        # self.thread = threading.Thread(target=self.run)
        if lock:    self.lock = lock
        else:       self.lock = threading.Lock()
        
        self.stop_thread = False
        self.debug = DEBUG
        self.g = GameState()
        self.root = Node(self.g)

    def run(self):
        while True:
            with self.lock:               
                if self.stop_thread: 
                    self.stop_thread = False
                    return
                
                if self.recieved_move:
                    self.recieved_move = False
                    
                    side = "Black" if self.g.player_turn else "White"

                    self.g.update(self.last_opponent_move)
                    
                    self.aip(f"{side} AI THREAD recieved move {self.last_opponent_move}")
                    
                    self.last_opponent_move = None

                    v_m = self.g.get_valid_moves()
                    move = self.calculate_move(v_m)
                    
                    self.g.update(move)
                    
                    self.target_move = move
                    
                    self.send_move = True

                    self.aip(f"{side} AI THREAD calculated move {move}")
            
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
    
    def on_exit(self): 
        self.stop_thread = True
        self.join()


if __name__ == "__main__":
    gs = GameState()
    n = Node(gs)

    # 100 moves
    for mo in range(100):
        tmp = copy.deepcopy(n)
        depth = 5
        curr_eval = evaluate_board(n.board)
        side = n.gs.player_turn
        side_txt = "Black" if side else "White"
        print(f"Move {mo} | Turn {n.gs.turn_num} | {side_txt}'s Turn | Eval = {curr_eval}\n-----------------------------------")

        while depth > 0:
            # generate layer of children
            tmp.get_children()

            # Get evals for all children
            evals = {}
            for i in tmp.children: 
                evals[i.get_move()] = evaluate_board(i.get_board())
 
            # Get best move for layer
            best_eval = curr_eval
            index_value = curr_eval
            for notation, evaluation in evals.items(): 
                # print(f"\t{notation} | {evaluation}")

                # IF BLACK
                if tmp.gs.player_turn:
                    # if the evaluation is better than the current evaluation, set the index value to the evaluation
                    if evaluation <= curr_eval and evaluation < best_eval: 
                        index_value = evaluation
                        best_eval = evaluation
                
                # IF WHITE
                else:
                    # if the evaluation is better than the current evaluation, set the index value to the evaluation
                    if evaluation >= curr_eval and evaluation > best_eval: 
                        index_value = evaluation
                        best_eval = evaluation
            
            # Get best move notation
            best = [key for key, value in evals.items() if value == index_value]
            if len(best) > 1: best = random.choice(best)
            else: best = best[0]

            print(f'Depth {depth} | Best Eval {index_value} | Best Move {best}')

            # set tmp equal to the child of temp that has the best move
            for i in tmp.get_children():
                if i.get_move() == best: tmp = i

            depth -= 1

        # TMP is now the best move after depth
        # we need to get the best move from the children of tmp
        


        print(f"Found best move {best} with eval {index_value}")
        print("-----------------------------------")

        
        
        
        time.sleep(0.1)


