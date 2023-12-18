import os
import sys
import numpy as np
from new_game import *

class Move:
    def __init__(self, start, end) -> None:
        self.start = pos_to_row_col(start)
        self.end = pos_to_row_col(end)

    def __init__(self, notation) -> None:
        # assert notation is a string of length 4
        assert type(notation) == str
        assert len(notation) == 4

        self.start = pos_to_row_col(notation[:2])
        self.end = pos_to_row_col(notation[2:])

class GameState:
    def __init__(self, turn: int=1) -> None:
        self.turn = turn

        self.bool_turn = (self.turn - 1) % 2
        self.enpassant_square = None
        
        self.board_history = []
        self.board_dict = {}
        self.is_three_fold_repetition = False

    def get_board(self):
        return self.board

    def get_turn(self):
        return self.turn

    def get_player_turn(self):
        return self.bool_turn
    
    def get_board_history(self):
        return self.board_history

    def get_three_fold_repetition(self):
        return self.is_three_fold_repetition

    def archive(self, board):
        board_str = board_to_string(self.board)
        self.board_history.append(board_str)

        if board_str in self.board_dict:
            self.board_dict[board_str] += 1
            if self.board_dict[board_str] >= 3:
                self.is_three_fold_repetition = True
        else:
            self.board_dict[board_str] = 1

    def update(self, board, en_passant=None):        
        self.enpassant_square = en_passant
        
        self.archive(board)
        
        self.turn += 1
        self.bool_turn = not self.bool_turn