import random
import copy
import math
from __init__ import *


# Agent that plays chess

# as a thread
# go 3 layers deep
# each node is a board state
# calculate the score of each node
# when a new move is made, remove all other nodes (set move to root) and calculate another layer.
# when you make a move, remove all other nodes (set move to root) and calculate another layer

class AI:

    def __init__(self):
        self.current_board_state = init_empty_board()

        # variable to keep
        self.target_move = None

        self.root = self.Node(self.current_board_state)

    def target_move(self):
        # when ready, return move. If not ready, return None
        if self.target_move is None:
            return None
        else:
            a = self.target_move
            self.target_move = None
            return a

    def get_ai_move(self, valid_moves) -> tuple:
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

    def recieve(self, game_state):
        return None

    class Node:
        def __init__(self, board_state, children=[]):

            self.board_state = board_state
            score = self.calculate_score()

            # TODO: add logic for children (PREREQ: game_state class, update_game(move))

        def calculate_score(self):

            # is_game_over, mat_diff, king_safety, piece_activity, pawn_structure, center_control = self.analyze_board()
            mat_diff = self.analyze_board()

            overall_score = mat_diff  # TODO: this will comebine metrics to create an ultimate score
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

