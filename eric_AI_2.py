import copy
import time
import random
import math

import multiprocessing

from __init__ import *
from graphics import Graphics
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

    def __init__(self, gs, team):
        super(AI, self).__init__()
        self.exit_flag = False

        self.gs = gs

        self.team_ = team       # deletable

        self.target_move = None
        if team == 0:
            self.your_turn = True
        else:
            self.your_turn = False
            
        self.current_board_state = init_empty_board()
        
        self.root = self.Node(gs_=copy.deepcopy(gs), parent=None, children=[], move=None)


    def run(self):
        try:
            while not self.exit_flag:
                depth = self.get_depth(self.root)
                if depth < 2:
                    print(f"Depth = {depth} \t(Team= {self.team_}) (Your Turn= {self.your_turn})")
                    self.generate_next_level(self.root)
                    self.minimax_traverse(self.root)
                    print(f"Depth = {depth} \t(Team= {self.team_}) (Your Turn= {self.your_turn})")
                
                else:
                    time.sleep(0.0001)
                

                if self.your_turn and depth == 2:
                    self.target_move = self.pick_move()

        except KeyboardInterrupt:
            print("Ctrl+C pressed. Exiting gracefully.")
        finally:
            self.exit_flag = True  # Set the exit flag to signal thread exit



    def get_move(self):
        # if random.randint(1, 100) == 1:
        #     print(f"My Move: {self.team_}")
        self.your_turn = True

        if self.target_move is None:
            return None
        
        self.your_turn = False      # no longer your move
        ret_move = self.target_move 
        self.target_move = None     # set target move to None
        self.root = self.root.get_child(ret_move)    # move root down a layer
        return ret_move
    

    def get_depth(self, cur_node, depth=0):
        if cur_node.children == []:
            return depth
        return self.get_depth(cur_node.children[0], depth+1)
        

    def generate_next_level(self, cur_node):
        time.sleep(.0001)
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
                n = self.Node(gs_=new_gs, parent=cur_node, children=[], move=mv)
                cur_node.children.append(n)

    def minimax_traverse(self, node):
        time.sleep(.0001)
        if node.children != []:
            for ch in node.children:
                self.minimax_traverse(ch)
        else:
            self.minimax(node)
    
    def minimax(self, node):
        time.sleep(.0001)
        if node is self.root:
            return
        if node is None:
            # print("Node is None")
            return
        if node.parent is None:
            # print("Parent Node is None")
            return
        
        # print(f"Node: {node.move}\tParent: {node.parent}")

        max = self.team_ == node.gs_.player_turn
        node.parent.score = node.parent.get_min_or_max_of_children(max)
        self.minimax(node.parent)

    def pick_move(self):
        max_score = math.inf * -1
        max_node = None
        for ch in self.root.children:
            # print(f"{ch.move}: {ch.score}")
            if ch.score > max_score:
                max_score = ch.score
                max_node = ch
        return max_node.move
    

    def receive(self, move):
        print(f"Received Move={move} \t(Team= {self.team_})")
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

            Exception("No Child with that Move")
            return None
        
        def get_score(self):
            return evaluate_board(self.gs_.board)


        def get_min_or_max_of_children(self, max):
            if max:
                # print("Max. Board = ")
                # for r in self.gs_.board:
                #     print(r)
                # print()
                max_node_score = math.inf * -1
                for ch in self.children:
                    # print(f"\t{ch.move}: {ch.score}")
                    if ch.score > max_node_score:
                        max_node_score = ch.score
                # print(f"\tChose {max_node.move}: {max_node.score}")
                return max_node_score
            
            else:
                # print("Min. Board = ")
                # for r in self.gs_.board:
                #     print(r)
                # print()
                min_node_score = math.inf
                for ch in self.children:
                    # print(f"\t{ch.move}: {ch.score}")
                    if ch.score < min_node_score:
                        min_node_score = ch.score
                # print(f"\tChose {min_node.move}: {min_node.score}")
                return min_node_score



def print_tree(n, depth=0):

    s = "\t" * depth
    print(f"{s} {n.move}: {n.score}")
    # for r in n.gs_.board:
    #     print(r)
    # print()
    for ch in n.children:
        print_tree(ch, depth+1)


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
                # move = players[turn].get_move()

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