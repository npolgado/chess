import random
import copy
import math
from __init__ import *
# Agent that plays chess

# TODO: variable that keeps track of current board state
# TODO: function that transforms board state by one move
# TODO: create tree where each valid move is a new node, and the board state is transformed one move, and that Node is analyzed for a score, and pruned if its much lower than the original


class AI :
    
    def __init__(self):
        self.current_board_state = init_empty_board()

        # for el in self.current_board_state:
        #     print(el)

        self.root = self.Node(self.current_board_state)  

        # print("Score:", self.root.calculate_score())


    def get_target_move(self, valid_moves) -> tuple:

        count = 0
        for key in valid_moves:
            count += len(valid_moves[key])
        
        if count > 0:
            random_index = random.choice(range(count))
        else:
            return None

        
        for key in valid_moves:
            for value in valid_moves[key]:
                if random_index == 0:
                    random_move = (key, value)
                random_index -= 1

        
        move = translate_move_t2s(random_move[0][0], random_move[0][1], random_move[1][0], random_move[1][1])

        return move

    def recieve(self, move):
        return None
    
    class Node:
        def __init__(self, board_state, children=[]):

            self.board_state = board_state
            score = self.calculate_score()

            # TODO: add logic for children (PREREQ: game_state class, update_game(move))

        def calculate_score(self):

            # is_game_over, mat_diff, king_safety, piece_activity, pawn_structure, center_control = self.analyze_board()
            mat_diff = self.analyze_board()

            overall_score = mat_diff    # TODO: this will comebine metrics to create an ultimate score
            return overall_score


        def analyze_board(self):
            
            piece_points_dict = {'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 10}

            mat_diff = 0

            for row in range(8):
                for col in range(8):
                    # material difference
                    piece_char = self.board_state[row][col]
                    if piece_char == "-":
                        continue
                    piece_point = piece_points_dict[piece_char.lower()]
                    if piece_char.isupper():
                        piece_point *= -1
                    mat_diff += piece_point

            return mat_diff
            



