import random
import copy
import math
# Agent that plays chess


# TODO: variable that keeps track of current board state

# TODO: function that transforms board state by one move

# TODO: create tree where each valid move is a new node, and the board state is transformed one move, and that Node is analyzed for a score, and pruned if its much lower than the original

class AI :
    
    def __init__(self):
        self.current_board_state = None


    def get_move(self) -> tuple:
        move = ("a1", "b1")

        


        return move

    
    class Node:
        def __init__(self, board_state):

            self.board_state = board_state
            score = self.calculate_score()


        def calculate_score(self):

            # is_game_over, mat_diff, king_safety, piece_activity, pawn_structure, center_control = self.analyze_board()
            mat_diff = self.analyze_board()


        def analyze_board(self):
            
            piece_points_dict = {'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9}

            mat_diff = 0

            for row in range(8):
                for col in range(8):
                    # material difference
                    piece_char = self.board_state[row][col]
                    piece_point = piece_points_dict[piece_char.tolower()]
                    if piece_char.isLower():
                        piece_point *= -1
                    mat_diff += piece_point
            
            


