import random
import copy
import math
from __init__ import *

import game_state


# Agent that plays chess

# as a thread
# go 3 layers deep
# each node is a board state
# calculate the score of each node
# when a new move is made, remove all other nodes (set move to root) and calculate another layer.
# when you make a move, remove all other nodes (set move to root) and calculate another layer

import threading

class AI(threading.Thread):

    def __init__(self, gs):

        super().__init__()

        self.gs = gs

        self.current_board_state = init_empty_board()
        self.root = self.Node(gs_=copy.deepcopy(gs), parent=None, children=[])



    def run(self):
        for i in range(5):
            print(f"DEPTH = {i}")
            self.generate_next_level(self.root)
            print_tree(self.root)
            print("\n----------------------------\n")





    def generate_next_level(self, cur_node):
        if cur_node.children == []:
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
                # new_board = make_move(b_, mv)[0]
                n = self.Node(gs_=new_gs, parent=cur_node, children=[])
                cur_node.children.append(n)

    
    class Node:
        def __init__(self, gs_, parent, children):
            self.gs_ = gs_
            
            self.parent = parent
            self.children = children


def print_tree(n, depth=0):
    # print("\t"*depth, board_to_string(n.gs_.board))
    for r in n.gs_.board:
        print(r)
    print()
    for ch in n.children:
        print_tree(ch, depth+1)






if __name__ == "__main__":

    gs = game_state.GameState()

    p1 = AI(gs)

    p1.start()

    # print(string_to_board("rnbqkbnr/ppppppp1/8/8/7p/7N/PPPPPPPP/RNBQKBR1"))
