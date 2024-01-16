import copy
import time
import random
import math
import threading
import multiprocessing
from graphics import Graphics
import game_state
from __init__ import *

from operator import attrgetter

class AI(threading.Thread):

    def __init__(self, gs, team):
        super(AI, self).__init__()
        self.gs = gs
        self.team_ = team
        self.target_move = None
        self.your_turn = team == 0
        self.root = self.Node(gs_=copy.deepcopy(gs), parent=None, children=[], move=None)


    def run(self):
        while True:
            d = self.get_depth(self.root)
            if d < 3:
                self.generate_next_level(self.root)
                self.minimax_traverse(self.root)
                print(f"\t(Depth = {d})  (Team= {self.team_}) (Your Turn= {self.your_turn})")

            if self.your_turn and d == 3 and self.target_move is None:
                self.target_move = self.pick_move()

    def get_move(self):
        self.your_turn = True
        if self.target_move is None:
            return None
        self.your_turn = False
        ret_move = copy.deepcopy(self.target_move)
        self.target_move = None
        mv_start = ret_move[0]
        mv_end = ret_move[1]

        # print_tree(copy.deepcopy(self.gs.board), self.root)
        print()
        for r in self.gs.board:
            print(r)
        print()
        print(f"MOVE: {self.gs.board[mv_start[0]][mv_start[1]]} {mv_start[0]},{mv_start[1]} => {mv_end[0]},{mv_end[1]}")
        s = "WHITE" if self.team_ == 0 else "BLACK"
        print(f"===Team: {s}===\n")
        print("\n---------------------------------------\n")
        
        self.root = self.root.get_child(ret_move)
        return ret_move

    def get_depth(self, cur_node, depth=0):
        if cur_node.children == []:
            return depth
        return self.get_depth(cur_node.children[0], depth+1)

    def generate_next_level(self, cur_node):

        if not cur_node.children:
            # if cur_node is self.root:
            #     print("reached")
            #     start = (0, 1)
            #     end = (4, 5)
            #     mv = (start, end)
            #     new_gs = copy.deepcopy(cur_node.gs_)
            #     new_gs.update(mv)
            #     n = self.Node(gs_=new_gs, parent=cur_node, children=[], move=mv)
            #     cur_node.children.append(n)
            # else:
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

    def minimax_traverse(self, node):
        if node.children:
            for ch in node.children:
                self.minimax_traverse(ch)
        else:
            self.minimax(node)

    def minimax(self, node):
        if node is self.root:
            return
        if node is None:
            return
        if node.parent is None:
            return

        max_player = node.gs_.player_turn != 0
        node.parent.score = node.parent.get_min_or_max_of_children(max_player)
        self.minimax(node.parent)

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
        # print(f"Received Move={move} \t(Team= {self.team_})")
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
            
            # for row in self.gs_.board:
            #     print(row)
            # print()
            for ch in self.children:
                # print("\t", ch.move)
                if ch.move == move_:
                    return ch
            raise Exception("No Child with that Move:", move_)

        def get_score(self):
            return evaluate_board(self.gs_.board)

        def get_min_or_max_of_children(self, max_player):
            scores = [ch.score for ch in self.children]
            return max(scores) if max_player else min(scores)


def print_tree(board, n, depth=0):
    # if depth >= 2:
    #     return
    
    if n.move is not None:
        mv_start = n.move[0]
        mv_end = n.move[1]
        print(f"{s} {board[mv_start[0]][mv_start[1]]} {mv_start[0]},{mv_start[1]} => {mv_end[0]},{mv_end[1]}  =  {n.score}")
    for ch in n.children:
        print_tree(board, ch, depth+1)


if __name__ == "__main__":

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

    try:
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

            for r in gs.board:
                print(r)
            print()

    except KeyboardInterrupt:
        print("Ctrl+C pressed. Exiting gracefully.")
        p1.join()
        p2.join()
        p1.terminate()
        p2.terminate()
