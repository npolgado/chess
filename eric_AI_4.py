import copy
import time
import random
import math
import threading
import multiprocessing
from graphics import Graphics
import game_state
from __init__ import *
import logging, os

from operator import attrgetter

# TODO: look up how pruning works and compare it to my attempts. Am I doing it right? If so, why does it feel underwhelming (little time difference)
# Configure logging

log_filename = "output.log"
if os.path.exists(log_filename):
    with open(log_filename, "w"):
        pass

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler(log_filename)  # Log to file
    ]
)

custom_count = 0
def custom_print(*args, **kwargs):
    global custom_count
    log_message = " ".join(map(str, args))
    # print(log_message, **kwargs)
    if custom_count % 100 == 0:
        print(f"{100*custom_count/80000}%")
    custom_count += 1
    with open(log_filename, "a") as log_file:
        print(log_message, file=log_file, **kwargs)


class AI(threading.Thread):

    def __init__(self, gs, team):
        super(AI, self).__init__()
        self.gs = gs
        self.team_ = team
        self.target_move = None
        self.your_turn = team == 0
        self.root = self.Node(gs_=copy.deepcopy(gs), parent=None, children=[], move=None)

    def run(self):
        tree_depth = 3
        while True:
            d = self.get_depth(self.root)
            if d < tree_depth:
                self.generate_next_level(self.root)


                if self.team_ == 0:
            
                    custom_print("Depth:", d, "Team:", "black" if self.team_ else "white")
                    custom_print("BEFORE MINIMAX")
                    print_tree(copy.deepcopy(self.gs.board), self.root)

                    self.minimax(self.root, not self.team_)
                
                    custom_print("AFTER MINIMAX")
                    print_tree(copy.deepcopy(self.gs.board), self.root)

            if self.your_turn and d == tree_depth-1 and self.target_move is None:
                self.target_move = self.pick_move()
                print("Sleeping...")
                print(f"Chosen move: {self.target_move}")
                time.sleep(10000000)
            

    def get_move(self):
        self.your_turn = True
        if self.target_move is None:
            return None
        self.your_turn = False
        ret_move = copy.deepcopy(self.target_move)
        self.target_move = None
        
        self.root = self.root.get_child(ret_move)

        return ret_move

    def get_depth(self, cur_node, depth=0):
        if cur_node.children == []:
            return depth
        return self.get_depth(cur_node.children[0], depth+1)

    def generate_next_level(self, cur_node):

        if not cur_node.children:
            self.create_children(cur_node)
        else:
            for ch in cur_node.children:
                self.generate_next_level(ch)

    def create_children(self, cur_node):
        moves = cur_node.gs_.get_valid_moves()
        for start in moves:
            for end in moves[start]:
                mv = (start, end)
                new_gs = copy.deepcopy(cur_node.gs_)
                new_gs.update(mv)
                n = self.Node(gs_=new_gs, parent=cur_node, children=[], move=mv)
                cur_node.children.append(n)

    def minimax(self, node, maximizing_player, alpha=1000, beta=-1000):
        if not node.children:
            return node.get_score()

        if maximizing_player:
            best = beta
            for ch in node.children:
                val = self.minimax(ch, False, alpha, beta)
                best = max(best, val)
                alpha = max(alpha, best)
                if best <= alpha:
                    break
            node.score = best
            return best

        else:
            best = alpha
            for ch in node.children:
                val = self.minimax(ch, True, alpha, beta)
                best = min(best, val)
                beta = min(beta, best)
                if best <= beta:
                    print("--BROKEN--", beta, alpha)
                    break
            if node.score != best:
                print(f"REACHED - {ch.move}  (ch score: {ch})  {node.score} -> {best}")
            node.score = best
            return best

    


    def pick_move(self):
        scores = [ch for ch in self.root.children]
        if self.team_ == 0:
            max_value = max(scores, key=attrgetter('score')).score
            max_value_objects = [obj for obj in scores if obj.score == max_value]
            random_max_object = random.choice(max_value_objects)
            return random_max_object.move
        else:
            min_value = min(scores, key=attrgetter('score')).score
            min_value_objects = [obj for obj in scores if obj.score == min_value]
            random_min_object = random.choice(min_value_objects)
            return random_min_object.move

    def receive(self, move):
        self.target_move = None
        self.root = self.root.get_child(move)

    class Node:
        def __init__(self, gs_, move, parent, children):
            self.gs_ = gs_
            self.move = move
            self.score = self.get_score()
            self.parent = parent
            self.children = children

        def get_child(self, move_):
            for ch in self.children:
                if ch.move == move_:
                    return ch
            raise Exception("No Child with that Move:", move_)

        def get_score(self):
            end_status, string_status = self.gs_.handle_end_game(not self.gs_.get_player_turn)
            if end_status != -1:
                if end_status == 3:
                    return 0
                elif end_status == 0:
                    return 100
                elif end_status == 1:
                    return -100
            return evaluate_board(self.gs_.board)

        def get_min_or_max_of_children(self, max_player):
            scores = [ch.score for ch in self.children]
            return max(scores) if max_player else min(scores)


def print_tree(board, n, depth=0):
    # if depth >= 3:
    #     return

    if n.move is not None:
        mv_start = n.move[0]
        mv_end = n.move[1]
        s = "\t" * depth
        custom_print(f"{s} {board[mv_start[0]][mv_start[1]]} {mv_start[0]},{mv_start[1]} => {mv_end[0]},{mv_end[1]}  =  {n.score}    d={depth}")

    else:
        custom_print(f"ROOT =  {n.score}")
    for ch in n.children:
        print_tree(n.gs_.board, ch, depth+1)


if __name__ == "__main__":

    custom_print("Starting...")

    gs = game_state.GameState()
    p1 = AI(gs, 0)
    p2 = AI(gs, 1)

    graphics = Graphics(
        display_index=1,
        fullscreen=False
    )

    p1.start()
    p2.start()

    players = (p1, p2)

    while True:
        gs.tick()
        turn = gs.get_player_turn()

        move = players[turn].get_move()
        if move is None:
            gs.tick()
            graphics.draw(gs)
            continue

        gs.update(move)
        players[not turn].receive(move)
        
        graphics.draw(gs)
